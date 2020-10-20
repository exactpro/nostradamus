import concurrent.futures
from pathlib import Path
from typing import List

import pandas as pd
import numpy as np

from django.db.models import Model

from apps.settings.main.archiver import get_archive_path, read_from_archive
from apps.settings.main.common import (
    get_qa_metrics_settings,
    get_predictions_table_settings,
)
from utils.const import (
    TRAINING_PARAMETERS_FILENAME,
    UNRESOLVED_BUGS_FILTER,
    MANDATORY_FIELDS,
)
from apps.authentication.models import User
from apps.extractor.main.preprocessor import get_issues_dataframe
from utils.predictions import get_probabilities

# Required for areas of testing prediction.
BINARY_CLASSES = [0, 1]

# Resolution predictions will be mapped separately.
PREDICTIONS_TABLE_FIELD_MAPPING = {
    "Issue Key": "Key",
    "Area of Testing": "areas_of_testing_prediction",
    "Time to Resolve": "Time to Resolve_prediction",
}


def get_predictions_table(
    issues, fields_settings, offset, limit
) -> pd.DataFrame:
    """Reads issues predictions for according user settings.

    Parameters:
    ----------
    issues:
        Bug reports.
    fields_settings:
        Predictions table fields settings.
    offset:
        Start index to read bugs.
    limit:
        Count of rows to be read.

    Returns:
    ----------
        Predictions.
    """
    if offset is not None and limit is not None:
        issues = paginate_bugs(issues, offset, limit)

    for field in fields_settings:
        if field.startswith("Resolution:"):
            class_ = field.replace("Resolution: ", "")

            issues[field] = issues["Resolution_prediction"].apply(
                lambda value: max(value.get(class_), key=value.get(class_).get)
            )
        else:
            issues[field] = issues[
                PREDICTIONS_TABLE_FIELD_MAPPING.get(field, field)
            ].apply(
                lambda value: max(value, key=value.get)
                if isinstance(value, dict)
                else value
            )

    issues = issues[fields_settings]

    return issues


def get_predictions(user: User, issues: pd.DataFrame) -> pd.DataFrame:
    """Appends predictions for each issue.

    Parameters:
    ----------
    user:
        User instance.
    issues:
        Bug reports.

    Returns:
    ----------
        Issues dataframe with predictions.
    """
    chunks = issues.groupby(np.arange(len(issues)) // 1000)

    archive_path = get_archive_path(user)
    training_parameters = read_from_archive(
        archive_path, TRAINING_PARAMETERS_FILENAME
    )
    models = load_models(params=training_parameters, models_path=archive_path)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        df_predictions = {
            executor.submit(
                calculate_predictions, chunk, training_parameters, models
            )
            for ind, chunk in chunks
        }
        predictions = pd.concat(
            [
                prediction.result()
                for prediction in concurrent.futures.as_completed(
                    df_predictions
                )
            ]
        )

        return predictions


def load_models(params: dict, models_path: Path) -> dict:
    """Read models.

    Parameters:
    ----------
    params:
        Training parameters.
    models_path:
        Path to models storage.

    Returns:
    ----------
        Object containing models' pipelines.
    """
    models = {}
    for param in params:
        if param in ["Time to Resolve", "Priority"]:
            models[param] = read_from_archive(models_path, param + ".sav")
        elif param == "Resolution":
            models[param] = {
                class_: read_from_archive(models_path, class_ + ".sav")
                for class_ in params[param]
            }
        elif param == "areas_of_testing":
            models[param] = {
                class_: read_from_archive(models_path, class_ + ".sav")
                for class_ in params[param]
            }
    return models


def calculate_predictions(
    issues: pd.DataFrame, training_parameters: dict, models: dict
) -> pd.DataFrame:
    """Calculates predictions for received DataFrame and writes them to the DB.

    Parameters:
    ----------
    issues:
        Bug reports.
    training_parameters:
        Training parameters.
    models:
        Models' pipelines.

    Returns:
    ----------
        Predictions.
    """
    for parameter in training_parameters:
        if parameter == "Time to Resolve":
            issues[parameter + "_prediction"] = issues["Description_tr"].apply(
                lambda descr: get_probabilities(
                    descr,
                    training_parameters[parameter],
                    models[parameter],
                )
            )
        elif parameter == "Resolution":
            issues[parameter + "_prediction"] = issues["Description_tr"].apply(
                lambda descr: calculate_resolution_predictions(
                    descr, training_parameters[parameter], models[parameter]
                )
            )
        elif parameter == "areas_of_testing":
            issues[parameter + "_prediction"] = issues["Description_tr"].apply(
                lambda descr: calculate_area_of_testing_predictions(
                    descr, training_parameters[parameter], models[parameter]
                )
            )

    return issues


def calculate_resolution_predictions(
    text: str, classes: dict, models: dict
) -> dict:
    """Calculates predictions for defect resolutions.

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
        parameter: get_probabilities(text, classes, models[parameter])
        for parameter, classes in classes.items()
    }
    return prediction


def calculate_area_of_testing_predictions(
    text: str, classes: list, models: dict
) -> dict:
    """Calculates area of testing predictions.

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
            models[parameter],
        )[1]
        for parameter in classes
    }
    return prediction


def paginate_bugs(df: pd.DataFrame, offset: int, limit: int) -> pd.DataFrame:
    return df.iloc[offset : offset + limit]


def get_qa_metrics_fields(user: Model) -> list:
    """Append values for drop-down fields.

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


def get_predictions_table_fields(user: User) -> list:
    """Reads predictions table settings from db.

    Parameters:
    ----------
    user:
        User instance.

    Returns:
    ----------
        Predictions table fields.
    """
    predictions_table_settings = get_predictions_table_settings(user)
    predictions_table_fields = [
        field["name"] for field in predictions_table_settings
    ] + ["Description_tr", "Key"]

    return predictions_table_fields


def calculate_issues_predictions(
    user: User, fields: List[str], filters: List[dict]
) -> pd.DataFrame:
    """Appends predictions to issues.

    Parameters:
    ----------
    user:
        User instance.
    fields:
        Predictions table fields.
    filters:
        Filters.

    Returns:
    ----------
        Issues.
    """
    filters = [UNRESOLVED_BUGS_FILTER] + filters

    issues = get_issues_dataframe(fields=fields, filters=filters)

    if issues.empty:
        return pd.DataFrame()

    issues = get_predictions(user, issues)

    return issues
