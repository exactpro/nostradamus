import json

from base64 import b64encode
from pickle import dumps

import requests
from typing import Dict, List, Union

from imblearn.pipeline import Pipeline
from pandas import DataFrame, get_dummies, Series
from training.top_terms import calculate_top_terms
from models.User import User

TrainingParameters = Union[List[str], List[int], Dict[str, List[str]]]
ModelClasses = Dict[str, TrainingParameters]
ModelParams = List[Dict[str, Dict[str, int]]]
ModelPipeline = Dict[str, Pipeline]


SERVICE_URL = "nostradamus-core"
SERVICE_PORT = "8000"

BASE_ROUTE = "settings/training/"


def get_issues_fields(user: User) -> List[str]:
    """Get filter fields.

    :param user: User instance.
    :return: Filter fields.
    """
    response = requests.get(
        f"http://{SERVICE_URL}:{SERVICE_PORT}/{BASE_ROUTE}filters/",
        headers={"authorization": user.token},
    )
    issues_fields = response.json()["issues_fields"]
    return issues_fields


def get_bug_resolutions(user: User) -> List[Dict[str, str]]:
    """Get Bug Resolutions.

    :param user: User instance.
    :return: Bug resolutions.
    """
    response = requests.get(
        f"http://{SERVICE_URL}:{SERVICE_PORT}/{BASE_ROUTE}bug_resolution/",
        headers={"authorization": user.token},
    )
    bug_resolutions = response.json()["resolution_settings"]
    return bug_resolutions


def get_source_field(user: User) -> str:
    """Get Source Field.

    :param user: User instance.
    :return: Source Field.
    """
    response = requests.get(
        f"http://{SERVICE_URL}:{SERVICE_PORT}/{BASE_ROUTE}source_field/",
        headers={"authorization": user.token},
    )
    source_field = response.json()["source_field"]
    return source_field


def get_mark_up_entities(user: User) -> List[Dict[str, str]]:
    """Get Mark Up Entities.

    :param user: User instance.
    :return: Entities.
    """
    response = requests.get(
        f"http://{SERVICE_URL}:{SERVICE_PORT}/{BASE_ROUTE}markup_entities/",
        headers={"authorization": user.token},
    )
    mark_up_entities = response.json()["mark_up_entities"]
    return mark_up_entities


def save_top_terms(
    user: User,
    issues: DataFrame,
    resolutions: List[str],
    priorities: List[str],
    areas_of_testing: List[str],
):
    """Saves calculation results to database.

    :param user: User instance.
    :param issues: Bug reports.
    :param resolutions: Resolutions.
    :param priorities: Priorities derived after models' training.
    :param areas_of_testing: Areas of testing derived after models' training.
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
    ).to_json()

    requests.post(
        f"http://{SERVICE_URL}:{SERVICE_PORT}/{BASE_ROUTE}top_terms/",
        json={"top_terms": top_terms},
        headers={
            "authorization": user.token,
        },
    )


def save_models(user: User, raw_models: List[ModelPipeline]):
    """Saves models to database.

    :param user: User instance.
    :param raw_models: Models pipelines.
    """
    models = []
    for raw_model in raw_models:
        for model_name, model_obj in raw_model.items():
            models.append({"model_name": model_name, "model_obj": model_obj})

    # TODO: Rework model distribution
    requests.post(
        f"http://{SERVICE_URL}:{SERVICE_PORT}/{BASE_ROUTE}models/",
        data={"models": b64encode(dumps(models))},
        headers={
            "authorization": user.token,
        },
    )


def save_training_parameters(
    user: User,
    classes: ModelClasses,
    params: ModelParams,
) -> None:
    """Saves training parameters to the database.

    :param user: User instance.
    :param classes: classes.
    :param params: params for model.
    """
    training_settings = {}

    for class_ in classes:
        if class_ == "Resolution":
            training_settings["Resolution"] = {}
            resolution_settings = training_settings["Resolution"]
            for resolution in classes[class_]:
                resolution_settings[resolution] = [
                    "Not " + resolution,
                    resolution,
                ]
        else:
            training_settings[class_] = classes[class_]

    training_settings["model_params"] = params

    training_parameters = []
    for (
        training_settings_name,
        training_settings_value,
    ) in training_settings.items():
        training_parameters.append(
            {
                "name": training_settings_name,
                "training_parameters": json.dumps(training_settings_value),
            }
        )

    requests.post(
        f"http://{SERVICE_URL}:{SERVICE_PORT}/{BASE_ROUTE}training_parameters/",
        json={"training_parameters": training_parameters},
        headers={"authorization": user.token},
    )
