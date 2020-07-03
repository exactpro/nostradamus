from rest_framework import serializers


class FiltrationFieldRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    filtration_type = serializers.CharField()
    current_value = serializers.CharField()
    exact_match = serializers.BooleanField(required=False)


class FilterRequestSerializer(serializers.Serializer):
    action = serializers.CharField()
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class FiltrationFieldResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    filtration_type = serializers.CharField(write_only=True)
    values = serializers.ListField(
        child=serializers.CharField(), required=False
    )


class FilterResponseSerializer(serializers.Serializer):
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


class SignificantTermsRenderResponseSerializer(serializers.Serializer):
    metrics = serializers.ListField(child=serializers.CharField())
    chosen_metric = serializers.CharField()
    terms = serializers.DictField(child=serializers.IntegerField())


class AnalysisAndTrainingSerializer(serializers.Serializer):
    records_count = serializers.DictField(child=serializers.IntegerField())
    frequently_terms = serializers.ListField(child=serializers.CharField())
    statistics = serializers.DictField(child=StatisticsSerializer())
    submission_chart = serializers.DictField(child=serializers.IntegerField())
    significant_terms = SignificantTermsRenderResponseSerializer()
    filters = serializers.ListField(child=FiltrationFieldRequestSerializer())


class BugTrackerLoginSerializer(serializers.Serializer):
    link = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()


class DefectSubmissionSerializer(serializers.Serializer):
    period = serializers.CharField()


class DefectSubmissionResponseSerializer(serializers.Serializer):
    submission_chart = serializers.DictField(child=serializers.IntegerField())
