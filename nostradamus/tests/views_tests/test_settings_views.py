import requests

from pytest import mark
from unittest import TestCase


@mark.usefixtures("host", "settings_route")
class TestSettingsViews(TestCase):
    def test_get_settings_filters(self):
        request = requests.head(f"{self.host}{self.settings_route}filters/")

        assert "GET" in request.headers["Allow"]

    def test_post_settings(self):
        request = requests.head(f"{self.host}{self.settings_route}filters/")

        assert "POST" in request.headers["Allow"]

    def test_get_qa_metrics_settings(self):
        request = requests.head(f"{self.host}{self.settings_route}qa_metrics/")

        assert "GET" in request.headers["Allow"]

    def test_post_qa_metrics_settings(self):
        request = requests.head(f"{self.host}{self.settings_route}qa_metrics/")

        assert "POST" in request.headers["Allow"]

    def test_get_predictions_table(self):
        request = requests.head(
            f"{self.host}{self.settings_route}predictions_table/"
        )

        assert "GET" in request.headers["Allow"]

    def test_post_predictions_table(self):
        request = requests.head(
            f"{self.host}{self.settings_route}predictions_table/"
        )

        assert "POST" in request.headers["Allow"]

    def test_post_trainings(self):
        request = requests.head(f"{self.host}{self.settings_route}training/")

        assert "POST" in request.headers["Allow"]

    def test_get_source_filed(self):
        request = requests.head(
            f"{self.host}{self.settings_route}training/source_field/"
        )

        assert "GET" in request.headers["Allow"]

    def test_post_source_filed(self):
        request = requests.head(
            f"{self.host}{self.settings_route}training/source_field/"
        )

        assert "POST" in request.headers["Allow"]

    def test_get_markup_entities(self):
        request = requests.head(
            f"{self.host}{self.settings_route}training/markup_entities/"
        )

        assert "GET" in request.headers["Allow"]

    def test_get_bug_resolution(self):
        request = requests.head(
            f"{self.host}{self.settings_route}training/bug_resolution/"
        )

        assert "GET" in request.headers["Allow"]
