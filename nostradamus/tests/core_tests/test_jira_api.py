import pytest
import unittest
import pandas as pd

from apps.extractor.main.jira_api import JAPI


@pytest.mark.usefixtures("JQL")
class TestJiraAPI(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def init(self, request) -> None:
        self.Jira = JAPI(
            base_jql=self.JQL,
        )

    def test_get_extractor_args(self):
        larges_key = []
        request_args = self.Jira.get_extract_args(larges_key)

        assert all(
            [
                request_args[0][0] == f"{self.JQL} ORDER BY project, key ASC",
                request_args[0][1] == 0,
                request_args[0][2] == 1000,
                request_args[1][0] == f"{self.JQL} ORDER BY project, key ASC",
                request_args[1][1] == 1000,
                request_args[1][2] == 1000,
                request_args[2][0] == f"{self.JQL} ORDER BY project, key ASC",
                request_args[2][1] == 2000,
                request_args[2][2] == 1000,
            ]
        )

    def test_parse_issues_positive(self):
        issues = self.Jira.execute_jql(jql=self.JQL, step_size=1)

        assert (
            len(
                pd.DataFrame.from_records(
                    self.Jira.parse_issues(issues)
                ).keys()
            )
            != 0
        )

    def test_parse_issues_negative(self):
        issues = {
            "startAt": 0,
            "maxResults": 10,
            "total": 0,
            "issues": [],
        }

        assert not self.Jira.parse_issues(issues)

    def test_execute_jql_positive(self):
        assert self.Jira.execute_jql(self.JQL)["issues"]

    def test_execute_jql_negative(self):
        jql = 'issuetype = Bug AND priority = "Minor" AND assignee in (EMPTY) AND descrition = "ABCDEF"'

        assert not self.Jira.execute_jql(jql)["issues"]

    def test_get_step_in_execute_jql(self):
        request_args = self.Jira.get_extract_args([])

        steps = [request_arg[1] for request_arg in request_args]

        assert len(set(steps)) == len(steps)

    def test_get_update_args_positive(self):
        issues = self.Jira.execute_jql(jql=self.JQL, step_size=1)
        issues = self.Jira.parse_issues(issues)

        assert self.Jira.get_update_args(issues)

    def test_get_update_args_negative(self):
        issues = []

        assert not self.Jira.get_update_args(issues)
