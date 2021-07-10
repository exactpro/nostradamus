import json
from typing import Dict, Union


from fastapi import HTTPException
from passlib.context import CryptContext

from authentication.token import create_token
from models.User import User

from serializers import UserCredentialsSerializer
from database import create_session


DEFAULT_ERROR_CODE = 500


def auth_user(
    user_data: UserCredentialsSerializer,
) -> Dict[str, Union[str, int]]:
    """Authenticates User.

    :param user_data: User credentials.
    :return: Authenticated User with JWT.
    """
    with create_session() as db:
        user = (
            db.query(User)
            .filter(User.email == user_data.credentials.lower().strip())
            .first()
        )
        if not user:
            user = (
                db.query(User)
                .filter(
                    User.name == user_data.credentials.strip(),
                )
                .first()
            )
            if not user:
                raise HTTPException(
                    status_code=DEFAULT_ERROR_CODE,
                    detail="Incorrect username or password.",
                )
        if not CryptContext(schemes=["sha256_crypt"]).verify(
            user_data.password, user.password
        ):
            raise HTTPException(
                status_code=DEFAULT_ERROR_CODE,
                detail="Incorrect username or password.",
            )

    response = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "token": create_token(user),
    }
    return response
