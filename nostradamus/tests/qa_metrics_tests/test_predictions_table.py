import os

from apps.qa_metrics.main.charts import (
    calculate_aot_percentage,
    calculate_priority_percentage,
    calculate_ttr_percentage,
    calculate_resolution_percentage,
)

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django

django.setup()

from apps.qa_metrics.main.predictions_table import (
    get_predictions_table,
    paginate_bugs,
)
import unittest
import pytest

import pandas as pd

from datetime import datetime as dt


@pytest.mark.usefixtures(
    "predictions_table_settings",
    "training_parameters",
    "predictions_table_fields",
)
class TestPredictionsTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.issues = cls.make_test_predictions()

    @classmethod
    def make_test_predictions(self):
        return pd.DataFrame.from_records(
            [
                {
                    "Project": "Test Project",
                    "Attachments": 12,
                    "Priority": "Minor",
                    "Created": dt.now(),
                    "Resolved": dt.now(),
                    "Updated": dt.now(),
                    "Labels": "Test Label",
                    "Comments": 1,
                    "Status": "Open",
                    "Key": str(_),
                    "Summary": "Test Summary",
                    "Resolution": "Unresolved",
                    "Description": "Test Description",
                    "Description_tr": "Test Description_tr",
                    "Time_To_Resolve": 10,
                    "Markup": 1,
                    "Components": "Test components",
                    "Version": "Test Version",
                    "Assignee": "Test Assignee",
                    "Reporter": "Test Reporter",
                    "areas_of_testing_prediction": {"test": 0.0, "Other": 1.0},
                    "Resolution_prediction": {
                        "Done": {"not Done": 0.175, "Done": 0.825}
                    },
                    "Priority_prediction": {
                        "Blocker": 0.023,
                        "Critical": 0.113,
                        "Major": 0.774,
                        "Minor": 0.09,
                    },
                    "Time to Resolve_prediction": {
                        r"1": 0.236,
                        r"2": 0.183,
                        r"3": 0.383,
                        r"4": 0.198,
                    },
                }
                for _ in range(100)
            ]
        )

    def test_get_predictions_table_without_limit(self):
        predictions_table = get_predictions_table(
            self.issues, self.predictions_table_fields, None, None
        )

        assert len(predictions_table) == 100

    def test_get_predictions_table_with_limit(self):
        predictions_table = get_predictions_table(
            self.issues, self.predictions_table_fields, 0, 20
        )

        assert len(predictions_table) == 20

    def test_predictions_pagination(self):
        predictions_table = get_predictions_table(
            self.issues, self.predictions_table_fields, None, None
        )

        predictions_table = paginate_bugs(predictions_table, 0, 20)

        assert len(predictions_table) == 20

    def test_calculate_aot_percentage(self):
        predictions_table = get_predictions_table(
            self.issues, self.predictions_table_fields, None, None
        )
        areas_of_testing_percentage = calculate_aot_percentage(
            predictions_table["Area of Testing"]
        )

        assert areas_of_testing_percentage == {"Other": 100}

    def test_calculate_priority_percentage(self):
        predictions_table = get_predictions_table(
            self.issues, self.predictions_table_fields, None, None
        )
        priority_percentage = calculate_priority_percentage(
            predictions_table["Priority"], self.training_parameters["Priority"]
        )

        assert priority_percentage == {
            "Major": 0,
            "Blocker": 0,
            "Critical": 0,
            "Minor": 100,
        }

    def test_calculate_ttr_percentage(self):
        predictions_table = get_predictions_table(
            self.issues, self.predictions_table_fields, None, None
        )
        ttr_percentage = calculate_ttr_percentage(
            predictions_table["Time to Resolve"],
            self.training_parameters["Time to Resolve"],
        )

        assert ttr_percentage == {
            "3": 100,
            "0-1.0": 0,
            "0.999-1.0": 0,
            "2.0-19.0": 0,
            "20.0-127.0": 0,
            ">127.0": 0,
        }

    def test_calculate_resolution_percentage(self):
        predictions_table = get_predictions_table(
            self.issues, self.predictions_table_fields, None, None
        )
        resolution_percentage = calculate_resolution_percentage(
            predictions_table, self.training_parameters["Resolution"],
        )

        assert resolution_percentage == {"Done": {"Done": 100, "not Done": 0}}
