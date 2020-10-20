import requests

from pytest import mark
from unittest import TestCase


@mark.usefixtures("host", "auth_route")
class TestAuthViews(TestCase):
    def test_get_register(self):
        request = requests.head(f"{self.host}{self.auth_route}register/")

        assert "GET" in request.headers["Allow"]

    def test_post_register(self):
        request = requests.head(f"{self.host}{self.auth_route}register/")

        assert "POST" in request.headers["Allow"]

    def test_post_signin(self):
        request = requests.head(f"{self.host}{self.auth_route}signin/")

        assert "POST" in request.headers["Allow"]
