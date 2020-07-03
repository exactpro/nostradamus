from typing import List, Dict
from math import ceil
from datetime import datetime as dt

from jira import JIRA, JIRAError
from django.conf import settings

from apps.extractor.main.cleaner import clean_text
from utils.const import MAX_JIRA_BLOCK_SIZE, BASE_JQL
from apps.extractor.main.preprocessor import calculate_ttr
from utils.data_converter import get_utc_datetime
from utils.exceptions import NonexistentJiraUser, IncorrectJiraCredentials


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
        """ Creates connection object for communication
        with Jira REST API service

        Returns:
        ----------
            JIRA connection instance
        """
        credentials = (
            (self.username, self.password)
            if self.username and self.password
            else None
        )

        try:
            jira_connection = JIRA(
                options={"server": self.url},
                basic_auth=credentials,
                max_retries=3,
            )
        except JIRAError as exc:
            if exc.status_code == 401:
                raise NonexistentJiraUser

            raise IncorrectJiraCredentials

        return jira_connection

    def get_extract_args(self, largest_keys: list = None) -> List[tuple]:
        """ Generates arguments for REST API requests.

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

    def get_update_args(self, existing_issues: List[Dict]):
        """ Generates arguments for REST API requests.

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
        """ Request total issues amount

        Returns:
        ----------
            Total issues amount.
        """
        conn = self.__get_connection()

        return conn.search_issues(jql, maxResults=0, json_result=True)["total"]

    def __get_step(self, step: int, block_size: int):
        return step * block_size

    def execute_jql(
        self, jql: str, start: int = 0, step_size: int = 50
    ) -> dict:
        """ Executes JQL to fetch issues from bug-tracker

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
                    Extra information to fetch inside each resource
                startAt:
                    Index of the first issue to return
                maxResults:
                    Maximum number of issues to return
                total:
                    Loaded issues amount
                issues:
                    List containing loaded issues
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
        """ Parses issues

        Parameters:
        ----------
        issues_blocks:
            Object which contains information about loaded issues

        Returns:
        ----------
            List ob parsed issues
        """

        def _map_field_names(raw_issue: dict) -> None:
            """ Rename fields of loaded issues using mapper object

            Parameters:
            ----------
            raw_issue:
                Issue for rename fields

            Returns:
            ----------
                Issue with the renamed fields
            """
            for name in name_mapping:
                if name in raw_issue["fields"]:
                    raw_issue["fields"][name_mapping[name]] = raw_issue[
                        "fields"
                    ].pop(name)

        def _parse_issue(raw_issue: dict) -> dict:
            """ Parse issue raw object structure.

            Parameters:
            ----------
            raw_issue:
                Raw issue object to be parsed.

            Returns:
            ----------
                Returns object containing parsed issue attributes.
            """
            fields = raw_issue.get("fields")
            history = raw_issue.get("changelog").get("histories")

            parsed_issue = {
                "Project": fields["Project"].get("name")
                if fields.get("Project")
                else "" or "",
                "Attachments": len(fields.get("Attachment") or []),
                "Priority": fields["Priority"].get("name")
                if fields.get("Priority")
                else "" or "",
                "Resolved": get_utc_datetime(fields["Resolved"])
                if fields.get("Resolved")
                else None,
                "Updated": get_utc_datetime(fields["Updated"])
                if fields.get("Updated")
                else None,
                "Labels": ",".join(fields["Labels"] or ""),
                "Created": get_utc_datetime(fields["Created"]),
                "Comments": len(fields["Comment"].get("comments") or []),
                "Status": fields["Status"]["name"],
                "Key": raw_issue["key"] or "",
                "Summary": fields["Summary"] or "",
                "Resolution": fields["Resolution"].get("name", "Unresolved")
                if fields.get("Resolution")
                else "Unresolved",
                "Description": fields["Description"] or "",
                "Components": ",".join(
                    [component["name"] for component in fields["Component/s"]]
                ),
                "Version": ",".join([el["name"] for el in fields["Versions"]])
                if fields.get("Versions")
                else "",
                "Assignee": fields.get("Assignee").get("displayName")
                if fields.get("Assignee")
                else "" or "",
                "Reporter": fields.get("Reporter").get("displayName")
                if fields.get("Reporter")
                else "" or "",
                "History": [
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
                ],
            }

            parsed_issue["Description_tr"] = clean_text(
                parsed_issue["Description"]
            )
            parsed_issue["Time to Resolve"] = calculate_ttr(
                parsed_issue["Resolved"], parsed_issue["Created"]
            )

            for key in fields:
                if key not in parsed_issue:
                    parsed_issue[key] = str(fields[key])

            return parsed_issue

        name_mapping = issue_block.get("names")
        issues = []
        while issue_block["issues"]:
            issue = issue_block["issues"].pop()

            if name_mapping:
                _map_field_names(issue)

            issues.append(_parse_issue(issue))
        return issues
