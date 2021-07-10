import requests
import unittest
import pytest

from database import create_session
from models.User import User


@pytest.mark.usefixtures(
    "test_user_1",
    "host",
    "register_url",
)
class TestRegister(unittest.TestCase):
    def teardown_method(self, _):
        with create_session() as db:
            db.query(User).filter(User.name == self.test_user_1["name"]).delete()

    def test_special_symbols_of_name(self):
        """Test request for checking special symbols in a field name."""
        test_user = self.test_user_1.copy()
        test_user.update({"name": "test#$%user", "email": "test.user1@test.com"})

        request = requests.post(self.host + self.register_url, json=test_user)
        assert (
            request.json()["exception"][0]["name"] == "name"
            and request.json()["exception"][0]["errors"][0]
            == "Ensure that name doesn't have special symbols."
        )

    def test_special_symbols_of_email(self):
        """Test request for checking special symbols in a field email."""
        test_user = self.test_user_1.copy()
        test_user.update({"name": "test.user", "email": "test.u#ser1@test.com"})

        request = requests.post(self.host + self.register_url, json=test_user)
        assert (
            request.json()["exception"][0]["name"] == "email"
            and request.json()["exception"][0]["errors"][0]
            == "Ensure that email doesn't have special characters."
        )

    def test_password_length(self):
        """Test request for checking password length."""
        test_user = self.test_user_1.copy()
        test_user.update(
            {
                "name": "test.user.2",
                "email": "test.user.2@test.com",
                "password": 123,
            }
        )
        request = requests.post(self.host + self.register_url, json=test_user)

        assert (
            request.status_code == 400
            and request.json()["exception"][0]["errors"][0]
            == "Ensure password cannot be less than 6 symbol(s)."
        )

    def test_whitespaces_credentials(self):
        """Test request for checking whitespaces in field."""
        test_user = self.test_user_1.copy()
        test_user.update(
            {
                "name": "test.user 3",
                "email": "test.user3@test.com",
            }
        )
        request = requests.post(self.host + self.register_url, json=test_user)

        assert (
            request.json()["exception"][0]["name"] == "name"
            and request.json()["exception"][0]["errors"][0]
            == "Username cannot contain whitespaces."
        )
