import re

from datetime import datetime as dt
from typing import Optional

from django.conf import settings
from pymongo import MongoClient, UpdateOne

from apps.extractor.consumers import ExtractorConsumer
from utils.redis import clear_cache

CLIENT = MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)

DB = CLIENT[settings.MONGODB_NAME].bug


def build_query(filters: list = None, query: dict = None) -> dict:
    """Builds mongodb query.

    Parameters
    ----------
    filters:
        Filters to be applied.
    query:
        MongoDB's native query.

    Returns
    -------
        Mongodb query.
    """

    def _build_filtration_conditions(
        f_type: str, f_value: Optional, exact_match: bool
    ) -> Optional:
        """Builds filtration conditions.

        Parameters:
        ----------
        f_type:
            Filtration type.
        f_value:
            Filter value.
        exact_match:
            Filtration option.

        Returns:
        ----------
            Filtration conditions.
        """
        query_field = {}

        if f_type == "numeric":
            if f_value[0] is not None:
                query_field["$gte"] = f_value[0]
            if f_value[1] is not None:
                query_field["$lte"] = f_value[1]

        elif f_type == "string":
            if exact_match:
                query_field = f_value
            else:
                query_field["$regex"] = rf"{re.escape(f_value)}"
                query_field["$options"] = "i"

        elif f_type == "date":
            if f_value[0] is not None:
                query_field["$gte"] = dt.strptime(
                    f_value[0], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            if f_value[1] is not None:
                query_field["$lte"] = dt.strptime(
                    f_value[1], "%Y-%m-%dT%H:%M:%S.%f%z"
                )

        elif f_type == "drop-down":
            if exact_match:
                f_value = [rf"(?=.*?\b{value})" for value in f_value]
                query_field["$regex"] = rf"^{''.join(f_value)}.*"
            else:
                query_field["$regex"] = rf"^.*\b({'|'.join(f_value)}).*"

        return query_field

    def _build_find_query() -> dict:
        """Builds query for received filters.

        Returns:
        -------
            Query
        """
        query_ = {}
        for filter_ in filters:
            if filter_.get("current_value"):
                query_[filter_["name"]] = _build_filtration_conditions(
                    filter_["filtration_type"],
                    filter_["current_value"],
                    filter_["exact_match"],
                )
        return query_

    if filters:
        query = _build_find_query()
    query = query if query else {}

    return query


def get_issues(
    fields: list = None, filters: list = None, query: dict = None
) -> list:
    """Query bugs from the db with specific conditions.

    Parameters:
    ----------
    fields:
        Issue fields.
    filters:
        Filters to be applied.
    query:
        MongoDB's native query.

    Returns:
    ----------
        Bugs
    """
    fields = {field: 1 for field in fields} if fields else None
    if fields:
        fields["_id"] = 0
    else:
        fields = {"_id": 0}

    query = build_query(filters, query)

    issues = DB.find(query, fields)
    return [issue for issue in issues]


def get_largest_keys() -> list:
    """Finds the largest issue keys.

    Returns
    -------
        Issue keys.
    """

    def _get_natural_number(issue_key) -> int:
        """Converts issue key to a number.

        Parameters
        ----------
        issue_key:
            Issue key.

        Returns
        -------
            Issue key as a number.
        """
        return int(re.split(r"(\d+)", issue_key)[1])

    issues = get_issues(fields=["Key", "Project"])
    keys = []
    if issues:
        projects = set(issue.get("Project") for issue in issues)
        for project in projects:
            filtered_issues = filter(
                lambda issue: issue.get("Project") == project, issues
            )
            max_key = max(
                filtered_issues,
                key=lambda x: _get_natural_number(x.get("Key")),
            )["Key"]
            keys.append(max_key)
        return keys
    return []


def update_issues(issues: list) -> None:
    """Update issues in the db.

    Parameters
    ----------
    issues:
        Updated issues.
    """
    if issues:
        requests = [
            UpdateOne(
                filter={"Key": issue["Key"]},
                update={"$set": issue},
                upsert=True,
            )
            for issue in issues
        ]
        DB.bulk_write(requests=requests, ordered=False)

        cache_keys = [
            "analysis_and_training:defect_submission",
            "analysis_and_training:records_count",
            "qa_metrics:predictions_page",
            "qa_metrics:predictions_table",
        ]
        clear_cache(cache_keys)

        ExtractorConsumer.loader_notification()


def get_issue_count(filters: list = None) -> int:
    """Get count bugs

    Parameters
    ----------
    filters:
        Filters to be applied.

    Returns
    -------
        Count bugs
    """
    query = build_query(filters)
    return DB.count_documents(query)


def get_fields() -> list:
    """Get unique field names from Bug document.

    Returns:
        Unique field names.
    """
    fields = [key for key in DB.find_one()]

    return fields


def get_unique_values(field: str) -> list:
    """Query unique values from the db by the field.

    Parameters
    ----------
    field:
        Issue field.

    Returns
    -------
        Unique values.
    """
    return DB.distinct(field)
