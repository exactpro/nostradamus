import requests
import unittest
import pytest
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "nostradamus.settings"

import django

django.setup()

from apps.authentication.models import User


@pytest.mark.usefixtures(
    "sql_conn", "test_user_1", "test_user_2", "host", "register_url"
)
class TestRegister(unittest.TestCase):
    def teardown_method(self, _):
        User.objects.filter(name=self.test_user_1["name"]).delete()
        User.objects.filter(name=self.test_user_2["name"]).delete()

    def test_get_teams(self):
        request = requests.get(self.host + self.register_url)
        teams = {team["name"] for team in request.json()}

        self.conn.execute("SELECT name FROM authentication_team")
        db_teams = set(*self.conn.fetchall())

        assert db_teams == teams

    def test_register_success(self):
        request = requests.post(
            self.host + self.register_url, data=self.test_user_1
        )

        assert request.json() == {"result": "success"}

    def test_registered_already(self):
        requests.post(self.host + self.register_url, data=self.test_user_2)
        request = requests.post(
            self.host + self.register_url, data=self.test_user_2
        )
        assert request.status_code == 400

    def test_check_registered_user(self):
        self.conn.execute(
            f"SELECT * FROM authentication_user WHERE name='{self.test_user_1['name']}' AND email='{self.test_user_1['email']}'",
        )

        result = self.conn.fetchall()

        assert result is not None

    def test_special_symbols(self):
        test_user = self.test_user_1.copy()
        test_user.update(
            {"name": "test#$%user", "email": "test.user1@test.com"}
        )

        request = requests.post(self.host + self.register_url, data=test_user)
        assert (
            request.json()["exception"]["fields"][0]["name"] == "name"
            and request.json()["exception"]["fields"][0]["errors"][0]
            == "Ensure that name doesn't have special symbols."
        )

    def test_password_length(self):
        test_user = self.test_user_1.copy()
        test_user.update(
            {
                "name": "test.user.2",
                "email": "test.user.2@test.com",
                "password": 123,
            }
        )
        request = requests.post(self.host + self.register_url, data=test_user)

        assert (
            request.status_code == 400
            and request.json()["exception"]["fields"][0]["name"] == "password"
        )

    def test_whitespaces_credentials(self):
        test_user = self.test_user_1.copy()
        test_user.update(
            {
                "name": "test.user 3",
                "email": "test.user3@test.com",
            }
        )
        request = requests.post(self.host + self.register_url, data=test_user)

        assert (
            request.json()["exception"]["fields"][0]["name"] == "name"
            and request.json()["exception"]["fields"][0]["errors"][0]
            == "Ensure that username doesn't have whitespaces."
        )
