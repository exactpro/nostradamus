import re

from database import create_session
from models.User import User


def validate_name_pattern(name: str) -> None:
    """Validate the name for special characters.

    :param name: Name to be validated.
    """
    forbidden_symbols = re.compile(r"[-№`/!-,:-@[-^{-~]")
    if forbidden_symbols.search(name):
        raise ValueError("Ensure that name doesn't have special symbols.")


def validate_name_uniqueness(name: str) -> None:
    """Validates the name for uniqueness.

    :param name: Name to be validated.
    """
    with create_session() as db:
        if db.query(User).filter(User.name == name).first():
            raise ValueError("Name already taken.")
