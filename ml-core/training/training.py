import concurrent.futures
from typing import List, Dict, Tuple
from json import loads

from starlette.responses import Response
from pandas import DataFrame, Series
from sklearn import feature_selection
from sklearn.svm import SVC
from sklearn.feature_selection import chi2
from sklearn.model_selection import GridSearchCV
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


from models.User import User
from training.common import (
    check_bugs_count,
    compare_resolutions,
    stringify_ttr_intervals,
)
from training.classess import filter_classes, encode_series
from training.stop_words import get_stop_words
from training.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer
from training.mark_up import (
    mark_up_series,
    mark_up_other_data,
)
from error_handlers.exceptions import (
    SmallNumberRepresentatives,
    LittleDataToAnalyze,
    ResolutionElementsMissed,
    InconsistentGivenData,
    InvalidSourceField,
    AreaOfTestingEmpty,
    BugResolutionEmpty,
)
from error_handlers.warnings import BugsNotFoundWarning
from database.users.settings import (
    save_top_terms,
    save_models,
    save_training_parameters,
    get_issues_fields,
    get_source_field,
    get_bug_resolutions,
    get_mark_up_entities,
)
from database.issues.query import get_issues_dataframe
from cache import redis_conn, clear_cache


def get_k_neighbors(series: Series) -> int:
    """Calculates the number of k-nearest neighbors.

    :param series: data used for calculations.
    :return: Number of k-nearest neighbors.
    """
    unique_values_count = series.value_counts()
    k_neighbors = (
        int(min(unique_values_count) / 2) if len(unique_values_count) != 0 else 0
    )

    if k_neighbors <= 1:
        raise SmallNumberRepresentatives(
            f"Oops! Too small number of class representatives for {series.name}"
        )

    if len(set(unique_values_count)) == 1:
        return 2

    return k_neighbors


def get_best_params(model, X: Series, Y: Series) -> Dict[str, int]:
    """Selects optimal parameters for model.

    :param model: model;
    :param X: training vector;
    :param Y: target values.
    :return: Best parameters for model.
    """
    param_grid = {"clf__C": [1, 2], "clf__gamma": [2, 5]}

    gs = GridSearchCV(model, param_grid, scoring="f1_weighted", cv=10, n_jobs=12)
    gs.fit(X, Y)
    return gs.best_params_


def train_imbalance(
    descr_series: Series,
    classes_codes: Series,
    TFIDF_,
    IMB_,
    FS_,
    req_percentage: int,
    CLF_,
    model_name: str,
) -> Tuple[Dict[str, Pipeline], Dict[str, dict]]:
    """Trains models using handled setting and saves them as binary objects.

    :param descr_series: description series.
    :param classes_codes: series with classes' codes.
    :param TFIDF_: vectorizer.
    :param IMB_: SMOTE instance.
    :param FS_: ranking terms method.
    :param req_percentage: percentage to be taken from the ranked list.
    :param CLF_: classifier.
    :param model_name: models name.
    :return: Trained model in byte representation associated to its model name.
    """
    transformer = feature_selection.SelectPercentile(FS_)
    clf_model = Pipeline(
        [("tfidf", TFIDF_), ("imba", IMB_), ("fs", transformer), ("clf", CLF_)]
    )

    best_params = get_best_params(clf_model, descr_series, classes_codes)
    print(f"{model_name}:{best_params}")

    clf_model.set_params(
        fs__percentile=req_percentage,
        clf__C=best_params["clf__C"],
        clf__gamma=best_params["clf__gamma"],
    ).fit(descr_series, classes_codes)

    return {model_name: clf_model}, {model_name: best_params}


def execute_training(
    instance: User,
    issues: DataFrame,
    areas_of_testing: List[str],
    resolution: List[str],
):
    """Train models.

    :param instance: Instance of User model.
    :param issues: Bug reports.
    :param areas_of_testing: Areas of testing.
    :param resolution: Resolution.
    """

    def _params_producer() -> Tuple[Series, Series, SMOTE, str]:
        """Generates parameters for imbalance training.

        Returns:
        ----------
            Bugs description, classes codes, SMOTE instance and model name.
        """
        for metric in filtered_classes.keys():
            if metric in ["Priority", "Time to Resolve"]:
                filtered_df = issues[issues[metric].isin(filtered_classes[metric])]
                smt = SMOTE(
                    ratio="minority",
                    random_state=0,
                    kind="borderline1",
                    n_jobs=4,
                )
                smt.k_neighbors = get_k_neighbors(
                    filtered_df[metric.lower() + "_codes"]
                )
                classes_codes = filtered_df[metric.lower() + "_codes"]
                model_name = metric.split("_")[0]

                yield filtered_df.Description_tr, classes_codes, smt, model_name
            else:
                for class_ in filtered_classes[metric]:
                    df_index = (
                        "Resolution_" + class_ if metric == "Resolution" else class_
                    )
                    smt = SMOTE(
                        ratio="minority",
                        random_state=0,
                        kind="borderline1",
                        n_jobs=4,
                    )
                    smt.k_neighbors = get_k_neighbors(issues[df_index])

                    yield issues.Description_tr, issues[df_index], smt, class_

    issues = issues[
        (issues["Resolution"] != "Unresolved")
        & (issues["Resolved"].isna() is not True)
        & (issues["Resolved"].notnull())
    ]
    issues = issues.reset_index()

    if not check_bugs_count(issues):
        raise LittleDataToAnalyze

    issues = encode_series(issues)
    filtered_classes = filter_classes(issues, areas_of_testing, resolution)

    # TODO: remove unnecessary resolution verification
    # when settings will be linked to data
    missing_resolutions = compare_resolutions(issues.Resolution, resolution)
    if missing_resolutions:
        raise ResolutionElementsMissed(
            f"Oops! These Resolution elements are missed: {missing_resolutions}. Models can't be trained."
        )

    filtered_elements = (set(resolution).union(set(areas_of_testing))).difference(
        set(filtered_classes.get("Resolution")).union(
            set(filtered_classes.get("areas_of_testing"))
        )
    )

    if filtered_elements and filtered_elements != {"Other"}:
        raise SmallNumberRepresentatives(
            f"Oops! Too little number of class representatives for: {filtered_elements}. Models can't be trained."
        )

    svm_imb = SVC(gamma=2, C=1, probability=True, class_weight="balanced")
    sw = get_stop_words(issues)
    tfidf = StemmedTfidfVectorizer(stop_words=sw)

    try:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            models_and_params = {
                executor.submit(
                    train_imbalance,
                    description,
                    classes,
                    tfidf,
                    smote,
                    chi2,
                    50,
                    svm_imb,
                    model_name,
                )
                for description, classes, smote, model_name in _params_producer()
            }
            models = [
                model.result()[0]
                for model in concurrent.futures.as_completed(models_and_params)
            ]
            params = [
                param.result()[1]
                for param in concurrent.futures.as_completed(models_and_params)
            ]
    except ValueError:
        raise InconsistentGivenData

    save_models(user=instance, raw_models=models)

    filtered_classes["Time to Resolve"] = stringify_ttr_intervals(
        filtered_classes["Time to Resolve"]
    )
    filtered_classes["binary"] = [0, 1]

    save_training_parameters(user=instance, classes=filtered_classes, params=params)

    resolutions = ["Resolution_" + resol for resol in filtered_classes["Resolution"]]

    save_top_terms(
        user=instance,
        issues=issues,
        resolutions=resolutions,
        priorities=filtered_classes["Priority"],
        areas_of_testing=filtered_classes["areas_of_testing"],
    )


def train_models(user: User):
    cache = redis_conn.get(f"user:{user.id}:analysis_and_training:filters")
    filters = loads(cache) if cache else None
    fields = get_issues_fields(user)
    issues = get_issues_dataframe(filters=filters, fields=fields)

    if issues.empty:
        raise BugsNotFoundWarning

    source_field = get_source_field(user)
    if source_field not in issues.columns:
        raise InvalidSourceField

    resolutions = (
        [resolution["value"] for resolution in get_bug_resolutions(user)]
        if len(get_bug_resolutions(user)) != 0
        else []
    )

    if not resolutions:
        raise BugResolutionEmpty

    areas_of_testing = []

    mark_up_entities = get_mark_up_entities(user)
    if source_field:
        areas_of_testing = [area["area_of_testing"] for area in mark_up_entities] + [
            "Other"
        ]
        for area in mark_up_entities:
            issues = mark_up_series(
                issues,
                get_source_field(user),
                area["area_of_testing"],
                area["entities"],
            )
        issues = mark_up_other_data(issues, areas_of_testing)

    if len(areas_of_testing) == 1:
        raise AreaOfTestingEmpty

    execute_training(
        user,
        issues,
        areas_of_testing,
        resolutions,
    )

    clear_cache(
        ["qa_metrics:predictions_page", "qa_metrics:predictions_table"],
        user.id,
    )

    return Response(status_code=200)
