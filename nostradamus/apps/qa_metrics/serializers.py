from rest_framework import serializers

from apps.analysis_and_training.serializers import (
    FiltrationFieldRequestSerializer,
)


class RecordsCountSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    filtered = serializers.IntegerField()


class PredictionsInfoSerializer(serializers.Serializer):
    records_count = RecordsCountSerializer()
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


class QAMetricsFiltersSerializer(serializers.Serializer):
    filters = FiltrationFieldRequestSerializer(many=True)


class QAMetricsTableRequestSerializer(serializers.Serializer):
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
