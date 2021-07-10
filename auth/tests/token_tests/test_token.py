import aiounittest
import pytest
from fastapi import HTTPException

from authentication.register import create_user
from authentication.token import create_token, decode_jwt
from database import create_session
from models.User import User
from serializers import UserSerializer


@pytest.mark.usefixtures(
    "test_user_1",
    "test_user_model"
)
class TestRegister(aiounittest.AsyncTestCase):
    def teardown_method(self, _):
        with create_session() as db:
            db.query(User).filter(User.name == self.test_user_1["name"]).delete()

    def test_create_token(self):
        """Test for validate create token."""
        token = create_token(self.test_user_model)

        assert token

    def test_decode_token_user_not_found(self):
        """Negative test for validate decode token with error 'user_not_found'."""
        token = create_token(self.test_user_model)
        with pytest.raises(HTTPException) as exception_info:
            decode_jwt(token)

        assert exception_info

    def test_decode_token_invalid(self):
        """Negative test for validate decode invalid token."""
        token = "adbcdeerf123"
        with pytest.raises(HTTPException) as exception_info:
            decode_jwt(token)

        assert exception_info

    async def test_decode_token_positive(self):
        """Positive test for validate decode token."""
        user = UserSerializer(**self.test_user_1)
        await create_user(user)

        with create_session() as db:
            user = db.query(User).filter(User.name == self.test_user_1["name"]).first()

        token = create_token(user)
        user_id = decode_jwt(token)

        assert user_id