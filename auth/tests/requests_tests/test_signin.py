import requests
import unittest
import pytest

from database import create_session
from models.User import User


@pytest.mark.usefixtures(
    "test_user_1",
    "host",
    "signin_url",
    "register_url",
    "verify_token_url",
)
class TestRegister(unittest.TestCase):
    def teardown_method(self, method):
        with create_session() as db:
            db.query(User).filter(User.name == self.test_user_1["name"]).delete()

    def test_auth_by_username(self):
        """Test request for checking auth by username."""
        requests.post(self.host + self.register_url, json=self.test_user_1).json()

        test_user = {
            "credentials": self.test_user_1["name"],
            "password": self.test_user_1["password"],
        }

        request = requests.post(self.host + self.signin_url, json=test_user)
        data = request.json()

        assert data is not None and "exception" not in data

    def test_auth_by_email(self):
        """Test request for checking auth by email."""
        requests.post(self.host + self.register_url, json=self.test_user_1)

        test_user = {
            "credentials": self.test_user_1["email"],
            "password": self.test_user_1["password"],
        }

        request = requests.post(self.host + self.signin_url, json=test_user)
        data = request.json()

        assert data is not None and "exception" not in data

    def test_auth_error(self):
        """Test request for checking auth error."""
        requests.post(self.host + self.register_url, json=self.test_user_1).json()

        test_user = {
            "credentials": self.test_user_1["email"],
            "password": "1234Pass",
        }

        request = requests.post(self.host + self.signin_url, json=test_user)
        data = request.json()

        assert (
            data is not None
            and data["exception"]["detail"] == "Incorrect username or password."
        )

    def test_auth_data(self):
        """Test request for validation data from response."""
        requests.post(self.host + self.register_url, json=self.test_user_1).json()

        test_user = {
            "credentials": self.test_user_1["name"],
            "password": self.test_user_1["password"],
        }

        with create_session() as db:
            user_id = (
                db.query(User)
                .filter(User.email == self.test_user_1["email"])
                .first()
                .id
            )

        request = requests.post(self.host + self.signin_url, json=test_user)
        data = request.json()

        assert all(
            [
                data["id"] == str(user_id),
                data["name"] == self.test_user_1["name"],
                data["email"] == self.test_user_1["email"],
            ]
        )

    def test_auth_token(self):
        """Test request for validate token."""
        requests.post(
            self.host + self.register_url,
            json=self.test_user_1,
        ).json()

        test_user = {
            "credentials": self.test_user_1["name"],
            "password": self.test_user_1["password"],
        }

        request = requests.post(self.host + self.signin_url, json=test_user)

        user_id = request.json()["id"]
        token = request.json()["token"]

        request = requests.get(
            self.host + self.verify_token_url, params={"token": token}
        )

        assert request.json()["id"] == user_id
