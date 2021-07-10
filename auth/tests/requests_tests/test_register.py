import requests
import unittest
import pytest

from database import create_session
from models.User import User


@pytest.mark.usefixtures(
    "test_user_1",
    "test_user_2",
    "host",
    "register_url",
)
class TestRegister(unittest.TestCase):
    def teardown_method(self, _):
        with create_session() as db:
            db.query(User).filter(User.name == self.test_user_1["name"]).delete()
            db.query(User).filter(User.name == self.test_user_2["name"]).delete()

    def test_register_success(self):
        """Test request for register success."""
        request = requests.post(self.host + self.register_url, json=self.test_user_1)

        assert request.status_code == 200

    def test_registered_already(self):
        """Test request that user registered already."""
        requests.post(self.host + self.register_url, json=self.test_user_2)
        request = requests.post(self.host + self.register_url, json=self.test_user_2)

        assert (
            request.status_code == 400
            and request.json()["exception"][0]["errors"][0] == "Email already taken."
        )

    def test_check_registered_user(self):
        """Test that registered user exist in database."""
        requests.post(self.host + self.register_url, json=self.test_user_2)
        with create_session() as db:
            result = (
                db.query(User)
                .filter(
                    User.name == self.test_user_2["name"],
                    User.email == self.test_user_2["email"],
                )
                .first()
            )

        assert result is not None
