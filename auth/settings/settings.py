from database import Base

DEFAULT_FILTERS = [
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

DEFAULT_PREDICTIONS_TABLE_COLUMNS = [
    "Issue Key",
    "Priority",
    "Area of Testing",
    "Time to Resolve",
    "Summary",
]


async def init_filters(model: Base, settings_id: int) -> None:
    """Creates a default filters settings.

    :param model: Metaclass of table.
    :param settings_id: User settings id.
    """

    for filter_ in DEFAULT_FILTERS:
        await model(
            name=filter_["name"],
            type=filter_["type"],
            settings_id=settings_id,
        ).create()


async def init_predictions_table(model: Base, settings_id: int) -> None:
    """Creates a default predictions table settings.

    :param model: Metaclass of table.
    :param settings_id: User settings id.
    """

    for position, name in enumerate(DEFAULT_PREDICTIONS_TABLE_COLUMNS, 1):
        await model(
            name=name,
            is_default=True,
            position=position,
            settings_id=settings_id,
        ).create()
