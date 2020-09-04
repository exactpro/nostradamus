from json import dumps

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from apps.extractor.main.connector import get_fields, get_unique_values
from apps.settings.main.common import (
    read_settings,
    get_filter_settings,
    get_qa_metrics_settings,
    get_training_settings,
    update_resolutions,
    update_training_settings,
    get_predictions_table_settings,
    check_loaded_issues,
    split_values,
)
from apps.settings.serializers import (
    UserFilterSerializer,
    UserQAMetricsFilterSerializer,
    UserTrainingSerializer,
    UserPredictionsTableSerializer,
    SourceFieldSerializer,
    SourceFieldGetViewSerializer,
    MarkUpEntiitiesSerializer,
    PredictionsTableSettingsSerializer,
    QAMetricsFiltersSettingsSerializer,
    BugResolutionSettingsSerializer,
    FiltersSettingsSerializer,
    TrainingSettingsPostSerializer,
)
from utils.redis import (
    redis_conn,
    remove_cache_record,
    clear_cache,
    clear_page_cache,
)


class FilterSettingsView(APIView):
    @swagger_auto_schema(responses={200: FiltersSettingsSerializer},)
    def get(self, request):
        check_loaded_issues()

        filter_settings = get_filter_settings(request.user)
        names = sorted(get_fields())

        result = {"filter_settings": filter_settings, "names": names}

        return Response(result)

    @swagger_auto_schema(
        request_body=UserFilterSerializer,
        responses={200: UserFilterSerializer},
    )
    def post(self, request):
        check_loaded_issues()

        data = request.data.copy()

        read_settings(data, request.user)

        filter_settings_serializer = UserFilterSerializer(data=data, many=True)
        filter_settings_serializer.is_valid(raise_exception=True)

        UserFilterSerializer.delete_old_filters(data[0]["settings"])
        filter_settings_serializer.save()

        clear_page_cache(["analysis_and_training"], request.user.id)

        return Response({"result": "success"})


class QAMetricsSettingsView(APIView):
    @swagger_auto_schema(responses={200: QAMetricsFiltersSettingsSerializer},)
    def get(self, request):
        check_loaded_issues()

        qa_metrics_settings = get_qa_metrics_settings(request.user)
        names = sorted(get_fields())

        result = {"filter_settings": qa_metrics_settings, "names": names}

        return Response(result)

    @swagger_auto_schema(
        request_body=UserQAMetricsFilterSerializer,
        responses={200: UserQAMetricsFilterSerializer},
    )
    def post(self, request):
        check_loaded_issues()

        data = request.data.copy()
        read_settings(data, request.user)

        settings_serializer = UserQAMetricsFilterSerializer(
            data=data, many=True
        )
        settings_serializer.is_valid(raise_exception=True)

        UserQAMetricsFilterSerializer.delete_old_filters(data[0]["settings"])
        settings_serializer.save()

        remove_cache_record("qa_metrics:filters", request.user.id)

        redis_conn.set(
            f"user:{request.user.id}:settings:qa_metrics",
            dumps(get_qa_metrics_settings(request.user)),
        )

        return Response({"result": "success"})


class PredictionsTableSettingsView(APIView):
    @swagger_auto_schema(responses={200: PredictionsTableSettingsSerializer},)
    def get(self, request):
        check_loaded_issues()

        predictions_table_settings = get_predictions_table_settings(
            request.user
        )

        result = {
            "predictions_table_settings": predictions_table_settings,
            "field_names": sorted(get_fields()),
        }

        return Response(result)

    @swagger_auto_schema(
        request_body=UserPredictionsTableSerializer,
        responses={200: UserPredictionsTableSerializer},
    )
    def post(self, request):
        check_loaded_issues()

        data = request.data.copy()
        read_settings(data, request.user)

        settings_serializer = UserPredictionsTableSerializer(
            data=data, many=True
        )
        settings_serializer.is_valid(raise_exception=True)

        UserPredictionsTableSerializer.delete_old_fields(data[0]["settings"])
        settings_serializer.save()

        clear_cache(
            ["qa_metrics:predictions_page", "qa_metrics:predictions_table"],
            request.user.id,
        )

        return Response({"result": "success"})


class TrainingSettingsView(APIView):
    @swagger_auto_schema(
        request_body=UserTrainingSerializer,
        responses={200: UserTrainingSerializer},
    )
    def post(self, request):
        check_loaded_issues()

        data = request.data.copy()

        data["predictions_table"] = get_predictions_table_settings(
            request.user
        )
        data["source_field"] = get_training_settings(request.user)[
            "source_field"
        ]
        update_resolutions(data, request.user)
        remove_cache_record("settings:predictions_table", request.user.id)

        training_serializer = TrainingSettingsPostSerializer(data=data)
        training_serializer.is_valid(raise_exception=True)

        update_training_settings(training_serializer.data, request.user)

        return Response({"result": "success"})


class SourceFieldView(APIView):
    @swagger_auto_schema(responses={200: SourceFieldGetViewSerializer},)
    def get(self, request):
        check_loaded_issues()

        training_settings = get_training_settings(request.user)
        source_field_names = sorted(get_fields())

        result = {
            "source_field": training_settings.get("source_field", ""),
            "source_field_names": source_field_names,
        }

        return Response(result)

    @swagger_auto_schema(request_body=SourceFieldSerializer)
    def post(self, request):
        training_settings = get_training_settings(request.user)

        source_field_serializer = SourceFieldSerializer(data=request.data)
        source_field_serializer.is_valid(raise_exception=True)

        training_settings["source_field"] = source_field_serializer.data.get(
            "source_field"
        )

        update_training_settings(training_settings, request.user)

        return Response({"result": "success"})


class MarkUpEntitiesView(APIView):
    @swagger_auto_schema(responses={200: MarkUpEntiitiesSerializer},)
    def get(self, request):
        check_loaded_issues()

        training_settings = get_training_settings(request.user)
        source_field = training_settings.get("source_field", "")

        if not source_field:
            return Response({})

        unique_values = get_unique_values(source_field)
        unique_values = split_values(unique_values)

        result = {
            "mark_up_entities": training_settings["mark_up_entities"],
            "entity_names": sorted(unique_values),
        }

        return Response(result)


class BugResolutionView(APIView):
    @swagger_auto_schema(responses={200: BugResolutionSettingsSerializer},)
    def get(self, request):
        check_loaded_issues()

        resolution_settings = get_training_settings(request.user)[
            "bug_resolution"
        ]
        resolution = get_unique_values("Resolution")

        result = {
            "resolution_settings": resolution_settings,
            "resolution_names": resolution,
        }

        return Response(result)
