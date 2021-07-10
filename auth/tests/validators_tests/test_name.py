import aiounittest
import pytest

from authentication.register import create_user
from database import create_session
from models.User import User
from serializers import UserSerializer
from validators.name import validate_name_pattern, validate_name_uniqueness


@pytest.mark.usefixtures(
    "test_user_1",
)
class TestRegister(aiounittest.AsyncTestCase):
    def teardown_method(self, _):
        with create_session() as db:
            db.query(User).filter(User.name == self.test_user_1["name"]).delete()

    def test_name_pattern_negative(self):
        """Negative test of validate name pattern."""
        name = "#Big%Test%"

        with pytest.raises(ValueError) as exception_info:
            validate_name_pattern(name)

        assert "Ensure that name doesn't have special symbols." == str(exception_info.value)

    def test_name_pattern_positive(self):
        """Positive test of validate name pattern."""
        name = "BigTest"
        validate_name_pattern(name)

    def test_name_uniqueness_positive(self):
        """Positive test of validate name uniqueness."""
        name = "test"
        validate_name_uniqueness(name)

    async def test_name_uniqueness_negative(self):
        """Negative test of validate name uniquness."""
        user = UserSerializer(**self.test_user_1)
        await create_user(user)

        name = self.test_user_1["name"]
        with pytest.raises(ValueError) as exception_info:
            validate_name_uniqueness(name)

        assert "Name already taken." == str(exception_info.value)
