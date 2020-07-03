from zipfile import ZipFile
from multiprocessing import Pool
import pandas as pd
import numpy
from typing import List
from pathlib import Path

from pandas import qcut, get_dummies, Categorical
from sklearn import feature_selection
from sklearn.feature_selection import chi2, SelectKBest
from imblearn.pipeline import Pipeline
from pickle import dumps
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from django.db.models import Model

from apps.analysis_and_training.main.common import (
    get_stop_words,
    save_to_archive,
    check_required_percentage,
    get_models_dir,
    check_bugs_count,
)
from apps.authentication.models import User
from apps.settings.main.archiver import get_archive_path
from utils.const import TRAINING_PARAMETERS_FILENAME
from utils.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer
from utils.exceptions import (
    SmallNumberRepresentatives,
    LittleDataToAnalyze,
    ResolutionElementsMissed,
    InconsistentGivenData,
)
from utils.warnings import ModelsNotTrainedWarning


def compare_resolutions(df: pd.DataFrame, resolutions: list) -> set:
    """ Checks for difference between required resolutions and those that are present in df.
    
    Parameters:
    ----------
        df:
            Bug reports.
        resolutions:
            bugs resolution.
    Returns:
    ----------
        The difference between the required resolutions and those that are present in the dataframe.
    """
    return set(resolutions).difference(set(df.Resolution.unique()))


def get_k_neighbors(series: pd.Series) -> int:
    """ Calculates the number of k-nearest neighbors.
    
    Parameters:
    ----------
        series:
            data used for calculations.
    Returns:
    ----------
        number of k-nearest neighbors.
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


def stringify_ttr_intervals(intervals: List[pd.Interval]) -> str:
    """ Stringifies list of ttr intervals.
    
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
            for el in range(len(intervals) - 1)
        ]
        + [">" + str(intervals[len(intervals) - 1].left)]
    )


def filter_classes(
    df: pd.DataFrame, areas_of_testing: list, resolution: list
) -> dict:
    """ Filters out classes with inadequate percentage of representatives
    
    Parameters:
    ----------
        df:
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
        "Priority": df["Priority"].unique().tolist(),
        "Time to Resolve": df["Time to Resolve"].unique().tolist(),
    }

    filtered_classes = {}
    for metric in classes.keys():
        if metric == "areas_of_testing":
            filtered_classes[metric] = [
                el
                for el in classes[metric]
                if check_required_percentage(df[el], 1)
                and len(set(df[el])) != 1
            ]
        else:
            filtered_classes[metric] = sorted(
                [
                    el
                    for el in classes[metric]
                    if check_required_percentage(df[metric], el)
                    and len(set(df[metric])) != 1
                ]
            )
    return filtered_classes


def encode_series(df: pd.DataFrame) -> pd.DataFrame:
    """Encodes series classes.
    
    Parameters:
    ----------
        df:
            Bug reports.

    Returns:
    ----------
        Dataframe containing encoded series.
    """
    # TODO Investigation is required for imbalanced data
    df["Time to Resolve"] = qcut(
        df["Time to Resolve"].astype(int), q=4, duplicates="drop"
    )
    df["time to resolve_codes"] = df["Time to Resolve"].cat.rename_categories(
        range(len(df["Time to Resolve"].unique()))
    )

    df["priority_codes"] = Categorical(df["Priority"], ordered=True).codes

    df = df.reset_index(drop=True)
    series_resolution = df["Resolution"]
    df = get_dummies(df, columns=["Resolution"])
    df["Resolution"] = series_resolution

    return df


def train_imbalance(
    descr_series: pd.Series,
    classes_codes: pd.Series,
    TFIDF_,
    IMB_,
    FS_,
    req_percentage: int,
    CLF_,
    model_name: str,
) -> dict:
    """ Trains models using handled setting and saves them as .sav objects.

    Parameters:
    ----------
    instance:
        Instance of User model;
    descr_series:
        description series;
    classes_codes:
        series with classes' codes;
    TFIDF_:
        vectorizer;
    IMB_:
        SMOTE instance;
    FS_:
        ranking terms method;
    req_percentage:
        percentage to be taken from the ranked list;
    CLF_:
        classifier;
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
    clf_model.set_params(fs__percentile=req_percentage).fit(
        descr_series, classes_codes
    )

    return {model_name: clf_model}


def save_training_parameters(archive_path: Path, classes: dict):
    """ Saves training parameters to the config file.

    Parameters:
    ----------
    archive_path:
        Path to an archive.
    classes:
        classes.
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

    save_to_archive(
        archive_path, "training_parameters.pkl", dumps(training_settings)
    )


def train(
    instance: Model, df: pd.DataFrame, areas_of_testing: list, resolution: list
) -> dict:
    """ Train models.
    
    Parameters:
    ----------
    instance:
        Instance of User model;
    df:
        Bug reports;
    areas_of_testing:
        areas of testing;
    resolution:
        resolution.

    Returns:
    ----------
        Valid classes.
    """

    def _params_producer() -> tuple:
        """ Generates parameters for imbalance training.

        Returns:
        ----------
            Bugs description, classes codes, SMOTE instance and model name.
        """
        for metric in filtered_classes.keys():
            if metric == "Priority" or metric == "Time to Resolve":
                filtered_df = df[df[metric].isin(filtered_classes[metric])]
                smt = SMOTE(
                    ratio="minority",
                    random_state=0,
                    kind="borderline1",
                    n_jobs=4,
                )
                smt.k_neighbors = get_k_neighbors(
                    df[metric.lower() + "_codes"]
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
                    smt.k_neighbors = get_k_neighbors(df[df_index])

                    yield df.Description_tr, df[df_index], smt, class_

    df = df[
        (df["Resolution"] != "Unresolved")
        & (df["Resolved"].isna() is not True)
        & (df["Resolved"].notnull())
    ]
    df = df.reset_index()

    if not check_bugs_count(df):
        raise LittleDataToAnalyze

    df = encode_series(df)
    filtered_classes = filter_classes(df, areas_of_testing, resolution)

    # TODO: remove unnecessary resolution verification
    # when settings will be linked to data
    missing_resolutions = compare_resolutions(df, resolution)
    if missing_resolutions:
        raise ResolutionElementsMissed(
            f"Oops! These Resolution elements are missed: {missing_resolutions}. Models can't be trained."
        )

    filtered_resolutions = set(resolution).difference(
        set(filtered_classes.get("Resolution"))
    )
    if filtered_resolutions:
        raise ResolutionElementsMissed(
            f"Oops! These Resolution elements are missed: {filtered_resolutions}. Models can't be trained."
        )

    svm_imb = SVC(gamma=2, C=1, probability=True, class_weight="balanced")

    sw = get_stop_words(df)
    tfidf = StemmedTfidfVectorizer(stop_words=sw)

    try:
        with Pool() as pool:
            models = [
                pool.apply_async(
                    train_imbalance,
                    args=(
                        description,
                        classes,
                        tfidf,
                        smote,
                        chi2,
                        50,
                        svm_imb,
                        model_name,
                    ),
                )
                for description, classes, smote, model_name in _params_producer()
            ]
            models = [model.get() for model in models]
    except ValueError:
        raise InconsistentGivenData

    save_models(models, instance)

    filtered_classes["Time to Resolve"] = stringify_ttr_intervals(
        filtered_classes["Time to Resolve"]
    )
    filtered_classes["binary"] = [0, 1]

    save_training_parameters(get_models_dir(instance), filtered_classes)

    resolutions = [
        "Resolution_" + resol for resol in filtered_classes["Resolution"]
    ]
    save_top_terms(
        get_models_dir(instance),
        df,
        resolutions,
        filtered_classes["Priority"],
        filtered_classes["areas_of_testing"],
    )


def get_top_terms(df: pd.DataFrame, metric: str) -> dict:
    """ Calculates top terms.

    Parameters:
    ----------
    df:
        Bug reports.
    metric:
        Value which is used for calculations.

    Returns:
    ----------
        Object with calculated terms.
    """
    chi2 = feature_selection.chi2

    sw = get_stop_words(df)
    tfidf = StemmedTfidfVectorizer(stop_words=sw)
    tfs = tfidf.fit_transform(df["Description_tr"])

    y = df[metric]
    selector = SelectKBest(score_func=chi2, k="all")
    selector.fit_transform(tfs, y)
    return dict(zip(tfidf.get_feature_names(), selector.scores_))


def calculate_top_terms(df: pd.DataFrame, metric: str) -> list:
    """ Calculates top terms which are based on significance weights.

    Parameters:
    ----------
        df: 
            Bug reports;
        metric: 
            field which is used for calculation.

    Returns:
    ----------
        list of the calculated terms.

    """
    terms = get_top_terms(df, metric)

    terms = {k: v for (k, v) in terms.items() if v > 1}
    return [
        k for (k, v) in terms.items() if v > numpy.mean(list(terms.values()))
    ]


def save_top_terms(
    archive_path: Path,
    df: pd.DataFrame,
    resolutions: list,
    priorities: list,
    areas_of_testing: list,
):
    """ Saves calculation results as a .pkl to an archive.
    
    Parameters:
    ----------
        archive_path:
            Path to an archive;
        df: 
            Bug reports;
        resolutions: 
            resolutions;
        priorities: 
            priorities derived after models' training;
        areas_of_testing: 
            areas of testing derived after models' training.

    """
    binarized_df = pd.get_dummies(
        df, prefix=["Priority"], columns=["Priority"],
    )
    top_terms = {}

    metrics = (
        ["Priority_" + priority for priority in priorities]
        + resolutions
        + [area for area in areas_of_testing if area != "Other"]
    )

    for metric in metrics:
        top_terms[metric] = calculate_top_terms(binarized_df, metric)

    top_terms = pd.DataFrame(
        dict([(k, pd.Series(v)) for k, v in top_terms.items()])
    )

    save_to_archive(archive_path, "top_terms.pkl", dumps(top_terms))


def check_training_files(user: User) -> None:
    """ Raises warning if models don't exist.

    Parameters:
    ----------
    user:
        User instance.
    """
    archive_path = get_archive_path(user)
    with ZipFile(archive_path, "r") as archive:
        if TRAINING_PARAMETERS_FILENAME not in archive.namelist():
            raise ModelsNotTrainedWarning


def save_models(models: list, user: User) -> None:
    """ Appends models to archive.

    Parameters:
    ----------
    models:
        Trained models.
    user:
        User instance.
    """
    for model in models:
        for model_name, model_obj in model.items():
            save_to_archive(
                get_models_dir(user),
                "{}.sav".format(model_name),
                dumps(model_obj),
            )
