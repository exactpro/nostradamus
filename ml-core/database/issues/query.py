import os
import re

from datetime import datetime as dt
from typing import Optional, Dict, List, Any

from pandas import DataFrame
from pymongo import MongoClient

from database.issues.preprocessor import preprocess_df

MONGODB_HOST = os.environ.get("MONGODB_HOST", default="localhost")
MONGODB_PORT = int(os.environ.get("MONGODB_PORT", default=27017))
MONGODB_NAME = os.environ.get("MONGODB_NAME", default="issues")

CLIENT = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)

DB = CLIENT[MONGODB_NAME].bug


def build_query(
    filters: List[Dict[str, str]] = None, query: Dict[str, str] = None
) -> Dict[str, Dict[str, str]]:
    """Builds mongodb query.

    :param filters: Filters to be applied.
    :param query: MongoDB's native query.
    :return: Mongodb query.
    """

    def _build_filtration_conditions(
        filter_type: str, filter_value: Optional[str], exact_match: bool
    ) -> Optional[Dict[str, str]]:
        """Builds filtration conditions.

        :param filter_type: Filtration type.
        :param filter_value: Filter value.
        :param exact_match: Filtration option.
        :return: Filtration conditions.
        """
        query_field = {}

        if filter_type == "numeric":
            if filter_value[0] is not None:
                query_field["$gte"] = filter_value[0]
            if filter_value[1] is not None:
                query_field["$lte"] = filter_value[1]

        elif filter_type == "string":
            if exact_match:
                query_field = filter_value
            else:
                query_field["$regex"] = rf"{re.escape(filter_value)}"
                query_field["$options"] = "i"

        elif filter_type == "date":
            if filter_value[0] is not None:
                query_field["$gte"] = dt.strptime(
                    filter_value[0], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            if filter_value[1] is not None:
                query_field["$lte"] = dt.strptime(
                    filter_value[1], "%Y-%m-%dT%H:%M:%S.%f%z"
                )

        elif filter_type == "drop-down":
            if exact_match:
                filter_value = [rf"(?=.*?\b{value})" for value in filter_value]
                query_field["$regex"] = rf"^{''.join(filter_value)}.*"
            else:
                query_field["$regex"] = rf"^.*\b({'|'.join(filter_value)}).*"

        return query_field

    def _build_find_query() -> Dict[str, Dict[str, str]]:
        """Builds query for received filters.

        :return: Query.
        """
        query_ = {}
        for filter_ in filters:
            if filter_.get("current_value"):
                query_[filter_["name"]] = _build_filtration_conditions(
                    filter_["type"],
                    filter_["current_value"],
                    filter_["exact_match"],
                )
        return query_

    if filters:
        query = _build_find_query()
    query = query if query else {}

    return query


def get_issues(
    fields: List[str] = None,
    filters: List[Dict[str, str]] = None,
    query: Dict[str, Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """Query bugs from the db with specific conditions.

    :param fields: Issue fields.
    :param filters: Filters to be applied.
    :param query: MongoDB's native query.
    :return: Bugs.
    """
    fields = {field: 1 for field in fields} if fields else None
    if fields:
        fields["_id"] = 0
    else:
        fields = {"_id": 0}

    query = build_query(filters, query)

    issues = DB.find(query, fields)
    return [issue for issue in issues]


def get_issues_dataframe(
    fields: List[str] = None, filters: List[Dict[str, str]] = None
) -> DataFrame:
    """Converts issues to optimized pandas dataframe.

    :param fields: Issue fields.
    :param filters: Filters to be applied.
    :return: Optimized issues.
    """
    issues = DataFrame(get_issues(fields=fields, filters=filters))

    return preprocess_df(issues)
