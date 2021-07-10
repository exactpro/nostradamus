from rest_framework import serializers


class DescriptionAssessmentResponseSerializer(serializers.Serializer):
    priority = serializers.ListField(child=serializers.CharField())
    resolution = serializers.ListField(child=serializers.CharField())
    areas_of_testing = serializers.ListField(child=serializers.CharField())


class PredictorResponseSerializer(serializers.Serializer):
    priority = serializers.DictField(child=serializers.FloatField())
    resolution = serializers.DictField(child=serializers.FloatField())
    areas_of_testing = serializers.DictField(child=serializers.FloatField())
    time_to_resolve = serializers.DictField(child=serializers.FloatField())


class HighlightingResponseSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class PredictorRequestSerializer(serializers.Serializer):
    description = serializers.CharField()


class HighlightingRequestSerializer(serializers.Serializer):
    metric = serializers.CharField()
    value = serializers.CharField()
