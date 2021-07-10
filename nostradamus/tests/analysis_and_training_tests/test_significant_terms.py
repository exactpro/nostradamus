import os

from apps.analysis_and_training.main.mark_up import mark_up_series

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django
from django.conf import settings

settings.MONGODB_NAME = "testdb"

django.setup()

import unittest
import pytest
from utils.warnings import (
    SignificantTermsMetricDoesntExist,
    SignificantTermsLessOnePercentWarning,
)
from datetime import datetime as dt
from apps.extractor.main.connector import DB
from apps.extractor.main.preprocessor import get_issues_dataframe
from apps.analysis_and_training.main.significant_terms import (
    get_significant_terms,
    check_standard_metric,
    check_aot_metric,
)


@pytest.mark.usefixtures("result_significant_metrics", "settings_aot_metrics")
class TestSignificantTerms(unittest.TestCase):
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
                    "Priority": "Blocker"
                    if _ % 150 == 0
                    else "Major"
                    if _ % 5 == 0
                    else "Minor",
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
                for _ in range(15000)
            ],
            ordered=False,
        )

    def test_get_significant_terms(self):
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

        significant_terms = get_significant_terms(issues)

        assert significant_terms == self.result_significant_terms

    def test_get_significant_terms_with_aot(self):
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
        aot = self.settings_for_aot.copy()
        aot["mark_up_entities"][0]["entities"] = ["Major"]

        significant_terms = get_significant_terms(issues, aot)

        result_significant_terms = self.result_significant_terms.copy()
        result_significant_terms["metrics"].append("AOT1")

        assert significant_terms == result_significant_terms

    def test_get_significant_terms_with_filter_positive(self):
        issues = get_issues_dataframe(
            fields=[
                "Priority",
                "Resolution",
                "Description_tr",
                "Assignee",
                "Reporter",
            ],
            filters=[
                {
                    "name": "Priority",
                    "type": "drop-down",
                    "current_value": ["Major"],
                    "exact_match": False,
                }
            ],
        )

        significant_terms = get_significant_terms(issues)

        assert all(
            [
                significant_terms["chosen_metric"] == "Resolution Done",
                significant_terms["metrics"]
                == [
                    "Resolution Done",
                    "Resolution Rejected",
                    "Resolution Unresolved",
                    "Priority Major",
                ],
            ]
        )

    def test_check_aot_metric_doesnt_exist_metric(self):
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
        metric = "test"
        source_field = self.settings_for_aot["source_field"]
        mark_up_entities = self.settings_for_aot["mark_up_entities"]

        with pytest.raises(SignificantTermsMetricDoesntExist) as excinfo:
            check_aot_metric(issues, metric, source_field, mark_up_entities)

        assert excinfo

    def test_check_standard_metric_doesnt_exist_metric(self):
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
        metric = "Resolution test"

        with pytest.raises(SignificantTermsMetricDoesntExist) as excinfo:
            check_standard_metric(issues, metric)

        assert excinfo

    def test_check_standard_metric_few_bugs_for_metric(self):
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
        metric = "Priority Blocker"

        with pytest.raises(SignificantTermsLessOnePercentWarning) as excinfo:
            check_standard_metric(issues, metric)

        assert excinfo

    def test_check_aot_metric_few_bugs_for_metric(self):
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
        metric = "AOT1"
        source_field = self.settings_for_aot["source_field"]
        mark_up_entities = self.settings_for_aot.copy()
        mark_up_entities = mark_up_entities["mark_up_entities"]
        for area in mark_up_entities:
            area["entities"] = ["Blocker"]

        with pytest.raises(SignificantTermsLessOnePercentWarning) as excinfo:
            check_aot_metric(issues, metric, source_field, mark_up_entities)

        assert excinfo
