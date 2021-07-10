import pytest

from validators.validators import validate_symbols_count, validate_for_whitespace


def test_validate_max_symbols():
    """Negative test of validate max symbols in string."""
    string = "abcdefgh123456"
    with pytest.raises(ValueError) as exception_info:
        validate_symbols_count(string, "password", 10)

    assert "Ensure password cannot be longer than 10 symbols." == str(exception_info.value)


def test_validate_min_symbols():
    """Negative test of validate min symbols in string."""
    string = "12345"
    with pytest.raises(ValueError) as exception_info:
        validate_symbols_count(string, "password", 256, 6)

    assert "Ensure password cannot be less than 6 symbol(s)." == str(exception_info.value)


def test_validate_symbols_positive():
    """Positive test of validate symbols in string."""
    string = "123456789"
    validate_symbols_count(string, "password", 256, 6)


def test_validate_whitespace_negative():
    """Negative test of validate whitespace in string."""
    string = "test test test"
    with pytest.raises(ValueError) as exception_info:
        validate_for_whitespace(string, "name")

    assert "Name cannot contain whitespaces." == str(exception_info.value)


def test_validate_whitespace_positive():
    """Positive test of validate whitespace in string."""
    string = "test_test_test"
    validate_for_whitespace(string, "name")