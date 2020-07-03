import multiprocessing
from pathlib import Path

import pandas as pd
import numpy as np

from math import ceil

from django.db.models import Model

from apps.settings.main.archiver import get_archive_path, read_from_archive
from apps.extractor.main.connector import get_issues, update_issues
from apps.extractor.models import Bug
from apps.settings.main.common import get_qa_metrics_settings
from utils.const import (
    TRAINING_PARAMETERS_FILENAME,
    BINARY_CLASSES,
    PREDICTIONS_TABLE_FIELD_MAPPING,
    PREDICTION_FIELDS,
    UNRESOLVED_BUGS_FILTER,
    MANDATORY_FIELDS,
)
from apps.authentication.models import User
from utils.predictions import get_probabilities
from utils.warnings import PredictionsNotReadyWarning


def get_predictions_table(settings, filters, offset, limit) -> pd.DataFrame:
    """ Reads bugs predictions for according user settings.

    Parameters:
    ----------
    settings:
        Predictions table settings.
    filters:
        Filters.
    offset:
        Start index to read bugs.
    limit:
        Count of rows to be read.

    Returns:
    ----------
        Bugs predictions.
    """
    filters = [UNRESOLVED_BUGS_FILTER] + filters

    bugs = pd.DataFrame(get_issues(filters=filters))

    if bugs.empty:
        return pd.DataFrame()

    if offset is not None and limit is not None:
        bugs = paginate_bugs(bugs, offset, limit)

    prediction_table_fields = [field["name"] for field in settings]

    for field in prediction_table_fields:
        if field.startswith("Resolution:"):
            class_ = field.replace("Resolution: ", "")

            bugs[field] = bugs["Resolution_prediction"].apply(
                lambda value: max(value.get(class_), key=value.get(class_).get)
            )
        else:
            bugs[field] = bugs[
                PREDICTIONS_TABLE_FIELD_MAPPING.get(field, field)
            ].apply(
                lambda value: max(value, key=value.get)
                if isinstance(value, dict)
                else value
            )

    bugs = bugs[prediction_table_fields]

    return bugs


def append_predictions(user: User) -> None:
    """ Appends predictions for each issue.

    Parameters:
    ----------
    user:
        User instance.
    """

    bugs = pd.DataFrame(
        get_issues(
            fields=["Key", "Description_tr"], filters=[UNRESOLVED_BUGS_FILTER]
        )
    )

    # Split DF to process its chunks asynchronously.
    chunk_size = ceil(len(bugs) / multiprocessing.cpu_count())

    archive_path = get_archive_path(user)
    training_parameters = read_from_archive(
        archive_path, TRAINING_PARAMETERS_FILENAME
    )

    with multiprocessing.Pool() as pool:
        df_predictions = [
            pool.apply_async(
                calculate_predictions,
                args=(chunk, training_parameters, archive_path),
            )
            for chunk in np.array_split(bugs, chunk_size)
        ]

        df_predictions = [prediction.get() for prediction in df_predictions]

    df_predictions = pd.concat(df_predictions)
    del df_predictions["Description_tr"]

    update_issues(df_predictions.T.to_dict().values())


def calculate_predictions(
    df: pd.DataFrame, training_parameters: dict, archive_path: Path
) -> pd.DataFrame:
    """ Calculates predictions for received DataFrame.

    Parameters:
    ----------
    df:
        Bugs.
    training_parameters:
        Training parameters.
    archive_path:
        Path to user archive.

    Returns:
    ----------
        DataFrame with calculated predictions.
    """
    for parameter in training_parameters:
        if parameter == "Time to Resolve":
            df[parameter + "_prediction"] = df["Description_tr"].apply(
                lambda descr: get_probabilities(
                    descr,
                    training_parameters[parameter],
                    read_from_archive(archive_path, parameter + ".sav"),
                )
            )
        elif parameter == "Resolution":
            df[parameter + "_prediction"] = df["Description_tr"].apply(
                lambda descr: calculate_resolution_predictions(
                    descr, training_parameters[parameter], archive_path
                )
            )
        elif parameter == "areas_of_testing":
            df[parameter + "_prediction"] = df["Description_tr"].apply(
                lambda descr: calculate_area_of_testing_predictions(
                    descr, training_parameters[parameter], archive_path
                )
            )

    return df


def calculate_resolution_predictions(
    text: str, classes: list, archive_path: Path
) -> dict:
    """ Calculates predictions for defect resolutions.

    Parameters:
    ----------
    text:
        Bug description.
    classes:
        Model's classes.
    archive_path:
        Path to user archive.

    Returns:
    ----------
        Calculated predictions.
    """
    prediction = {
        parameter: get_probabilities(
            text, classes, read_from_archive(archive_path, parameter + ".sav")
        )
        for parameter, classes in classes.items()
    }
    return prediction


def calculate_area_of_testing_predictions(
    text: str, classes: list, archive_path: Path
) -> dict:
    """ Calculates area of testing predictions.

    Parameters:
    ----------
    text:
        Bug description.
    classes:
        Model's classes.
    archive_path:
        Path to user archive.

    Returns:
    ----------
        Calculated predictions.
    """
    prediction = {
        parameter: get_probabilities(
            text,
            BINARY_CLASSES,
            read_from_archive(archive_path, parameter + ".sav"),
        )[1]
        for parameter in classes
    }
    return prediction


def paginate_bugs(df: pd.DataFrame, offset: int, limit: int) -> pd.DataFrame:
    return df.iloc[offset : offset + limit]


def delete_old_predictions() -> None:
    """ Deletes old bugs predictions.

    Parameters:
    ----------
    bugs:
        Bugs.
    path_to_saving:
        Path to where file will be saved.
    """
    fields = {"unset__" + field_name: True for field_name in PREDICTION_FIELDS}
    Bug.objects.update(**fields)


def check_predictions() -> None:
    """ Raises warning if predictions haven't been written yet.
    """
    query = {"exists__" + field_name: True for field_name in PREDICTION_FIELDS}
    result = [issues for issues in Bug.objects._collection.find(query)]
    if not result:
        raise PredictionsNotReadyWarning


def get_qa_metrics_fields(user: Model) -> list:
    """ Append values for drop-down fields.

    Parameters:
    ----------
    user:
        User instance.

    Returns:
    ----------
        Filled QA Metrics filters.
    """
    filters = get_qa_metrics_settings(user)

    fields = [filter_["name"] for filter_ in filters]
    fields = list(set(fields).union(set(MANDATORY_FIELDS)))

    return fields
