import re

from rest_framework import serializers
from string import whitespace

from apps.authentication.models import User


def name_whitespaces_validator(value):
    whitespaces_regex = re.compile(f"[{whitespace}]")

    if whitespaces_regex.search(value):
        raise serializers.ValidationError(
            "Ensure that username doesn't have whitespaces."
        )


def password_whitespaces_validator(value):
    whitespaces_regex = re.compile(f"[{whitespace}]")

    if whitespaces_regex.search(value):
        raise serializers.ValidationError(
            "Ensure that password doesn't have whitespaces."
        )


def email_whitespaces_validator(value):
    whitespaces_regex = re.compile(f"[{whitespace}]")

    if whitespaces_regex.search(value):
        raise serializers.ValidationError(
            "Ensure that email doesn't have whitespaces."
        )


def name_special_symbols_validator(value):
    special_symbols_regex = re.compile(r"[-№`/!-,:-@[-^{-~]")

    if special_symbols_regex.search(value):
        raise serializers.ValidationError(
            "Ensure that name doesn't have special symbols."
        )


def email_validator(value):
    email_regex = re.compile(r"[№/!--:-?[-`{-~]")

    if email_regex.search(value):
        raise serializers.ValidationError(
            "Ensure that email doesn't have special characters."
        )


def unique_user_name(value):
    user = User.objects.filter(name__iexact=value)

    if user:
        raise serializers.ValidationError(
            "User with this name already exists."
        )


def unique_user_email(value):
    user = User.objects.filter(email__iexact=value)

    if user:
        raise serializers.ValidationError(
            "User with this email already exists."
        )
