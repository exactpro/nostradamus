import requests


ROUTE = "settings/"


def test_get_settings(host):
    request = requests.head(host + ROUTE)

    assert "GET" in request.headers["Allow"]


def test_post_settings(host):
    request = requests.head(host + ROUTE)

    assert "POST" in request.headers["Allow"]


def test_post_rollback(host):
    request = requests.head(host + ROUTE + "rollback/")

    assert "POST" in request.headers["Allow"]
