import configparser

from typing import List, Dict, Optional, Union
from math import ceil
from pathlib import Path

from jira import JIRA, JIRAError
from django.conf import settings

from apps.extractor.main.cleaner import clean_text
from apps.extractor.main.preprocessor import calculate_ttr
from apps.extractor.main.mapping import FUNCTION_MAPPING, REPLACE_MAPPING
from utils.data_converter import get_utc_datetime
from utils.exceptions import NonexistentJiraUser, IncorrectJiraCredentials


PARSE_CONF_FILENAME = "parse.conf"
CONFIG_PARSE = Path(__file__).parents[0].joinpath(PARSE_CONF_FILENAME)

# Jira limits response size to 1000 per request
MAX_JIRA_BLOCK_SIZE = 1000
BASE_JQL = "issuetype=BUG"


class JAPI:
    """
    Extract and parse JIRA issues.

    Attributes
    ----------
    url : str
        service URL.
    username : str
        JIRA user login name.
    password : str
        JIRA user password.
    base_jql : str
        service URL.

    Methods
    -------
        get_extract_args:
            Generates arguments for REST API requests.
        get_update_args:
            Generates arguments for REST API requests.
        execute_jql:
            Executes JQL to fetch issues from bug-tracker.
        parse_issues:
            Parses issues.
    """

    def __init__(
        self,
        url=settings.JIRA_URL,
        username=settings.JIRA_USERNAME,
        password=settings.JIRA_PASSWORD,
        base_jql=BASE_JQL,
    ):
        self.url = url
        self.username = username
        self.password = password
        self.base_jql = base_jql

    def __get_connection(self) -> JIRA:
        """Creates connection object for communication
        with Jira REST API service.

        Returns:
        ----------
            JIRA connection instance.
        """
        credentials = (
            (self.username, self.password)
            if self.username and self.password
            else None
        )

        try:
            jira_connection = JIRA(
                options={"server": self.url, "verify": False},
                basic_auth=credentials,
                max_retries=3,
            )
        except JIRAError as exc:
            if exc.status_code == 401:
                raise NonexistentJiraUser

            raise IncorrectJiraCredentials

        return jira_connection

    def get_extract_args(self, largest_keys: list = None) -> List[tuple]:
        """Generates arguments for REST API requests.

        Parameters:
        ----------
        largest_keys:
            The largest available issue-keys.

        Returns:
        ----------
            Request arguments.
        """

        def _form_extract_jql(keys: list):
            conditions = [f"(key > {key})" for key in keys]
            return (
                f"{self.base_jql} and ({' or '.join(conditions)}) ORDER BY project, key ASC"
                if keys
                else f"{self.base_jql} ORDER BY project, key ASC"
            )

        jql = _form_extract_jql(largest_keys)
        total_issues = self.__get_issues_amount(jql)
        block_size = MAX_JIRA_BLOCK_SIZE
        blocks_count = ceil(total_issues / block_size)

        request_args = [
            (jql, self.__get_step(el, block_size), block_size)
            for el in range(blocks_count)
        ]
        return request_args

    def get_update_args(self, existing_issues: List[Dict]) -> list:
        """Generates arguments for REST API requests.

        Parameters:
        ----------
        existing_issues:
            Issue keys and dates of updating.

        Returns:
        ----------
            Parsed issues.
        """

        def _form_update_jql(issues_data: List[Dict]):
            conditions = [
                f"(key = {issue.get('Key')} and updated > '{issue.get('Updated').strftime('%Y-%m-%d %H:%M')}')"
                for issue in issues_data
            ]
            return (
                f"{self.base_jql} and ({' or '.join(conditions)})"
                if issues_data
                else f"{self.base_jql}"
            )

        def _split_into_chunks(iterable: list, chunk_size: int = 50):
            for ind in range(0, len(iterable), chunk_size):
                yield iterable[ind : ind + chunk_size]

        existing_issues = _split_into_chunks(existing_issues)
        request_args = [_form_update_jql(chunk) for chunk in existing_issues]

        return request_args

    def __get_issues_amount(self, jql: str) -> int:
        """Request total issues amount.

        Returns:
        ----------
            Total issues amount.
        """
        conn = self.__get_connection()

        return conn.search_issues(jql, maxResults=0, json_result=True)["total"]

    def __get_step(self, step: int, block_size: int) -> int:
        return step * block_size

    def execute_jql(
        self, jql: str, start: int = 0, step_size: int = 50
    ) -> dict:
        """Executes JQL to fetch issues from bug-tracker.

        Parameters:
        ----------
        jql:
            JQL query.
        start:
            Index of the first issue to request.
        step_size:
            The number of elements to request.

        Returns:
        ----------
            Object that contains the following information:
                expand:
                    Extra information to fetch inside each resource.
                startAt:
                    Index of the first issue to return.
                maxResults:
                    Maximum number of issues to return.
                total:
                    Loaded issues amount.
                issues:
                    List containing loaded issues.
        """
        conn = self.__get_connection()
        return conn.search_issues(
            jql,
            startAt=start,
            maxResults=step_size,
            json_result=True,
            validate_query=False,
            expand="names,changelog",
            fields="*all",
        )

    @staticmethod
    def parse_issues(issue_block: dict) -> List[Dict]:
        """Parses issues.

        Parameters:
        ----------
        issues_blocks:
            Object which contains information about loaded issues.

        Returns:
        ----------
            List ob parsed issues.
        """

        def _get_value(
            path_values: list, raw_value: Optional, result=None
        ) -> Optional[Union[dict, str, List[str]]]:
            """Get values using values path.

            Parameters:
            ----------
            path_values:
                Path to values from config.
            raw_value:
                Value from raw issue.
            result:
                Parsed field value.

            Returns:
            ----------
                Parsed field value.
            """
            for path_piece in path_values:
                if isinstance(raw_value, list):
                    result = []
                    for field in raw_value:
                        result.append(
                            _get_value(
                                path_values[path_values.index(path_piece) :],
                                field,
                                result,
                            )
                        )
                    break
                elif isinstance(raw_value, (str, int, bool)):
                    return raw_value
                elif raw_value.get(path_piece) is not None:
                    raw_value = raw_value.get(path_piece)
                    result = raw_value

            return result

        def _map_field_names(raw_issue: dict) -> None:
            """Rename fields of loaded issues using mapper object.

            Parameters:
            ----------
            raw_issue:
                Issue for rename fields.

            Returns:
            ----------
                Issue with the renamed fields.
            """
            for name in name_mapping:
                if name in raw_issue["fields"]:
                    raw_issue["fields"][name_mapping[name]] = raw_issue[
                        "fields"
                    ].pop(name)

        def _parse_issue(raw_issue: dict) -> dict:
            """Parse issue raw object structure.

            Parameters:
            ----------
            raw_issue:
                Raw issue object to be parsed.

            Returns:
            ----------
                Returns object containing parsed issue attributes.
            """
            issue = raw_issue.get("fields")
            history = raw_issue.get("changelog").get("histories")
            parsed_issue = {}

            config_parser = configparser.ConfigParser()
            config_parser.read(CONFIG_PARSE)

            for new_field in config_parser["DEFAULT"]:
                new_field = new_field.capitalize()
                maps = config_parser["DEFAULT"][new_field].split(".")

                func = FUNCTION_MAPPING.get(new_field)
                value = (
                    _get_value(maps, issue[maps[0]])
                    if maps[0] in issue and issue[maps[0]] is not None
                    else None
                )
                if value is not None and func:
                    parsed_issue[new_field] = func(value)
                else:
                    parsed_issue[new_field] = (
                        value
                        if value is not None
                        else REPLACE_MAPPING[new_field]
                        if new_field in REPLACE_MAPPING.keys()
                        else ""
                    )

            parsed_issue["Key"] = raw_issue["key"] or ""
            parsed_issue["History"] = [
                {
                    "Author": snapshot.get("author").get("displayName")
                    if snapshot.get("author")
                    else "",
                    "Created": get_utc_datetime(snapshot.get("created"))
                    if snapshot.get("created")
                    else "",
                    "Items": [
                        {
                            "Field": item.get("field"),
                            "From": item.get("fromString"),
                            "To": item.get("toString"),
                        }
                        for item in snapshot.get("items")
                    ]
                    if snapshot.get("items")
                    else "",
                }
                for snapshot in history
            ]

            parsed_issue["Description_tr"] = clean_text(
                parsed_issue["Description"]
            )
            parsed_issue["Time to Resolve"] = calculate_ttr(
                parsed_issue["Resolved"], parsed_issue["Created"]
            )

            for key in issue:
                if key not in parsed_issue:
                    parsed_issue[key] = str(issue[key])

            return parsed_issue

        name_mapping = issue_block.get("names")
        issues = []
        while issue_block["issues"]:
            issue = issue_block["issues"].pop()

            if name_mapping:
                _map_field_names(issue)

            issues.append(_parse_issue(issue))

        return issues
