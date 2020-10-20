import os
import requests

from unittest import TestCase
from pytest import mark

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django
from django.conf import settings

settings.MONGODB_NAME = "testdb"

django.setup()

from apps.extractor.main.connector import DB
from apps.authentication.models import User
from apps.extractor.main.connector import get_fields, get_unique_values
from apps.settings.main.common import (
    get_filter_settings,
    get_qa_metrics_settings,
    get_training_settings,
    get_predictions_table_settings,
    update_resolutions,
    update_training_settings,
    split_values,
    read_settings,
)


TEST_USER = {
    "team": 1,
    "name": "test123456",
    "email": "test@test.com",
    "password": 123456,
}


@mark.usefixtures("host")
class TestSettings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        requests.post("http://localhost:8000/auth/register/", data=TEST_USER)
        cls.__fill_db()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.filter(name=TEST_USER["name"]).delete()
        DB.delete_many({})

    @classmethod
    def __fill_db(self):
        DB.insert_many(
            documents=[
                {
                    "Project": "Test Project",
                    "Attachments": 12,
                    "Priority": "Minor" if not _ % 5 else "Major",
                }
                for _ in range(100)
            ]
        )

    @classmethod
    def teardown_class(cls) -> None:
        User.objects.filter(name=TEST_USER["name"]).delete()

    def test_get_filter_settings(self):
        user = User.objects.get(name=TEST_USER["name"])
        settings = get_filter_settings(user.id)

        assert settings

    def test_qa_metrics_settings(self):
        user = User.objects.get(name=TEST_USER["name"])
        settings = get_qa_metrics_settings(user.id)

        assert settings

    def test_training_settings(self):
        user = User.objects.get(name=TEST_USER["name"])
        settings = get_training_settings(user)

        assert settings

    def test_update_resolutions(self):
        user = User.objects.get(name=TEST_USER["name"])
        data = {
            "mark_up_entities": [
                {"area_of_testing": "TestAOT", "entities": ["Minor"]}
            ],
            "bug_resolution": [
                {"metric": "Resolution", "value": "Fixed"},
                {"metric": "Resolution", "value": "Duplicate"},
            ],
            "predictions_table": get_predictions_table_settings(user),
            "source_field": get_training_settings(user)["source_field"],
        }

        update_resolutions(data, user)
        settings = get_predictions_table_settings(user)

        settings_clear = {
            "bug_resolution": [],
            "mark_up_entities": [],
            "predictions_table": get_predictions_table_settings(user),
            "source_field": "",
        }
        update_resolutions(settings_clear, user)

        settings_clear = get_predictions_table_settings(user)

        assert len(settings_clear) != len(settings)

    def test_update_training_settings(self):
        user = User.objects.get(name=TEST_USER["name"])
        settings = {
            "bug_resolution": [],
            "mark_up_entities": [],
            "source_field": "Priority",
        }
        update_training_settings(settings, user)

        assert get_training_settings(user).get("source_field") == "Priority"

    def test_get_predictions_table_settings(self):
        user = User.objects.get(name=TEST_USER["name"])
        settings = get_predictions_table_settings(user.id)

        assert settings

    def test_split_values(self):
        values = ["Major", "Minor"]
        sp_values = split_values(values)

        assert sp_values == {"Major", "Minor"}

    def test_get_unique_values(self):
        values = get_unique_values("Priority")

        assert values == ["Major", "Minor"]

    def test_get_fields(self):
        assert get_fields() == ["_id", "Project", "Attachments", "Priority"]

    def test_read_settings(self):
        user = User.objects.get(name=TEST_USER["name"])
        filters = [
            {"name": "Priority", "filtration_type": "drop-down"},
            {"name": "Attachments", "filtration_type": "numeric"},
        ]

        read_settings(filters, user)
        assert all([filters[0].get("settings"), filters[1].get("settings")])
