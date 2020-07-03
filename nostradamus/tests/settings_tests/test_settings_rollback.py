from json import dumps

import requests

from tests.settings_tests.test_settings import SETTINGS_URL

ROLLBACK_URL = "settings/rollback/"


def test_rollback(host, auth_header, default_settings):
    requests.post(host + ROLLBACK_URL, headers=auth_header)

    request = requests.get(host + SETTINGS_URL, headers=auth_header)

    assert request.json() == default_settings


def test_negative_rollback(host, auth_header, default_settings):
    # When backup is does't exists in cache
    request = requests.post(host + ROLLBACK_URL, headers=auth_header)

    assert request.json() == {"result": "There are no any previous settings"}
