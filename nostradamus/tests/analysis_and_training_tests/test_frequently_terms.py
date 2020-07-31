import os
import pandas as pd

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django
from django.conf import settings

settings.MONGODB_NAME = "testdb"
settings.MONGODB_HOST = "127.0.0.1"

django.setup()

import unittest
import pytest

from datetime import datetime as dt

from apps.extractor.main.connector import DB
from apps.extractor.main.preprocessor import get_issues_dataframe
from apps.analysis_and_training.main.frequently_used_terms import (
    calculate_frequently_terms,
)


@pytest.mark.usefixtures("result_significant_metrics", "settings_aot_metrics")
class TestFrequentlyTerms(unittest.TestCase):
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

    def test_frequently_terms(self):
        issues = get_issues_dataframe(
            fields=[
                "Priority",
                "Resolution",
                "Description_tr",
                "Assignee",
                "Reporter",
            ],
            filters=[],
        )

        frequently_terms = calculate_frequently_terms(issues)

        assert frequently_terms == ["description_tr"]
