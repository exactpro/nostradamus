import requests


ROUTE = "qa_metrics/"


def test_get_qa_metrics_view(host):
    request = requests.head(host + ROUTE)

    assert "GET" in request.headers["Allow"]


def test_get_predictions_info_view(host):
    request = requests.head(host + ROUTE + "predictions_info/")

    assert "GET" in request.headers["Allow"]


def test_predictions_table_view(host):
    request = requests.head(host + ROUTE + "predictions_table/")

    assert "GET" in request.headers["Allow"]
