import re


def validate_symbols_count(
    string: str,
    field_name: str,
    maximum: int,
    minimum: int = 0,
) -> None:
    """Validates the field string for minimum and maximum length.

    :param string: String to be validated.
    :param field_name: Field name.
    :param maximum: Maximum length.
    :param minimum: Minimum length.
    """
    if len(string) > maximum:
        raise ValueError(
            f"Ensure {field_name} cannot be longer than {maximum} symbols."
        )
    if len(string) < minimum:
        raise ValueError(
            f"Ensure {field_name} cannot be less than {minimum} symbol(s)."
        )


def validate_for_whitespace(string: str, field_name: str) -> None:
    """Validates the string for containing whitespaces.

    :param string: String to be validated.
    :param field_name: Name of the field under validation.
    """
    pattern = re.compile(r"\s")
    if pattern.search(string):
        raise ValueError(f"{field_name.capitalize()} cannot contain whitespaces.")
