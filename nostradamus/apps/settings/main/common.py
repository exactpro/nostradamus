from json import loads, dumps
from typing import Dict, List, Union

from django.db.models import Model, Max
from rest_framework.serializers import Serializer
from imblearn.pipeline import Pipeline

from apps.analysis_and_training.main.significant_terms import (
    MarkUpEntities,
    BugResolutions,
)
from apps.extractor.main.connector import get_issue_count

from utils.const import DEFAULT_PREDICTIONS_TABLE_FIELDS
from utils.exceptions import (
    IncorrectPredictionsTableOrder,
    NotFilledDefaultFields,
)
from utils.warnings import BugsNotFoundWarning

from itertools import chain

ModelParams = List[Dict[str, Dict[str, int]]]
TrainingParameters = Union[List[str], List[int], Dict[str, List[str]]]
ModelClasses = Dict[str, TrainingParameters]
ModelPipeline = Dict[str, Pipeline]


def init_filters(model: Model, settings: Model) -> None:
    """Creates a default filters settings.

    :param model: Object for which settings will be creating.
    :param settings: Link to user settings.
    :return:
    """
    filters = [
        {"name": "Project", "type": "drop-down"},
        {"name": "Attachments", "type": "numeric"},
        {"name": "Priority", "type": "drop-down"},
        {"name": "Resolved", "type": "date"},
        {"name": "Labels", "type": "string"},
        {"name": "Created", "type": "date"},
        {"name": "Comments", "type": "numeric"},
        {"name": "Status", "type": "drop-down"},
        {"name": "Key", "type": "drop-down"},
        {"name": "Summary", "type": "string"},
        {"name": "Resolution", "type": "drop-down"},
        {"name": "Description", "type": "string"},
        {"name": "Components", "type": "string"},
    ]
    for filter_ in filters:
        model.objects.create(
            name=filter_["name"],
            type=filter_["type"],
            settings=settings,
        )


def init_predictions_table(model: Model, settings: Model) -> None:
    """Creates a default predictions table settings.

    :param model: Object for which settings will be creating.
    :param settings: Link to user settings.
    """
    names = [
        "Issue Key",
        "Priority",
        "Area of Testing",
        "Time to Resolve",
        "Summary",
    ]

    for position, name in enumerate(names, 1):
        model.objects.create(
            name=name, is_default=True, position=position, settings=settings
        )


def read_settings(request_data: list, user: Model) -> None:
    """Reads settings and appends it to request.

    :param request_data: Django request.data object.
    :param user: User instance.
    """

    # To avoid a circular dependency
    from apps.settings.models import UserSettings

    user_settings = UserSettings.objects.get(user=user).id
    for obj in request_data:
        obj["settings"] = user_settings


def update_predictions_table(
    model: Model, settings: int, fields: List[Dict[str, str]]
) -> None:
    """Updates predictions table settings.

    :param model: User model object.
    :param settings: Settings identifier.
    :param fields: List of predictions table fields.
    """

    def _validate_default_fields() -> None:
        """Checks that all default fields exist."""
        default_fields = [
            field
            for field in fields
            if field["name"] in DEFAULT_PREDICTIONS_TABLE_FIELDS
        ]
        if len(DEFAULT_PREDICTIONS_TABLE_FIELDS) != len(default_fields):
            raise NotFilledDefaultFields

    def _validate_positions() -> None:
        """Checks that there are no duplicated positions."""
        positions = set([field["position"] for field in fields])
        if len(positions) != len(fields):
            raise IncorrectPredictionsTableOrder

    _validate_default_fields()
    _validate_positions()

    model.objects.filter(settings_id=settings).delete()

    for field in fields:
        model.objects.create(settings_id=settings, **field)


def get_filter_settings(user: Model) -> List[Dict[str, str]]:
    """Reads filter settings.

    :param user: User instance.
    :return: Filter settings.
    """

    # To avoid a circular dependency
    from apps.settings.models import UserSettings, UserFilter
    from apps.settings.serializers import UserFilterSerializer

    user_settings = UserSettings.objects.get(user=user)
    filter_settings = UserFilter.objects.filter(settings=user_settings)

    settings_data = UserFilterSerializer(filter_settings, many=True).data

    return settings_data


def get_qa_metrics_settings(user: Model) -> List[Dict[str, str]]:
    """Reads QA Metrics settings.

    :param user: User instance.
    :return: QA metrics settings.
    """

    # To avoid a circular dependency
    from apps.settings.models import UserSettings, UserQAMetricsFilter
    from apps.settings.serializers import UserQAMetricsFilterSerializer

    user_settings = UserSettings.objects.get(user=user)
    qa_metrics_settings = UserQAMetricsFilter.objects.filter(
        settings=user_settings
    )

    settings_data = UserQAMetricsFilterSerializer(
        qa_metrics_settings, many=True
    ).data

    return settings_data


def get_predictions_table_settings(user: Model) -> List[Dict[str, str]]:
    """Reads predictions table settings.

    :param user: User instance.
    :return: Predictions table settings.
    """

    # To avoid a circular dependency
    from apps.settings.models import UserSettings, UserPredictionsTable
    from apps.settings.serializers import UserPredictionsTableSerializer

    user_settings = UserSettings.objects.get(user=user)
    qa_metrics_settings = UserPredictionsTable.objects.filter(
        settings=user_settings
    )

    settings_data = UserPredictionsTableSerializer(
        qa_metrics_settings, many=True
    ).data

    return settings_data


def update_resolutions(request_data: Dict[str, str], user: Model) -> None:
    """Appends resolutions to predictions_table settings if their were not added.

    :param request_data: Django request.data object.
    :param user: User instance.
    """

    def _delete_old_resolutions(resolutions: List[str]) -> None:
        """Deletes resolution from predictions_table
        if it's not specified in training settings.

        Parameters:
        ----------
        old_resolutions:
            Resolutions from predictions_table settings.
        """
        for resolution in resolutions:
            UserPredictionsTable.objects.get(
                settings=user_settings, name=resolution
            ).delete()

    # To avoid a circular dependency
    from apps.settings.models import UserPredictionsTable
    from apps.settings.models import UserSettings

    user_settings = UserSettings.objects.get(user=user).id

    qa_metrics_resolutions = [
        field["name"]
        for field in request_data["predictions_table"]
        if field["name"].startswith("Resolution")
    ]

    training_resolutions = [
        ": ".join(resolution.values())
        for resolution in request_data.get("bug_resolution")
    ]

    diff = set(qa_metrics_resolutions).difference(set(training_resolutions))
    if diff:
        _delete_old_resolutions(diff)

    user_predictions_table = UserPredictionsTable.objects.filter(
        settings_id=user_settings
    )

    # reset starting index after changes in predictions
    position = 1
    for table in user_predictions_table:
        table.position = position
        table.save()

        position += 1

    for resolution in training_resolutions:
        if resolution not in qa_metrics_resolutions:
            UserPredictionsTable.objects.create(
                settings_id=user_settings,
                name=resolution,
                position=UserPredictionsTable.objects.filter(
                    settings_id=user_settings
                ).aggregate(Max("position"))["position__max"]
                + 1,
                is_default=True,
            )


def check_issues_exist() -> None:
    """Checks that database have issues. If it doesn't have issues then raises warning."""
    if not get_issue_count():
        raise BugsNotFoundWarning


def split_values(values: list) -> set:
    """Makes a set of unique elements.

    :param values: A list of values by a field from db.
    :return: Unique elements.
    """
    values = [
        [
            splitted_value
            for splitted_value in value.split(",")
            if splitted_value
        ]
        if isinstance(value, str)
        else value
        for value in values
        if value
    ]
    if values and isinstance(values[0], list):
        return set(chain(*values))

    return set(values)


def check_filters_equality(
    new_filters: List[Dict[str, str]], old_filters: List[Dict[str, str]]
) -> bool:
    """Compares new filters and cached filters.

    :param new_filters: Received filters.
    :param old_filters: Cached filters.
    :return: Equality of filters.
    """
    for new_filter in new_filters:
        for old_filter in old_filters:
            if new_filter["name"] == old_filter["name"]:
                if new_filter.get("current_value") != old_filter.get(
                    "current_value"
                ):
                    return False

    return True


def get_bug_resolutions(user: Model) -> BugResolutions:
    """Get Bug Resolutions from database.

    :param user: User instance.
    :return: Bug resolutions.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserSettings,
        UserBugResolution,
    )

    user_settings = UserSettings.objects.get(user=user)
    bug_resolutions = UserBugResolution.objects.filter(settings=user_settings)

    return [
        {"metric": bug_resolution.metric, "value": bug_resolution.value}
        for bug_resolution in bug_resolutions
    ]


def get_source_field(user: Model) -> str:
    """Get Source Field from database.

    :param user: User instance.
    :return: Source Field.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserSettings,
        UserSourceField,
    )

    user_settings = UserSettings.objects.get(user=user)
    source_field = ""
    if UserSourceField.objects.filter(settings=user_settings):
        source_field = UserSourceField.objects.get(settings=user_settings).name

    return source_field


def get_mark_up_entities(
    user: Model,
) -> MarkUpEntities:
    """Get Mark Up Entities from database.

    :param user: User instance.
    :return: Entities.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserSettings,
        UserMarkUpEntity,
    )

    user_settings = UserSettings.objects.get(user=user)
    mark_up_entities = UserMarkUpEntity.objects.filter(settings=user_settings)

    return [
        {
            "area_of_testing": mark_up_entity.name,
            "entities": loads(mark_up_entity.entities),
        }
        for mark_up_entity in mark_up_entities
    ]


def update_source_field(user: Model, source_field: Serializer) -> None:
    """Update Source Field in database.

    :param user: User instance.
    :param source_field: New Source Field.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserSettings,
        UserSourceField,
    )

    user_settings = UserSettings.objects.get(user=user)
    UserSourceField.objects.filter(settings=user_settings).delete()
    UserSourceField.objects.create(
        name=source_field.get("source_field"),
        settings=user_settings,
    )


def update_bug_resolutions(user: Model, bug_resolutions: Serializer) -> None:
    """Update Bug Resolutions in database.

    Parameters:
    ----------
    user:
        User.
    bug_resolutions:
        New Bug Resolutions.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserBugResolution,
        UserSettings,
    )

    user_settings = UserSettings.objects.get(user=user)
    UserBugResolution.objects.filter(settings=user_settings).delete()
    for bug_resolution in bug_resolutions:
        UserBugResolution.objects.create(
            metric=bug_resolution.get("metric"),
            value=bug_resolution.get("value"),
            settings=user_settings,
        )


def update_mark_up_entities(user: Model, mark_up_entities: Serializer) -> None:
    """Update Mark Up Entities in database.

    Parameters:
    ----------
    user:
        User.
    mark_up_entities:
        New Mark Up Entities.
    """
    # To avoid a circular dependency
    from apps.settings.models import (
        UserMarkUpEntity,
        UserSettings,
    )

    user_settings = UserSettings.objects.get(user=user)
    UserMarkUpEntity.objects.filter(settings=user_settings).delete()
    for mark_up_entity in mark_up_entities:
        UserMarkUpEntity.objects.create(
            name=mark_up_entity.get("area_of_testing"),
            entities=dumps(mark_up_entity.get("entities")),
            settings=user_settings,
        )
