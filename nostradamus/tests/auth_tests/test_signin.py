import os
import requests
import unittest
import pytest

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django

django.setup()

from apps.authentication.models import User


@pytest.mark.usefixtures(
    "sql_conn", "test_user_1", "host", "signin_url", "register_url"
)
class TestRegister(unittest.TestCase):
    def teardown_method(self, method):
        User.objects.filter(name=self.test_user_1["name"]).delete()

    def test_auth_by_username(self):
        requests.post(
            self.host + self.register_url, data=self.test_user_1
        ).json()

        test_user = {
            "credentials": self.test_user_1["name"],
            "password": self.test_user_1["password"],
        }

        request = requests.post(self.host + self.signin_url, data=test_user)
        data = request.json()

        assert data is not None and "exception" not in data

    def test_auth_by_email(self):
        requests.post(
            self.host + self.register_url, data=self.test_user_1
        ).json()

        test_user = {
            "credentials": self.test_user_1["email"],
            "password": self.test_user_1["password"],
        }

        request = requests.post(self.host + self.signin_url, data=test_user)
        data = request.json()

        assert data is not None and "exception" not in data

    def test_auth_error(self):
        requests.post(
            self.host + self.register_url, data=self.test_user_1
        ).json()

        test_user = {
            "credentials": self.test_user_1["email"],
            "password": "1234Pass",
        }

        request = requests.post(self.host + self.signin_url, data=test_user)
        data = request.json()

        assert data is not None and "exception" in data

    def test_auth_data(self):
        requests.post(
            self.host + self.register_url, data=self.test_user_1
        ).json()

        test_user = {
            "credentials": self.test_user_1["name"],
            "password": self.test_user_1["password"],
        }

        self.conn.execute(
            f"SELECT name FROM authentication_team WHERE id=%s",
            (self.test_user_1["team"],),
        )
        team = self.conn.fetchone()[0]

        self.conn.execute(
            f"SELECT id FROM authentication_user WHERE email=%s",
            (self.test_user_1["email"],),
        )
        user_id = self.conn.fetchone()[0]

        self.conn.execute(
            f"""
            SELECT
                name
            FROM
                authentication_role AS r
                INNER JOIN
                    authentication_teammember AS tm
                ON r.id = tm.role_id
            WHERE
                tm.user_id = '{user_id}'
            """,
        )
        role = self.conn.fetchone()[0]

        request = requests.post(self.host + self.signin_url, data=test_user)
        data = request.json()

        assert all(
            [
                data["id"] == user_id,
                data["name"] == self.test_user_1["name"],
                data["email"] == self.test_user_1["email"],
                data["team"] == team,
                data["role"] == role,
            ]
        )

    def test_auth_token(self):
        requests.post(
            self.host + self.register_url, data=self.test_user_1
        ).json()

        filter_route = "analysis_and_training/"
        test_user = {
            "credentials": self.test_user_1["name"],
            "password": self.test_user_1["password"],
        }

        request = requests.post(self.host + self.signin_url, data=test_user)
        token = "JWT " + request.json()["token"]
        headers = {"Authorization": token}

        request = requests.get(self.host + filter_route, headers=headers)

        assert request.status_code == 200
