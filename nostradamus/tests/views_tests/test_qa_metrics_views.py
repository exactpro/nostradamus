import requests

from pytest import mark
from unittest import TestCase


@mark.usefixtures("host", "qa_metrics_route")
class TestQAMetricsViews(TestCase):
    def test_get_qa_metrics_view(self):
        request = requests.head(f"{self.host}{self.qa_metrics_route}")

        assert "GET" in request.headers["Allow"]

    def test_get_qa_metrics_filter_view(self):
        request = requests.head(f"{self.host}{self.qa_metrics_route}filter/")

        assert "GET" in request.headers["Allow"]

    def test_post_qa_metrics_filter_view(self):
        request = requests.head(f"{self.host}{self.qa_metrics_route}filter/")

        assert "POST" in request.headers["Allow"]

    def test_get_predictions_info_view(self):
        request = requests.head(
            f"{self.host}{self.qa_metrics_route}predictions_info/"
        )

        assert "GET" in request.headers["Allow"]

    def test_predictions_table_view(self):
        request = requests.head(
            f"{self.host}{self.qa_metrics_route}predictions_table/"
        )

        assert "POST" in request.headers["Allow"]
