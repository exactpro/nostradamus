import os
import pandas as pd

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django
from django.conf import settings

settings.MONGODB_NAME = "testdb"

django.setup()

import unittest
import pytest


from datetime import timedelta as td
from datetime import datetime as dt

from apps.analysis_and_training.main.filter import update_drop_down_fields
from apps.extractor.main.connector import get_issues, DB


@pytest.mark.usefixtures("default_filters")
class TestFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.__fill_testdb()

    @classmethod
    def tearDownClass(cls) -> None:
        DB.delete_many({})

    @classmethod
    def __fill_testdb(self):
        DB.insert_many(
            documents=[
                {
                    "Project": "Test Project",
                    "Attachments": 12,
                    "Priority": "Minor" if _ % 5 == 0 else "Major",
                    "Created": dt.now(),
                    "Resolved": dt.now(),
                    "Updated": dt.now(),
                    "Labels": "Test Label" if _ % 5 == 0 else "Nostra",
                    "Comments": 1,
                    "Status": "Open",
                    "Key": str(_),
                    "Summary": "Test Summary",
                    "Resolution": "Unresolved"
                    if _ % 3 == 0
                    else "Rejected"
                    if _ % 2 == 0
                    else "Done",
                    "Description": "Test Description",
                    "Description_tr": "Test Description_tr",
                    "ttr": 10,
                    "Markup": 1,
                    "Components": "Test components",
                    "Version": "Test Version",
                    "Assignee": "Test Assignee",
                    "Reporter": "Test Reporter",
                }
                for _ in range(100)
            ],
            ordered=False,
        )

    def test_up_drop_down_fields(self):
        new_filters = update_drop_down_fields(
            filters=self.default_filters, issues=pd.DataFrame(get_issues())
        )

        assert all(
            [
                new_filters[0]["values"][0] == "Test Project",
                set(new_filters[2]["values"]) == set(["Minor", "Major"]),
                new_filters[7]["values"][0] == "Open",
                set(new_filters[10]["values"])
                == set(["Rejected", "Unresolved", "Done"]),
            ]
        )

    def test_filter_priority_positive(self):
        filter = [
            {
                "name": "Priority",
                "type": "drop-down",
                "current_value": ["Minor"],
                "exact_match": False,
            },
        ]
        issues = get_issues(filters=filter)

        assert len(issues) == 20

    def test_filter_priority_negative(self):
        filter = [
            {
                "name": "Priority",
                "type": "drop-down",
                "current_value": ["Critical"],
                "exact_match": False,
            },
        ]
        issues = get_issues(filters=filter)

        assert not issues

    def test_filter_project_positive(self):
        filter = [
            {
                "name": "Project",
                "type": "drop-down",
                "current_value": ["Test Project"],
                "exact_match": False,
            },
        ]
        issues = get_issues(filters=filter)

        assert len(issues) == 100

    def test_filter_project_negative(self):
        filter = [
            {
                "name": "Project",
                "type": "drop-down",
                "current_value": ["Nostradamus"],
                "exact_match": False,
            },
        ]
        issues = get_issues(filters=filter)

        assert not issues

    def test_filter_resolution_positive(self):
        filter = [
            {
                "name": "Resolution",
                "type": "drop-down",
                "current_value": ["Rejected", "Unresolved"],
                "exact_match": False,
            },
        ]
        issues = get_issues(filters=filter)

        assert len(issues) == 67

    def test_filter_resolution_negative(self):
        filter = [
            {
                "name": "Resolution",
                "type": "drop-down",
                "current_value": ["Won't Do"],
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert not issues

    def test_filter_created_positive_left(self):
        filter = [
            {
                "name": "Created",
                "type": "date",
                "current_value": [
                    dt.strftime(
                        dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                    None,
                ],
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert len(issues) == 100

    def test_filter_created_negative_left(self):
        filter = [
            {
                "name": "Created",
                "type": "date",
                "current_value": [
                    dt.strftime(
                        dt.now() + td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                    None,
                ],
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert not issues

    def test_filter_created_positive_right(self):
        filter = [
            {
                "name": "Created",
                "type": "date",
                "current_value": [
                    None,
                    dt.strftime(
                        dt.now() + td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                ],
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert len(issues) == 100

    def test_filter_created_negative_right(self):
        filter = [
            {
                "name": "Created",
                "type": "date",
                "current_value": [
                    None,
                    dt.strftime(
                        dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                ],
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert not issues

    def test_filter_created_both_positive(self):
        filter = [
            {
                "name": "Created",
                "type": "date",
                "current_value": [
                    dt.strftime(
                        dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                    dt.strftime(
                        dt.now() + td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                ],
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert len(issues) == 100

    def test_filter_created_both_negative(self):
        filter = [
            {
                "name": "Created",
                "type": "date",
                "current_value": [
                    dt.strftime(
                        dt.now() + td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                    dt.strftime(
                        dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"
                    ),
                ],
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert not issues

    def test_filter_label_positive(self):
        filter = [
            {
                "name": "Labels",
                "type": "string",
                "current_value": "Test Label",
                "exact_match": False,
            }
        ]

        issues = get_issues(filters=filter)

        assert len(issues) == 20

    def test_filter_label_negative(self):
        filter = [
            {
                "name": "Labels",
                "type": "string",
                "current_value": "Nostra",
                "exact_match": False,
            }
        ]
        issues = get_issues(filters=filter)

        assert len(issues) == 80
