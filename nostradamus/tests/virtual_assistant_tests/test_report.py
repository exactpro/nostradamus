import os

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django
from django.conf import settings

settings.MONGODB_NAME = "testdb"
settings.MONGODB_HOST = "127.0.0.1"

django.setup()

import unittest
import pytest

from pathlib import Path
from pandas import ExcelWriter
from datetime import datetime as dt
from datetime import timedelta as td
from apps.extractor.main.connector import DB
from apps.virtual_assistant.main.report_generator import (
    build_report_filters,
    get_issues_for_report,
    create_report_file,
    make_report_path,
    write_report_dataframe,
)


@pytest.mark.usefixtures("report_fields")
class TestReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.__fill_testdb()

    @classmethod
    def tearDownClass(cls) -> None:
        DB.delete_many({})
        path = (
            Path(__file__)
            .parents[3]
            .joinpath("chatbot")
            .joinpath("reports")
            .joinpath(f"{dt.now().strftime('%Y-%m-%d')}.xlsx")
        )
        if os.path.isfile(path):
            os.remove(path)

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
            field="Created",
            values=("01-01-2000", "30-01-2000"),
            f_type="date",
            exact_match=True,
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
            field="Resolved",
            values=("01-12-1980", "31-12-1980"),
            f_type="date",
            exact_match=True,
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
        filters = build_report_filters(
            field="Created", values=(), f_type="date", exact_match=True
        )

        issues = get_issues_for_report(self.report_fields, filters)

        assert len(issues) == 100

    def test_get_issues_report_for_certain_period(self):
        filters = build_report_filters(
            field="Created",
            values=(
                dt.strftime(dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
                dt.strftime(dt.now(), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
            ),
            f_type="date",
            exact_match=True,
        )

        issues = get_issues_for_report(self.report_fields, filters)

        assert len(issues) == 20

    def test_create_report_file(self):
        filters = build_report_filters(
            field="Created",
            values=(
                dt.strftime(dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
                dt.strftime(dt.now(), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
            ),
            f_type="date",
            exact_match=True,
        )

        created_issues = get_issues_for_report(["Created"], filters)
        filters = build_report_filters(
            field="Resolved",
            values=(
                dt.strftime(dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
                dt.strftime(dt.now(), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
            ),
            f_type="date",
            exact_match=True,
        )

        resolved_issues = get_issues_for_report(
            ["Created", "Resolved"], filters
        )

        filepath = make_report_path(filters[0]["current_value"][1])

        create_report_file(
            created_issues=created_issues,
            resolved_issues=resolved_issues,
            filename="test_file",
            file_path=filepath,
        )

        assert os.path.isfile(filepath)

    def test_write_report_dataframe(self):
        filters = build_report_filters(
            field="Created",
            values=(
                dt.strftime(dt.now() - td(days=1), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
                dt.strftime(dt.now(), "%Y-%m-%dT%H:%M:%S.%f%zZ"),
            ),
            f_type="date",
            exact_match=True,
        )

        issues = get_issues_for_report(["Created"], filters)
        filepath = make_report_path(filters[0]["current_value"][1])
        filename = "test_file"
        with ExcelWriter(filepath, engine="xlsxwriter") as writer:
            if not writer.book.get_worksheet_by_name(filename):
                sheet = writer.book.add_worksheet(filename)
                writer.sheets.update({filename: sheet})

            text_style = writer.book.add_format()
            row = write_report_dataframe(
                df=issues,
                writer=writer,
                sheet_name=filename,
                header="Test",
                text_style=text_style,
                row_number=0,
            )

        assert row == 23
