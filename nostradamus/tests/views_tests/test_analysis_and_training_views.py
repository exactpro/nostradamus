import requests


ROUTE = 'analysis_and_training/'


def test_post_jira_login(host):
    request = requests.head(host + ROUTE + 'jira_login/')

    assert 'POST' in request.headers['Allow']


def test_get_filter(host):
    request = requests.head(host + ROUTE + 'filter/')

    assert 'GET' in request.headers['Allow']


def test_post_filter(host):
    request = requests.head(host + ROUTE + 'filter/')

    assert 'POST' in request.headers['Allow']


def test_get_defect_submission(host):
    request = requests.head(host + ROUTE + 'defect_submission/')

    assert 'GET' in request.headers['Allow']


def test_get_significant_terms(host):
    request = requests.head(host + ROUTE + 'significant_terms/')

    assert 'GET' in request.headers['Allow']


def test_post_train(host):
    request = requests.head(host + ROUTE + 'train/')

    assert 'POST' in request.headers['Allow']
