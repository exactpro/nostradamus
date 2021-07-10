import aiounittest
import pytest

from authentication.register import create_user
from database import create_session
from models.User import User
from serializers import UserSerializer
from validators.email import validate_email_pattern, validate_email_uniqueness


@pytest.mark.usefixtures(
    "test_user_1",
)
class TestRegister(aiounittest.AsyncTestCase):
    def teardown_method(self, _):
        with create_session() as db:
            db.query(User).filter(User.name == self.test_user_1["name"]).delete()

    def test_email_pattern_negative(self):
        """Negative test of validate email pattern."""
        email = "#test%test%@gmail.com"
        with pytest.raises(ValueError) as exception_info:
            validate_email_pattern(email)

        assert "Ensure that email doesn't have special characters." == str(exception_info.value)

    def test_email_pattern_positive(self):
        """Positive test of validate email pattern."""
        email = "test@gmail.com"
        validate_email_pattern(email)

    def test_email_uniqueness_positive(self):
        """Positive test of validate email uniqueness."""
        email = "test@gmail.com"
        validate_email_uniqueness(email)

    async def test_email_uniqueness_negative(self):
        """Negative test of validate email uniqueness."""
        user = UserSerializer(**self.test_user_1)
        await create_user(user)

        email = self.test_user_1["email"]
        with pytest.raises(ValueError) as exception_info:
            validate_email_uniqueness(email)

        assert "Email already taken." == str(exception_info.value)
