import re

from database import create_session
from models.User import User


def validate_email_uniqueness(email: str) -> None:
    """Validates the email for uniqueness.

    :param email: Email to be validated.
    """
    with create_session() as db:
        if db.query(User).filter(User.email == email).first():
            raise ValueError("Email already taken.")


def validate_email_pattern(email: str) -> None:
    """Validate the email for special characters.

    :param email: Email to be validated.
    """
    forbidden_symbols = re.compile(r"[№/!--:-?[-`{-~]")
    if forbidden_symbols.search(email):
        raise ValueError("Ensure that email doesn't have special characters.")
