import requests


def test_get_analysis_and_training_count(
    host, analysis_and_training_route,
):
    request = requests.head(f"{host}{analysis_and_training_route}")

    assert "GET" in request.headers["Allow"]


def test_get_filter(host, analysis_and_training_route):
    request = requests.head(f"{host}{analysis_and_training_route}filter/")

    assert "GET" in request.headers["Allow"]


def test_post_filter(
    host, analysis_and_training_route,
):
    request = requests.head(f"{host}{analysis_and_training_route}filter/")

    assert "POST" in request.headers["Allow"]


def test_get_defect_submission(
    host, analysis_and_training_route,
):
    request = requests.head(
        f"{host}{analysis_and_training_route}defect_submission/"
    )

    assert "GET" in request.headers["Allow"]


def test_post_defect_submission(
    host, analysis_and_training_route,
):
    request = requests.head(
        f"{host}{analysis_and_training_route}defect_submission/"
    )

    assert "POST" in request.headers["Allow"]


def test_get_significant_terms(host, analysis_and_training_route):
    request = requests.head(
        f"{host}{analysis_and_training_route}significant_terms/"
    )

    assert "GET" in request.headers["Allow"]


def test_post_significant_terms(host, analysis_and_training_route):
    request = requests.head(
        f"{host}{analysis_and_training_route}significant_terms/"
    )

    assert "POST" in request.headers["Allow"]


def test_post_train(host, analysis_and_training_route):
    request = requests.head(f"{host}{analysis_and_training_route}train/")

    assert "POST" in request.headers["Allow"]


def test_get_statistics(host, analysis_and_training_route):
    request = requests.head(f"{host}{analysis_and_training_route}statistics/")

    assert "GET" in request.headers["Allow"]


def test_get_frequently_terms(host, analysis_and_training_route):
    request = requests.head(
        f"{host}{analysis_and_training_route}frequently_terms/"
    )
