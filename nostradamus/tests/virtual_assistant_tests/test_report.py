import os

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django
from django.conf import settings

settings.MONGODB_NAME = "testdb"
settings.MONGODB_HOST = "127.0.0.1"

django.setup()

import unittest
import pytest

from datetime import datetime as dt
from datetime import timedelta as td
from apps.extractor.main.connector import DB
from apps.virtual_assistant.main.report_generator import (
    build_report_filters,
    get_issues_for_report,
)


@pytest.mark.usefixtures("report_fields")
class TestReport(unittest.TestCase):
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
                    "Created": dt.now()
                    if _ % 5 == 0
                    else dt.now() + td(days=5),
                    "Resolved": dt.now(),
                    "Updated": dt.now(),
                }
                for _ in range(100)
            ],
            ordered=False,
        )

    def test_build_report_filters_created(self):
        filters = build_report_filters(
            field="Created", period=("01-01-2000", "30-01-2000")
        )

        assert filters == [
            {
                "name": "Created",
                "filtration_type": "date",
                "current_value": ("01-01-2000", "30-01-2000"),
                "exact_match": True,
            }
        ]

    def test_build_report_filters_resolved(self):
        filters = build_report_filters(
            field="Resolved", period=("01-12-1980", "31-12-1980")
        )

        assert filters == [
            {
                "name": "Resolved",
                "filtration_type": "date",
                "current_value": ("01-12-1980", "31-12-1980"),
                "exact_match": True,
            }
        ]

    def test_get_issues_report(self):
        filters = build_report_filters(field="Created", period=())

        issues = get_issues_for_report(self.report_fields, filters)

        assert len(issues) == 100

    def test_get_issues_report_for_certain_period(self):
        filters = build_report_filters(
            field="Created",
            period=(
                dt.strftime(dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
                dt.strftime(dt.now(), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
            ),
        )

        issues = get_issues_for_report(self.report_fields, filters)

        assert len(issues) == 20
