import os

import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

from database import create_session
from models.User import User

ACCESS_TOKEN_EXPIRE_WEEKS = 15

SECRET_KEY_DEFAULT = "v$1bx=+6#ibt4a$4i&5i8stwjqzm+3=tjsde9iku1a0w(u6bfy"
SECRET_KEY = os.environ.get("SECRET_KEY", default=SECRET_KEY_DEFAULT)


def create_token(user: User) -> str:
    """Generates JSON Web Token.

    :param user: User to be authenticated.
    :return: JSON Web Token.
    """
    raw_token = {
        "exp": datetime.utcnow() + timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS),
        "id": str(user.id),
    }
    token = jwt.encode(raw_token, key=SECRET_KEY).decode("UTF-8")
    return token


def decode_jwt(token: str) -> str:
    """Checks JSON Web Token and return user id.

    :param token: JSON Web Token.
    :return: User id.
    """
    # To avoid a circular dependency
    from authentication.sign_in import DEFAULT_ERROR_CODE

    try:
        decoded_token = jwt.decode(jwt=token, key=SECRET_KEY)
    except jwt.DecodeError:
        raise HTTPException(status_code=DEFAULT_ERROR_CODE, detail="Token is invalid")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=DEFAULT_ERROR_CODE, detail="Token expired")
    with create_session() as db:
        user = db.query(User).filter(User.id == decoded_token.get("id")).first()

        if not user:
            raise HTTPException(
                status_code=DEFAULT_ERROR_CODE, detail="User not found",
            )
    return str(user.id)
