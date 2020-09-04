import requests


def test_get_qa_metrics_view(host, qa_metrics_route):
    request = requests.head(host + qa_metrics_route)

    assert "GET" in request.headers["Allow"]


def test_get_qa_metrics_filter_view(host, qa_metrics_route):
    request = requests.head(f"{host}{qa_metrics_route}filter/")

    assert "GET" in request.headers["Allow"]


def test_post_qa_metrics_filter_view(host, qa_metrics_route):
    request = requests.head(f"{host}{qa_metrics_route}filter/")

    assert "POST" in request.headers["Allow"]


def test_get_predictions_info_view(host, qa_metrics_route):
    request = requests.head(f"{host}{qa_metrics_route}predictions_info/")

    assert "GET" in request.headers["Allow"]


def test_predictions_table_view(host, qa_metrics_route):
    request = requests.head(f"{host}{qa_metrics_route}predictions_table/")

    assert "GET" in request.headers["Allow"]
