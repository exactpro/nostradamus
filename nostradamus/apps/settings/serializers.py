from rest_framework import serializers

from apps.settings.models import (
    UserFilter,
    UserQAMetricsFilter,
    UserPredictionsTable,
)
from apps.settings.validators import default_fields_validator


class UserFilterSerializer(serializers.ModelSerializer):
    filtration_types = [
        ("string", "String"),
        ("drop-down", "Drop-down"),
        ("numeric", "Numeric"),
        ("date", "Date"),
    ]

    settings = serializers.IntegerField(required=True, write_only=True)
    name = serializers.CharField(max_length=128, required=True)
    filtration_type = serializers.ChoiceField(
        choices=filtration_types, required=True
    )

    class Meta:
        model = UserFilter
        fields = ("name", "filtration_type", "settings")

    def create(self, validated_data):
        UserFilter.objects.create(
            settings_id=validated_data.pop("settings"), **validated_data
        )

    @staticmethod
    def delete_old_filters(settings):
        UserFilter.objects.filter(settings=settings).delete()


class UserQAMetricsFilterSerializer(serializers.ModelSerializer):
    filtration_types = [
        ("string", "String"),
        ("drop-down", "Drop-down"),
        ("numeric", "Numeric"),
        ("date", "Date"),
    ]

    settings = serializers.IntegerField(required=True, write_only=True)
    name = serializers.CharField(max_length=128, required=True)
    filtration_type = serializers.ChoiceField(
        choices=filtration_types, required=True
    )

    class Meta:
        model = UserQAMetricsFilter
        fields = ("name", "filtration_type", "settings")

    def create(self, validated_data):
        UserQAMetricsFilter.objects.create(
            settings_id=validated_data.pop("settings"), **validated_data
        )

    @staticmethod
    def delete_old_filters(settings):
        UserQAMetricsFilter.objects.filter(settings=settings).delete()


class UserPredictionsTableSerializer(serializers.ModelSerializer):
    settings = serializers.IntegerField(required=True, write_only=True)
    name = serializers.CharField(max_length=128, required=True)
    is_default = serializers.BooleanField(default=False)
    position = serializers.IntegerField(required=True)

    def validate(self, data):
        default_fields_validator(data["name"], data["is_default"])
        return data

    class Meta:
        model = UserPredictionsTable
        fields = ("name", "is_default", "position", "settings")

    def create(self, validated_data):
        UserPredictionsTable.objects.create(
            settings_id=validated_data.pop("settings"), **validated_data
        )

    @staticmethod
    def delete_old_fields(settings):
        UserPredictionsTable.objects.filter(settings=settings).delete()


class EntityListSerializer(serializers.ListField):
    entity = serializers.CharField(max_length=128)


class MarkUpEntitySerializer(serializers.Serializer):
    area_of_testing = serializers.CharField(max_length=128)
    entities = EntityListSerializer()


class BugResolutionSerializer(serializers.Serializer):
    metric = serializers.CharField(max_length=128, default="Resolution")
    value = serializers.CharField(max_length=128)


class UserTrainingSerializer(serializers.Serializer):
    mark_up_source = serializers.CharField(max_length=128, allow_blank=True)
    mark_up_entities = MarkUpEntitySerializer(many=True)
    bug_resolution = BugResolutionSerializer(many=True)
