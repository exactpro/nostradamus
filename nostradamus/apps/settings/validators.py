from rest_framework import serializers

from utils.const import DEFAULT_PREDICTIONS_TABLE_FIELDS


def default_fields_validator(name: str, value: bool) -> None:
    """Raises validation error when specified field have
    incorrect is_default value.

    :param name: Predictions table field name.
    :param value: True if marked as is_default, otherwise False.
    """
    if name in DEFAULT_PREDICTIONS_TABLE_FIELDS or name.startswith(
        "Resolution:"
    ):
        if not value:
            raise serializers.ValidationError(
                f"Field with name '{name}' should be marked as default"
            )
    else:
        if value:
            raise serializers.ValidationError(
                f"Field with name {name} can't be marked as default"
            )
