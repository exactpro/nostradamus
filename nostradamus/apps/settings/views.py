from json import dumps

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from apps.extractor.main.connector import get_fields, get_unique_values
from apps.settings.main.common import (
    read_settings,
    get_filter_settings,
    get_qa_metrics_settings,
    update_resolutions,
    get_predictions_table_settings,
    check_issues_exist,
    split_values,
    get_bug_resolutions,
    get_source_field,
    get_mark_up_entities,
    update_source_field,
    update_bug_resolutions,
    update_mark_up_entities,
    remove_training_parameters,
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
)
from utils.redis import (
    redis_conn,
    remove_cache_record,
    clear_cache,
    clear_page_cache,
)


class FilterSettingsView(APIView):
    @swagger_auto_schema(
        responses={200: FiltersSettingsSerializer},
    )
    def get(self, request):
        check_issues_exist()

        filter_settings = get_filter_settings(request.user)
        names = sorted(get_fields())

        result = {"filter_settings": filter_settings, "names": names}

        return Response(result)

    @swagger_auto_schema(
        request_body=UserFilterSerializer,
        responses={200: UserFilterSerializer},
    )
    def post(self, request):
        check_issues_exist()

        request_data = request.data.copy()

        read_settings(request_data, request.user)

        filter_settings_serializer = UserFilterSerializer(
            data=request_data, many=True
        )
        filter_settings_serializer.is_valid(raise_exception=True)

        UserFilterSerializer.delete_old_filters(request_data[0]["settings"])
        filter_settings_serializer.save()

        clear_page_cache(["analysis_and_training"], request.user.id)

        return Response({"result": "success"})


class QAMetricsSettingsView(APIView):
    @swagger_auto_schema(
        responses={200: QAMetricsFiltersSettingsSerializer},
    )
    def get(self, request):
        check_issues_exist()

        qa_metrics_settings = get_qa_metrics_settings(request.user)
        names = sorted(get_fields())

        result = {"filter_settings": qa_metrics_settings, "names": names}

        return Response(result)

    @swagger_auto_schema(
        request_body=UserQAMetricsFilterSerializer,
        responses={200: UserQAMetricsFilterSerializer},
    )
    def post(self, request):
        check_issues_exist()

        request_data = request.data.copy()
        read_settings(request_data, request.user)

        settings_serializer = UserQAMetricsFilterSerializer(
            data=request_data, many=True
        )
        settings_serializer.is_valid(raise_exception=True)

        UserQAMetricsFilterSerializer.delete_old_filters(
            request_data[0]["settings"]
        )
        settings_serializer.save()

        remove_cache_record("qa_metrics:filters", request.user.id)

        redis_conn.set(
            f"user:{request.user.id}:settings:qa_metrics",
            dumps(get_qa_metrics_settings(request.user)),
        )

        return Response({"result": "success"})


class PredictionsTableSettingsView(APIView):
    @swagger_auto_schema(
        responses={200: PredictionsTableSettingsSerializer},
    )
    def get(self, request):
        check_issues_exist()

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
        check_issues_exist()

        request_data = request.data.copy()
        read_settings(request_data, request.user)

        settings_serializer = UserPredictionsTableSerializer(
            data=request_data, many=True
        )
        settings_serializer.is_valid(raise_exception=True)

        UserPredictionsTableSerializer.delete_old_fields(
            request_data[0]["settings"]
        )
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
        check_issues_exist()

        request_data = request.data.copy()
        user = request.user

        request_data["predictions_table"] = get_predictions_table_settings(
            user
        )

        request_data["source_field"] = get_source_field(user)

        update_resolutions(request_data, user)
        remove_cache_record("settings:predictions_table", user.id)

        training_serializer = UserTrainingSerializer(data=request_data)
        training_serializer.is_valid(raise_exception=True)

        update_bug_resolutions(
            user, training_serializer.data["bug_resolution"]
        )
        update_mark_up_entities(
            user, training_serializer.data["mark_up_entities"]
        )

        remove_training_parameters(user)

        return Response({"result": "success"})


class SourceFieldView(APIView):
    @swagger_auto_schema(
        responses={200: SourceFieldGetViewSerializer},
    )
    def get(self, request):
        check_issues_exist()

        source_field = get_source_field(request.user)
        source_field_names = sorted(get_fields())

        result = {
            "source_field": source_field,
            "source_field_names": source_field_names,
        }

        return Response(result)

    @swagger_auto_schema(request_body=SourceFieldSerializer)
    def post(self, request):

        source_field_serializer = SourceFieldSerializer(data=request.data)
        source_field_serializer.is_valid(raise_exception=True)

        update_source_field(request.user, source_field_serializer.data)
        remove_training_parameters(request.user)

        return Response({"result": "success"})


class MarkUpEntitiesView(APIView):
    @swagger_auto_schema(
        responses={200: MarkUpEntiitiesSerializer},
    )
    def get(self, request):
        check_issues_exist()

        mark_up_entities = get_mark_up_entities(request.user)
        source_field = get_source_field(request.user)

        if not source_field:
            return Response({})

        unique_values = get_unique_values(source_field)
        unique_values = split_values(unique_values)

        result = {
            "mark_up_entities": mark_up_entities,
            "entity_names": sorted(unique_values),
        }

        return Response(result)


class BugResolutionView(APIView):
    @swagger_auto_schema(
        responses={200: BugResolutionSettingsSerializer},
    )
    def get(self, request):
        check_issues_exist()

        resolution_settings = get_bug_resolutions(request.user)
        resolution = get_unique_values("Resolution")

        result = {
            "resolution_settings": resolution_settings,
            "resolution_names": resolution,
        }

        return Response(result)
