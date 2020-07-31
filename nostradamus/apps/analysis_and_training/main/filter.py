import pandas as pd

from django.db.models import Model
from apps.settings.main.common import get_filter_settings, split_values
from utils.const import MANDATORY_FIELDS


def update_drop_down_fields(filters: list, issues: pd.DataFrame) -> list:
    """ Append values for drop-down fields.

    Parameters:
    ----------
    filters:
        List of filters
    issues:
        Issues data used as filters.

    Returns:
    ----------
        Updated filters.
    """

    def _clean_empty(values: list) -> list:
        return [value for value in values if value != "" and value is not None]

    for filter_ in filters:
        if filter_["filtration_type"] == "drop-down":
            issues[filter_["name"]] = issues[filter_["name"]].astype(
                "category"
            )
            filter_["values"] = list(
                split_values(
                    _clean_empty(
                        issues[filter_["name"]].dropna().unique().tolist()
                    )
                    if filter_["name"] in issues.columns
                    else []
                )
            )

    return filters


def get_filters(user: Model, issues: pd.DataFrame) -> list:
    """ Reads filters settings from db.

    Parameters:
    ----------
    user:
        User instance.
    issues:
        Bug reports.

    Returns:
    ----------
        User filters.
    """
    filters = get_filter_settings(user)
    filters = update_drop_down_fields(filters=filters, issues=issues)
    for filter_ in filters:
        filter_["current_value"] = []
        filter_["exact_match"] = False
    return filters


def get_issues_fields(user: Model) -> list:
    """ Reads filter settings and makes fields list for issues
    uploading.

    Parameters:
    ----------
    user:
        User instance.

    Returns:
    ----------
        Issues fields.
    """
    filters = get_filter_settings(user)

    fields = [filter_["name"] for filter_ in filters]
    fields = list(set(fields).union(set(MANDATORY_FIELDS)))

    return fields
