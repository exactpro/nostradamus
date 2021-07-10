import requests

from pytest import mark
from unittest import TestCase


@mark.usefixtures("host", "analysis_and_training_route")
class TestAnalysisAndTrainingViews(TestCase):
    def test_get_analysis_and_training_count(self,):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}"
        )

        assert "GET" in request.headers["Allow"]

    def test_get_filter(self):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}filter/"
        )

        assert "GET" in request.headers["Allow"]

    def test_post_filter(self,):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}filter/"
        )

        assert "POST" in request.headers["Allow"]

    def test_get_defect_submission(self,):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}defect_submission/"
        )

        assert "GET" in request.headers["Allow"]

    def test_get_significant_terms(self):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}significant_terms/"
        )

        assert "GET" in request.headers["Allow"]

    def test_post_significant_terms(self):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}significant_terms/"
        )

        assert "POST" in request.headers["Allow"]

    def test_get_statistics(self):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}statistics/"
        )

        assert "GET" in request.headers["Allow"]

    def test_get_frequently_terms(self):
        request = requests.head(
            f"{self.host}{self.analysis_and_training_route}frequently_terms/"
        )
