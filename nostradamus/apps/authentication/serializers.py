from collections import OrderedDict

from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers

from apps.authentication.models import Team, User
from apps.authentication.validators import (
    password_whitespaces_validator,
    name_whitespaces_validator,
    email_whitespaces_validator,
    name_special_symbols_validator,
    email_validator,
    unique_user_name,
    unique_user_email,
)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "name",
        )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[
            MinLengthValidator(limit_value=6),
            MaxLengthValidator(limit_value=254),
            password_whitespaces_validator,
        ],
    )
    name = serializers.CharField(
        validators=[
            name_whitespaces_validator,
            unique_user_name,
            MaxLengthValidator(limit_value=64),
            name_special_symbols_validator,
        ]
    )
    email = serializers.EmailField(
        validators=[
            email_whitespaces_validator,
            unique_user_email,
            MaxLengthValidator(limit_value=254),
            email_validator,
        ]
    )
    team = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password", "team")

    def create(self, validated_data: OrderedDict) -> User:
        """ Creates new User instance when calling serializer.save() method.

        Parameters:
        ----------
        validated_data:
            Serializer property created while user_serializer.is_valid() method
            calling.

        Returns:
        ----------
            User instance.
        """

        user_instance = User(
            name=validated_data["name"],
            username=validated_data["name"],
            email=validated_data["email"],
        )
        user_instance.set_password(validated_data["password"])
        user_instance.save()

        return user_instance

    def get_team(self) -> Team:
        return Team.objects.get(id=self.validated_data["team"])


class AuthRequestSerializer(serializers.Serializer):
    credentials = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def get_credentials(self) -> tuple:
        return (
            self.validated_data["credentials"].lower(),
            self.validated_data["password"],
        )


class AuthResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    team = serializers.CharField()
    role = serializers.CharField()
    token = serializers.CharField()
