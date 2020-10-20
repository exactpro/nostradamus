import requests

from pytest import mark
from unittest import TestCase


@mark.usefixtures("host", "description_assessment_route")
class TestDescriptionAssessmentViews(TestCase):
    def test_get_description_assessment_view(self):
        request = requests.head(
            f"{self.host}{self.description_assessment_route}"
        )

        assert "GET" in request.headers["Allow"]

    def test_post_description_assessment_predictions_view(self):
        request = requests.head(
            f"{self.host}{self.description_assessment_route}predict/"
        )

        assert "POST" in request.headers["Allow"]

    def test_post_description_assessment_highlight_view(self):
        request = requests.head(
            f"{self.host}{self.description_assessment_route}highlight/"
        )

        assert "POST" in request.headers["Allow"]
