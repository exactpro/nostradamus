from json import loads

import requests

from utils.redis import redis_conn

SETTINGS_URL = "settings/"


def test_get_settings(host, auth_header, default_settings):
    request = requests.get(host + SETTINGS_URL, headers=auth_header)
    assert request.json() == default_settings


def test_get_settings_from_cache(sql_conn, test_user, default_settings):
    user_id = sql_conn.execute(
        "SELECT id FROM authentication_user WHERE email=(?)",
        (test_user["email"],),
    ).fetchone()[0]
    cached_settings = loads(redis_conn.get(f"settings:current:{user_id}"))

    assert cached_settings == default_settings


def test_update_settings(host, auth_header, new_settings):
    requests.post(host + SETTINGS_URL, headers=auth_header, json=new_settings)

    request = requests.get(host + SETTINGS_URL, headers=auth_header)
    assert request.json() == new_settings


def test_updated_settings_cache(sql_conn, test_user, new_settings):
    user_id = sql_conn.execute(
        "SELECT id FROM authentication_user WHERE email=(?)",
        (test_user["email"],),
    ).fetchone()[0]
    cached_settings = loads(redis_conn.get(f"settings:current:{user_id}"))

    assert cached_settings == new_settings


def test_updated_settings_backup(sql_conn, test_user, default_settings):
    user_id = sql_conn.execute(
        "SELECT id FROM authentication_user WHERE email=(?)",
        (test_user["email"],),
    ).fetchone()[0]
    cached_settings = loads(redis_conn.get(f"settings:backup:{user_id}"))

    assert cached_settings == default_settings
