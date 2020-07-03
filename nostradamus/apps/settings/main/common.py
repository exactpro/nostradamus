import pickle

from django.db.models import Model, Max

from apps.settings.main.archiver import (
    get_archive_path,
    read_from_archive,
    update_training_config,
    delete_training_data,
)
from utils.const import (
    DEFAULT_PREDICTIONS_TABLE_FIELDS,
    TRAINING_SETTINGS_FILENAME,
)
from utils.exceptions import (
    IncorrectPredictionsTableOrder,
    NotFilledDefaultFields,
)


def init_filters(model: Model, settings: Model) -> None:
    """ Creates a default filters settings.

    Parameters:
    ----------
    model:
        Object for which settings will be creating.
    settings:
        Link to user or team settings.
    """
    filters = [
        {"name": "Project", "filtration_type": "drop-down"},
        {"name": "Attachments", "filtration_type": "numeric"},
        {"name": "Priority", "filtration_type": "drop-down"},
        {"name": "Resolved", "filtration_type": "date"},
        {"name": "Labels", "filtration_type": "string"},
        {"name": "Created", "filtration_type": "date"},
        {"name": "Comments", "filtration_type": "numeric"},
        {"name": "Status", "filtration_type": "drop-down"},
        {"name": "Key", "filtration_type": "drop-down"},
        {"name": "Summary", "filtration_type": "string"},
        {"name": "Resolution", "filtration_type": "drop-down"},
        {"name": "Description", "filtration_type": "string"},
        {"name": "Components", "filtration_type": "string"},
    ]
    for filter_ in filters:
        model.objects.create(
            name=filter_["name"],
            filtration_type=filter_["filtration_type"],
            settings=settings,
        )


def init_predictions_table(model: Model, settings: Model) -> None:
    """ Creates a default predictions table settings.

    Parameters:
    ----------
    model:
        Object for which settings will be creating.
    settings:
        Link to user or team settings.
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


def init_training_settings() -> bytes:
    """ Creates a default training settings.
    """
    data = {"mark_up_source": "", "mark_up_entities": [], "bug_resolution": []}
    return pickle.dumps(data)


def read_settings(request_data: list, user: Model) -> None:
    """ Reads settings and appends it to request.

    Parameters:
    ----------
    request_data:
        Django request.data object.
    user:
        User instance.
    """

    # To avoid a circular dependency
    from apps.settings.models import UserSettings

    user_settings = UserSettings.objects.get(user=user).id
    for obj in request_data:
        obj["settings"] = user_settings


def get_training_settings(user: Model) -> dict:
    """ Prepares training settings data for serializing.

    Parameters:
    ----------
    user:
        User instance.

    Returns:
    ----------
        Training settings with path to user archive.
    """
    training_settings_path = get_archive_path(user)
    training_settings = read_from_archive(
        training_settings_path, TRAINING_SETTINGS_FILENAME
    )

    return training_settings


def update_predictions_table(
    model: Model, settings: int, fields: list
) -> None:
    """ Updates predictions table settings.

    Parameters:
    ----------
    model:
        User/Team model object.
    settings:
        Settings identifier.
    fields:
        List of predictions table fields.
    """

    def _validate_default_fields() -> None:
        """ Checks that all default fields exist.
        """
        default_fields = [
            field
            for field in fields
            if field["name"] in DEFAULT_PREDICTIONS_TABLE_FIELDS
        ]
        if len(DEFAULT_PREDICTIONS_TABLE_FIELDS) != len(default_fields):
            raise NotFilledDefaultFields

    def _validate_positions():
        """ Checks that there are no duplicated positions.
        """
        positions = set([field["position"] for field in fields])
        if len(positions) != len(fields):
            raise IncorrectPredictionsTableOrder

    _validate_default_fields()
    _validate_positions()

    model.objects.filter(settings_id=settings).delete()

    for field in fields:
        model.objects.create(settings_id=settings, **field)


def update_training_settings(training_settings: dict, user: Model) -> None:
    """ Updates training settings.

    Parameters:
    ----------
    training_settings:
        Training settings.
    user:
        User instance
    """

    def _parse() -> None:
        """ Parses objects with nested objects.
        """
        for obj in training_settings:
            if isinstance(obj, list):
                training_settings[obj] = [dict(value) for value in obj]

    def _check_by_changing():
        """ Checks that training data hasn't been edited.
        """
        current_settings = read_from_archive(
            archive_path, TRAINING_SETTINGS_FILENAME
        )

        is_changed = False

        for key, obj in current_settings.items():
            if key == "mark_up_source":
                if obj != training_settings[key]:
                    is_changed = True
                    break
            elif key == "bug_resolution":
                current_metrics = {resolution["value"] for resolution in obj}
                new_metrics = {
                    resolution["value"]
                    for resolution in training_settings["bug_resolution"]
                }
                if current_metrics.difference(new_metrics):
                    is_changed = True
                    break
            else:
                old_areas_of_testing = {
                    entity["area_of_testing"]: entity["entities"]
                    for entity in obj
                }
                new_areas_of_testing = {
                    entity["area_of_testing"]: entity["entities"]
                    for entity in training_settings[key]
                }
                for iteration, key_ in enumerate(old_areas_of_testing, 1):
                    if key_ not in new_areas_of_testing or set(
                        old_areas_of_testing[key_]
                    ).difference(set(new_areas_of_testing[key_])):
                        is_changed = True
                        break

        if is_changed:
            delete_training_data(archive_path)

    _parse()

    archive_path = get_archive_path(user)
    training_data = pickle.dumps(training_settings)

    _check_by_changing()
    update_training_config(archive_path, training_data)


def get_filter_settings(user: Model) -> list:
    """ Reads filter settings.

    Parameters:
    ----------
    user:
        User instance.

    Returns:
    ----------
        Filter settings.
    """

    # To avoid a circular dependency
    from apps.settings.models import UserSettings, UserFilter
    from apps.settings.serializers import UserFilterSerializer

    user_settings = UserSettings.objects.get(user=user)
    filter_settings = UserFilter.objects.filter(settings=user_settings)

    settings_data = UserFilterSerializer(filter_settings, many=True).data

    return settings_data


def get_qa_metrics_settings(user: Model) -> list:
    """ Reads QA Metrics settings.

    Parameters:
    ----------
    user:
        User instance.

    Returns:
    ----------
        QA metrics settings.
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


def get_predictions_table_settings(user: Model) -> list:
    """ Reads predictions table settings.

    Parameters:
    ----------
    user:
        User instance.

    Returns:
    ----------
        Predictions table settings.
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


def update_resolutions(request_data: dict, user: Model) -> None:
    """ Appends resolutions to predictions_table settings
    if their were not added.

    Parameters:
    ----------
    request_data:
        Django request.data object.
    user:
        User instance
    """

    def _delete_old_resolutions(old_resolutions) -> None:
        """ Deletes resolution from predictions_table
        if it's not specified in training settings.

        Parameters:
        ----------
        old_resolutions:
            Resolutions from predictions_table settings.
        """

        for resolution in old_resolutions:
            UserPredictionsTable.objects.filter(
                settings=user_settings, name=resolution
            ).delete()

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
