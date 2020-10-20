from rest_framework import serializers


class AnalysisAndTrainingSerializer(serializers.Serializer):
    records_count = serializers.DictField(child=serializers.IntegerField())


class FiltrationFieldRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    filtration_type = serializers.CharField()
    current_value = serializers.CharField()
    exact_match = serializers.BooleanField(required=False)


class FilterResultSerializer(AnalysisAndTrainingSerializer):
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class FilterContentSerializer(serializers.Serializer):
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class FilterActionSerializer(FilterContentSerializer):
    action = serializers.CharField()


class StatisticsSerializer(serializers.Serializer):
    minimum = serializers.CharField()
    maximum = serializers.CharField()
    mean = serializers.CharField()
    std = serializers.CharField()


class SignificantTermsRequestSerializer(serializers.Serializer):
    metric = serializers.CharField()


class SignificantTermsResponseSerializer(serializers.Serializer):
    terms = serializers.DictField(child=serializers.IntegerField())


class SignificantTermsRenderContentSerializer(
    SignificantTermsResponseSerializer
):
    metrics = serializers.ListField(child=serializers.CharField())
    chosen_metric = serializers.CharField()


class SignificantTermsRenderSerializer(serializers.Serializer):
    significant_terms = SignificantTermsRenderContentSerializer()


class DefectSubmissionSerializer(serializers.Serializer):
    period = serializers.CharField()


class DefectSubmissionResponseSerializer(DefectSubmissionSerializer):
    created_line = serializers.DictField(child=serializers.IntegerField())
    resolved_line = serializers.DictField(child=serializers.IntegerField())
    created_total_count = serializers.IntegerField()
    resolved_total_count = serializers.IntegerField()


class FrequentlyTermsResponseSerializer(serializers.Serializer):
    frequently_terms = serializers.ListField(child=serializers.CharField())


class StatisticsResponseSerializer(serializers.Serializer):
    statistics = serializers.DictField(child=StatisticsSerializer())


class StatusResponseSerializer(serializers.Serializer):
    issues_exists = serializers.BooleanField()
