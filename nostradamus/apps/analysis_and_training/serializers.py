from rest_framework import serializers


class FiltrationFieldRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    filtration_type = serializers.CharField()
    current_value = serializers.CharField()
    exact_match = serializers.BooleanField(required=False)


class FilterActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class FilterResultSerializer(serializers.Serializer):
    records_count = serializers.DictField(child=serializers.IntegerField())
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class FiltrationFieldResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    filtration_type = serializers.CharField(write_only=True)
    values = serializers.ListField(
        child=serializers.CharField(), required=False
    )


class FilterContentSerializer(serializers.Serializer):
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class StatisticsSerializer(serializers.Serializer):
    minimum = serializers.CharField()
    maximum = serializers.CharField()
    mean = serializers.CharField()
    std = serializers.CharField()


class SignificantTermsRequestSerializer(serializers.Serializer):
    metric = serializers.CharField()


class SignificantTermsResponseSerializer(serializers.Serializer):
    terms = serializers.DictField(child=serializers.IntegerField())


class SignificantTermsRenderContentSerializer(serializers.Serializer):
    metrics = serializers.ListField(child=serializers.CharField())
    chosen_metric = serializers.CharField()
    terms = serializers.DictField(child=serializers.IntegerField())


class SignificantTermsRenderSerializer(serializers.Serializer):
    significant_terms = SignificantTermsRenderContentSerializer()


class AnalysisAndTrainingSerializer(serializers.Serializer):
    records_count = serializers.DictField(child=serializers.IntegerField())


class BugTrackerLoginSerializer(serializers.Serializer):
    link = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()


class DefectSubmissionSerializer(serializers.Serializer):
    period = serializers.CharField()


class DefectSubmissionResponseSerializer(serializers.Serializer):
    defect_submission = serializers.DictField(child=serializers.IntegerField())
    period = serializers.CharField()


class FrequentlyTermsResponseSerializer(serializers.Serializer):
    frequently_terms = serializers.ListField(child=serializers.CharField())


class StatisticsResponseSerializer(serializers.Serializer):
    statistics = serializers.DictField(child=StatisticsSerializer())
