import requests


ROUTE = 'auth/'


def test_get_register(host):
    request = requests.head(host + ROUTE + 'register/')

    assert 'GET' in request.headers['Allow']


def test_post_register(host):
    request = requests.head(host + ROUTE + 'register/')

    assert 'POST' in request.headers['Allow']


def test_post_signin(host):
    request = requests.head(host + ROUTE + 'signin/')

    assert 'POST' in request.headers['Allow']
