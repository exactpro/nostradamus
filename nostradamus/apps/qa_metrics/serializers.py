from rest_framework import serializers

from apps.analysis_and_training.serializers import (
    FiltrationFieldRequestSerializer,
)


class QAMetricsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    filtered = serializers.IntegerField()


class PredictionsInfoSerializer(serializers.Serializer):
    predictions_table = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )
    prediction_table_rows_count = serializers.IntegerField()
    areas_of_testing_chart = serializers.DictField(
        child=serializers.IntegerField()
    )
    priority_chart = serializers.DictField(child=serializers.IntegerField())
    ttr_chart = serializers.DictField(child=serializers.IntegerField())
    resolution_chart = serializers.DictField(
        child=serializers.DictField(child=serializers.IntegerField())
    )


class PredictionsTableSerializer(serializers.ListSerializer):
    child = serializers.DictField(child=serializers.CharField())


class QAMetricsFiltersContentSerializer(serializers.ListSerializer):
    child = FiltrationFieldRequestSerializer()


class QAMetricsFiltersActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    filters = serializers.ListSerializer(
        child=FiltrationFieldRequestSerializer()
    )


class QAMetricsFiltersResultSerializer(serializers.Serializer):
    records_count = QAMetricsSerializer()
    filters = serializers.ListSerializer(
        child=FiltrationFieldRequestSerializer()
    )


class QAMetricsTableRequestSerializer(serializers.Serializer):
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
