import concurrent.futures
import json
import numpy
from typing import List, Dict, Union, Tuple

from pandas import qcut, get_dummies, Categorical, DataFrame, Series, Interval
from sklearn import feature_selection
from sklearn.feature_selection import chi2, SelectKBest
from imblearn.pipeline import Pipeline
from pickle import dumps
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from django.db.models import Model

from apps.analysis_and_training.main.common import (
    get_stop_words,
    check_required_percentage,
    check_bugs_count,
)
from apps.authentication.models import User

from apps.settings.models import (
    UserTrainingParameters,
    UserSettings,
    UserTopTerms,
    UserModels,
)
from utils.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer
from utils.exceptions import (
    SmallNumberRepresentatives,
    LittleDataToAnalyze,
    ResolutionElementsMissed,
    InconsistentGivenData,
)
from utils.warnings import ModelsNotTrainedWarning

from sklearn.model_selection import GridSearchCV

ModelParams = List[Dict[str, Dict[str, int]]]
TrainingParameters = Union[List[str], List[int], Dict[str, List[str]]]
ModelClasses = Dict[str, TrainingParameters]
ModelPipeline = Dict[str, Pipeline]


def compare_resolutions(issues: DataFrame, resolutions: List[str]) -> set:
    """Checks for difference between required resolutions and those that are present in df.

    Parameters:
    ----------
    issues:
        Bug reports.
    resolutions:
        bugs resolution.

    Returns:
    ----------
        The difference between the required resolutions and those that are present in the dataframe.
    """
    return set(resolutions).difference(set(issues.Resolution.unique()))


def get_k_neighbors(series: Series) -> int:
    """Calculates the number of k-nearest neighbors.

    Parameters:
    ----------
    series:
        data used for calculations.

    Returns:
    ----------
        Number of k-nearest neighbors.
    """
    unique_values_count = series.value_counts()
    k_neighbors = (
        int(min(unique_values_count) / 2)
        if len(unique_values_count) != 0
        else 0
    )

    if k_neighbors <= 1:
        raise SmallNumberRepresentatives(
            f"Oops! Too small number of class representatives for {series.name}"
        )

    if len(set(unique_values_count)) == 1:
        return 2

    return k_neighbors


def stringify_ttr_intervals(intervals: List[Interval]) -> str:
    """Stringifies list of ttr intervals.

    Parameters:
    ----------
    intervals:
        intervals.

    Returns:
    ----------
        Stringified list of intervals.
    """
    return (
        [
            str(intervals[0].left if intervals[0].left > 0 else 0)
            + "-"
            + str(intervals[0].right)
        ]
        + [
            str(intervals[el].left + 1) + "-" + str(intervals[el].right)
            for el in range(1, len(intervals) - 1)
        ]
        + [">" + str(intervals[len(intervals) - 1].left)]
    )


def filter_classes(
    issues: DataFrame, areas_of_testing: List[str], resolution: List[str]
) -> ModelClasses:
    """Filters out classes with inadequate percentage of representatives.

    Parameters:
    ----------
    issues:
        Bug reports.
    areas_of_testing:
        areas of testing classes;
    resolution:
        resolution classes.

    Returns:
    ----------
        Classes of models.
    """
    classes = {
        "areas_of_testing": areas_of_testing,
        "Resolution": resolution,
        "Priority": issues["Priority"].unique().tolist(),
        "Time to Resolve": issues["Time to Resolve"].unique().tolist(),
    }

    filtered_classes = {}
    for metric in classes.keys():
        if metric == "areas_of_testing":
            filtered_classes[metric] = [
                el
                for el in classes[metric]
                if check_required_percentage(issues[el], 1)
                and len(set(issues[el])) != 1
            ]
        else:
            filtered_classes[metric] = sorted(
                [
                    el
                    for el in classes[metric]
                    if check_required_percentage(issues[metric], el)
                    and len(set(issues[metric])) != 1
                ]
            )

    return filtered_classes


def encode_series(issues: DataFrame) -> DataFrame:
    """Encodes series classes.

    Parameters:
    ----------
    issues:
        Bug reports.

    Returns:
    ----------
        Dataframe containing encoded series.
    """

    # TODO Investigation is required for imbalanced data
    issues["Time to Resolve"] = qcut(
        issues["Time to Resolve"].astype(int), q=4, duplicates="drop"
    )
    issues["time to resolve_codes"] = issues[
        "Time to Resolve"
    ].cat.rename_categories(range(len(issues["Time to Resolve"].unique())))

    issues["priority_codes"] = Categorical(
        issues["Priority"], ordered=True
    ).codes

    issues = issues.reset_index(drop=True)
    series_resolution = issues["Resolution"]
    issues = get_dummies(issues, columns=["Resolution"])
    issues["Resolution"] = series_resolution

    return issues


def get_best_params(model, X: Series, Y: Series) -> dict:
    """Selects optimal parameters for model.

    Parameters:
    ----------
    model:
        model;
    X:
        training vector;
    Y:
        target values.

    Returns:
    ----------
        Best parameters for model.
    """
    param_grid = {"clf__C": [1, 2], "clf__gamma": [2, 5]}

    gs = GridSearchCV(
        model, param_grid, scoring="f1_weighted", cv=10, n_jobs=12
    )
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
) -> tuple:
    """Trains models using handled setting and saves them as .sav objects.

    Parameters:
    ----------
    instance:
        Instance of User model.
    descr_series:
        description series.
    classes_codes:
        series with classes' codes.
    TFIDF_:
        vectorizer.
    IMB_:
        SMOTE instance.
    FS_:
        ranking terms method.
    req_percentage:
        percentage to be taken from the ranked list.
    CLF_:
        classifier.
    model_name:
        models name.

    Returns:
    ----------
        Trained model in byte representation associated to its model name.

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


def save_training_parameters(
    user: Model,
    classes: ModelClasses,
    params: ModelParams,
):
    """Saves training parameters to the database.

    Parameters:
    ----------
    user:
        User.
    classes:
        classes.
    params:
        params for model.
    """
    training_settings = {}

    for class_ in classes:
        if class_ == "Resolution":
            training_settings["Resolution"] = {}
            resolution_settings = training_settings["Resolution"]
            for resolution in classes[class_]:
                resolution_settings[resolution] = [
                    "not " + resolution,
                    resolution,
                ]
        else:
            training_settings[class_] = classes[class_]

    training_settings["model_params"] = params

    user_settings = UserSettings.objects.get(user=user)
    for (
        training_settings_name,
        training_settings_value,
    ) in training_settings.items():
        UserTrainingParameters.objects.create(
            name=training_settings_name,
            training_parameters=json.dumps(training_settings_value),
            settings=user_settings,
        )


def train(
    instance: Model,
    issues: DataFrame,
    areas_of_testing: List[str],
    resolution: List[str],
):
    """Train models.

    Parameters:
    ----------
    instance:
        Instance of User model.
    issues:
        Bug reports.
    areas_of_testing:
        areas of testing.
    resolution:
        resolution.
    """

    def _params_producer() -> Tuple[Series, Series, SMOTE, str]:
        """Generates parameters for imbalance training.

        Returns:
        ----------
            Bugs description, classes codes, SMOTE instance and model name.
        """
        for metric in filtered_classes.keys():
            if metric in ["Priority", "Time to Resolve"]:
                filtered_df = issues[
                    issues[metric].isin(filtered_classes[metric])
                ]
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
                        "Resolution_" + class_
                        if metric == "Resolution"
                        else class_
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
    missing_resolutions = compare_resolutions(issues, resolution)
    if missing_resolutions:
        raise ResolutionElementsMissed(
            f"Oops! These Resolution elements are missed: {missing_resolutions}. Models can't be trained."
        )

    filtered_elements = (
        set(resolution).union(set(areas_of_testing))
    ).difference(
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

    save_models(user=instance, models=models)

    filtered_classes["Time to Resolve"] = stringify_ttr_intervals(
        filtered_classes["Time to Resolve"]
    )
    filtered_classes["binary"] = [0, 1]

    save_training_parameters(
        user=instance, classes=filtered_classes, params=params
    )

    resolutions = [
        "Resolution_" + resol for resol in filtered_classes["Resolution"]
    ]

    save_top_terms(
        user=instance,
        issues=issues,
        resolutions=resolutions,
        priorities=filtered_classes["Priority"],
        areas_of_testing=filtered_classes["areas_of_testing"],
    )


def get_top_terms(issues: DataFrame, metric: str) -> dict:
    """Calculates top terms.

    Parameters:
    ----------
    issues:
        Bug reports.
    metric:
        Value which is used for calculations.

    Returns:
    ----------
        Object with calculated terms.
    """
    chi2 = feature_selection.chi2

    sw = get_stop_words(issues)
    tfidf = StemmedTfidfVectorizer(stop_words=sw)
    tfs = tfidf.fit_transform(issues["Description_tr"])

    y = issues[metric]
    selector = SelectKBest(score_func=chi2, k="all")
    selector.fit_transform(tfs, y)

    return dict(zip(tfidf.get_feature_names(), selector.scores_))


def calculate_top_terms(issues: DataFrame, metric: str) -> list:
    """Calculates top terms which are based on significance weights.

    Parameters:
    ----------
    issues:
        Bug reports.
    metric:
        field which is used for calculation.

    Returns:
    ----------
        list of the calculated terms.

    """
    terms = get_top_terms(issues, metric)

    terms = {k: v for (k, v) in terms.items() if v > 1}
    return [
        k for (k, v) in terms.items() if v > numpy.mean(list(terms.values()))
    ]


def save_top_terms(
    user: Model,
    issues: DataFrame,
    resolutions: List[str],
    priorities: List[str],
    areas_of_testing: List[str],
):
    """Saves calculation results to database.

    Parameters:
    ----------
    user:
        User.
    issues:
        Bug reports.
    resolutions:
        Resolutions.
    priorities:
        Priorities derived after models' training.
    areas_of_testing:
        Areas of testing derived after models' training.

    """
    binarized_df = get_dummies(
        issues,
        prefix=["Priority"],
        columns=["Priority"],
    )
    top_terms = {}

    metrics = (
        ["Priority_" + priority for priority in priorities]
        + resolutions
        + [area for area in areas_of_testing if area != "Other"]
    )

    for metric in metrics:
        top_terms[metric] = calculate_top_terms(binarized_df, metric)

    top_terms = DataFrame(
        {metric: Series(terms) for metric, terms in top_terms.items()}
    )

    user_settings = UserSettings.objects.get(user=user)
    UserTopTerms.objects.filter(settings=user_settings).delete()
    UserTopTerms.objects.create(
        top_terms_object=dumps(top_terms),
        settings=user_settings,
    )


def check_training_files(user: User) -> None:
    """Check whether the model is trained.

    Parameters:
    ----------
    user:
        User.
    """
    user_settings = UserSettings.objects.get(user=user)
    if not UserTrainingParameters.objects.filter(settings=user_settings):
        raise ModelsNotTrainedWarning


def save_models(user: Model, models: List[ModelPipeline]):
    """Saves models to database.

    Parameters:
    ----------
    user:
        User.
    models:
        Models pipelines.
    """
    user_settings = UserSettings.objects.get(user=user)
    for model in models:
        for model_name, model_obj in model.items():
            UserModels.objects.create(
                name=model_name,
                model=dumps(model_obj),
                settings=user_settings,
            )
