import requests


def test_get_settings_filters(host, settings_route):
    request = requests.head(f"{host}{settings_route}filters/")

    assert "GET" in request.headers["Allow"]


def test_post_settings(host, settings_route):
    request = requests.head(f"{host}{settings_route}filters/")

    assert "POST" in request.headers["Allow"]


def test_get_qa_metrics_settings(host, settings_route):
    request = requests.head(f"{host}{settings_route}qa_metrics/")

    assert "GET" in request.headers["Allow"]


def test_post_qa_metrics_settings(host, settings_route):
    request = requests.head(f"{host}{settings_route}qa_metrics/")

    assert "POST" in request.headers["Allow"]


def test_get_predictions_table(host, settings_route):
    request = requests.head(f"{host}{settings_route}predictions_table/")

    assert "GET" in request.headers["Allow"]


def test_post_predictions_table(host, settings_route):
    request = requests.head(f"{host}{settings_route}predictions_table/")

    assert "POST" in request.headers["Allow"]


def test_post_trainings(host, settings_route):
    request = requests.head(f"{host}{settings_route}training/")

    assert "POST" in request.headers["Allow"]


def test_get_source_filed(host, settings_route):
    request = requests.head(f"{host}{settings_route}training/source_field/")

    assert "GET" in request.headers["Allow"]


def test_post_source_filed(host, settings_route):
    request = requests.head(f"{host}{settings_route}training/source_field/")

    assert "POST" in request.headers["Allow"]


def test_get_markup_entities(host, settings_route):
    request = requests.head(f"{host}{settings_route}training/markup_entities/")

    assert "GET" in request.headers["Allow"]


def test_get_bug_resolution(host, settings_route):
    request = requests.head(f"{host}{settings_route}training/bug_resolution/")

    assert "GET" in request.headers["Allow"]
