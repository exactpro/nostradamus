import pickle
import json
from typing import List, Dict

from django.db.models import Model
from imblearn.pipeline import Pipeline
from pandas import DataFrame

from utils.warnings import ModelsNotTrainedWarning


def get_training_parameters(instance: Model) -> Dict[str, str]:
    """Get training parameters.

    :param instance: Instance of User model.
    :return: Training parameters of User from database.
    """
    # To avoid a circular dependency
    from apps.settings.models import UserSettings, UserTrainingParameters

    user_settings = UserSettings.objects.get(user=instance)
    user_training_parameters = UserTrainingParameters.objects.filter(
        settings=user_settings
    )
    return {
        params.name: json.loads(params.training_parameters)
        for params in user_training_parameters
    }


def check_training_models(user: Model) -> None:
    """Check whether the model is trained.

    :param user: User.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserSettings,
        UserTrainingParameters,
    )

    user_settings = UserSettings.objects.get(user=user)
    if not UserTrainingParameters.objects.filter(settings=user_settings):
        raise ModelsNotTrainedWarning


def remove_training_parameters(user: Model) -> None:
    """Remove existing Training Parameters.

    Parameters:
    ----------
    user:
        User.
    """
    # To avoid a circular dependency
    from apps.settings.models import UserTrainingParameters, UserSettings

    user_settings = UserSettings.objects.get(user=user)
    UserTrainingParameters.objects.filter(settings=user_settings).delete()


def save_training_parameters(
    user: Model,
    training_settings: List[Dict[str, str]],
) -> None:
    """Saves training parameters to the database.

    :param user: User
    :param training_settings: Training parameters.
    """
    from apps.settings.models import (
        UserSettings,
        UserTrainingParameters,
    )

    user_settings = UserSettings.objects.get(user=user)
    for setting in training_settings:
        UserTrainingParameters.objects.create(
            name=setting["name"],
            training_parameters=setting["training_parameters"],
            settings=user_settings,
        )


def get_top_terms(user: Model) -> DataFrame:
    """Get Top Terms from database.

    Parameters:
    ----------
    user:
        User.

    Returns:
    ----------
        Top Terms.
    """
    # To avoid a circular dependency
    from apps.settings.models import UserTopTerms, UserSettings

    user_settings = UserSettings.objects.get(user=user)

    return pickle.loads(
        UserTopTerms.objects.get(settings=user_settings).top_terms_object
    )


def save_top_terms(user: Model, top_terms: DataFrame):
    """Saves calculation results to database.

    :param user: User.
    :param top_terms: Top terms.
    """
    # To avoid a circular dependency
    from apps.settings.models import UserSettings, UserTopTerms

    user_settings = UserSettings.objects.get(user=user)
    UserTopTerms.objects.filter(settings=user_settings).delete()
    UserTopTerms.objects.create(
        top_terms_object=pickle.dumps(top_terms),
        settings=user_settings,
    )


def save_models(user: Model, models: List[Dict[str, Pipeline]]):
    """Saves models to database.

    Parameters:
    ----------
    user:
        User.
    models:
        Models pipelines.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserSettings,
        UserModels,
    )

    user_settings = UserSettings.objects.get(user=user)
    UserModels.objects.filter(settings=user_settings).delete()
    for model in models:
        UserModels.objects.create(
            name=model["model_name"],
            model=pickle.dumps(model["model_obj"]),
            settings=user_settings,
        )
