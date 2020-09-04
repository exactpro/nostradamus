from rest_framework import serializers

from apps.analysis_and_training.serializers import (
    FiltrationFieldRequestSerializer,
)


class RecordsCountSerializer(serializers.Serializer):
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


class QAMetricsFiltersContentSerializer(serializers.Serializer):
    filters = FiltrationFieldRequestSerializer(many=True)


class QAMetricsFiltersResultSerializer(QAMetricsFiltersContentSerializer):
    records_count = RecordsCountSerializer()


class QAMetricsTableRequestSerializer(serializers.Serializer):
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()


class QAMetricsSerializer(serializers.Serializer):
    records_count = RecordsCountSerializer()
