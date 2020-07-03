import re

from datetime import datetime as dt
from typing import Optional

from django.conf import settings
from mongoengine import connect
from pymongo import MongoClient, UpdateOne

from apps.extractor.consumers import ExtractorConsumer
from apps.extractor.models import Bug
from utils.redis import clear_cache

CLIENT = MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)

DB = CLIENT[settings.MONGODB_NAME].bug

connect(
    settings.MONGODB_NAME,
    host=settings.MONGODB_HOST,
    port=settings.MONGODB_PORT,
)


def get_issues(fields: list = None, filters: list = None) -> list:
    """ Query bugs from the db with specific conditions.

    Parameters
    ----------
    filters:
        Filters to be applied.
    fields:
        Issue fields.

    Returns
    -------
        Bugs.
    """

    def _build_filtration_conditions(
        f_type: str, f_value: Optional, exact_match: bool
    ) -> Optional:
        """ Builds filtration conditions.

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
                query_field["$regex"] = rf"{f_value}"
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
        """ Builds query for received filters.

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

    fields = {field: 1 for field in fields} if fields else None
    if fields:
        fields["_id"] = 0

    if filters:
        query = _build_find_query()
        issues = DB.find(query, fields)
        return [issue for issue in issues]

    issues = DB.find({}, fields)
    return [issue for issue in issues]


def get_largest_keys() -> list:
    """ Finds the largest issue keys.

    Returns
    -------
        Issue keys.
    """

    def _get_natural_number(issue_key) -> int:
        """ Converts issue key to a number.

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


def insert_issues(issues: list) -> None:
    """ Insert issues to database.

    Parameters
    ----------
    issues:
        Issues to be inserted.
    """
    if issues:
        DB.insert_many(documents=issues, ordered=False)

        clear_cache()

        ExtractorConsumer.loader_notification()


def update_issues(issues: list):
    """ Update issues in the db.

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

        clear_cache()

        ExtractorConsumer.loader_notification()


def get_issue_count():
    return Bug.objects.count()
