from rest_framework import serializers


class AnalysisAndTrainingSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    filtered = serializers.IntegerField()


class FiltrationFieldRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    current_value = serializers.ListSerializer(
        child=serializers.CharField(), required=False
    )
    values = serializers.ListSerializer(
        child=serializers.CharField(), required=False
    )
    exact_match = serializers.BooleanField(required=False)


class FilterResultSerializer(serializers.Serializer):
    records_count = AnalysisAndTrainingSerializer()
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class FilterContentSerializer(serializers.ListSerializer):
    child = FiltrationFieldRequestSerializer()


class FilterActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class StatisticsSerializer(serializers.Serializer):
    max = serializers.CharField()
    mean = serializers.CharField()
    min = serializers.CharField()
    std = serializers.CharField()


class SignificantTermsRequestSerializer(serializers.Serializer):
    metric = serializers.CharField()


class SignificantTermsResponseSerializer(serializers.Serializer):
    terms = serializers.DictField(child=serializers.IntegerField())


class SignificantTermsGetResponseSerializer(
    SignificantTermsResponseSerializer
):
    metrics = serializers.ListField(child=serializers.CharField())
    chosen_metric = serializers.CharField()


class SignificantTermsPostResponseSerializer(serializers.Serializer):
    term = serializers.IntegerField()


class DefectSubmissionSerializer(serializers.Serializer):
    period = serializers.CharField(required=False)


class DefectSubmissionResponseSerializer(DefectSubmissionSerializer):
    created_line = serializers.DictField(child=serializers.IntegerField())
    resolved_line = serializers.DictField(child=serializers.IntegerField())
    created_total_count = serializers.IntegerField()
    resolved_total_count = serializers.IntegerField()


class FrequentlyTermsResponseSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class StatisticsResponseSerializer(serializers.Serializer):
    series_name = StatisticsSerializer()


class StatusResponseSerializer(serializers.Serializer):
    issues_exists = serializers.BooleanField()
