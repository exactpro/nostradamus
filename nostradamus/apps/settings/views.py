from json import dumps, loads

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from apps.settings.main.common import (
    read_settings,
    get_filter_settings,
    get_qa_metrics_settings,
    get_training_settings,
    update_resolutions,
    update_training_settings,
    get_predictions_table_settings,
)
from apps.settings.serializers import (
    UserFilterSerializer,
    UserQAMetricsFilterSerializer,
    UserTrainingSerializer,
    UserPredictionsTableSerializer,
)
from utils.redis import redis_conn, clear_cache


class FilterSettingsView(APIView):
    @swagger_auto_schema(responses={200: UserFilterSerializer},)
    def get(self, request):
        filter_settings = get_filter_settings(request.user)

        return Response(filter_settings)

    @swagger_auto_schema(
        request_body=UserFilterSerializer,
        responses={200: UserFilterSerializer},
    )
    def post(self, request):
        data = request.data.copy()
        read_settings(data, request.user)

        filter_settings_serializer = UserFilterSerializer(data=data, many=True)
        filter_settings_serializer.is_valid(raise_exception=True)

        UserFilterSerializer.delete_old_filters(data[0]["settings"])
        filter_settings_serializer.save()

        clear_cache()

        return Response({"result": "success"})


class QAMetricsSettingsView(APIView):
    @swagger_auto_schema(responses={200: UserQAMetricsFilterSerializer},)
    def get(self, request):
        cached_settings = redis_conn.get(
            f"settings:qa_metrics:{request.user.id}"
        )
        if cached_settings:
            return Response(loads(cached_settings))

        qa_metrics_settings = get_qa_metrics_settings(request.user)
        redis_conn.set(
            f"settings:qa_metrics:{request.user.id}",
            dumps(qa_metrics_settings),
        )

        return Response(qa_metrics_settings)

    @swagger_auto_schema(
        request_body=UserQAMetricsFilterSerializer,
        responses={200: UserQAMetricsFilterSerializer},
    )
    def post(self, request):
        data = request.data.copy()
        read_settings(data, request.user)

        settings_serializer = UserQAMetricsFilterSerializer(
            data=data, many=True
        )
        settings_serializer.is_valid(raise_exception=True)

        UserQAMetricsFilterSerializer.delete_old_filters(data[0]["settings"])
        settings_serializer.save()

        redis_conn.set(
            f"settings:qa_metrics:{request.user.id}",
            dumps(get_qa_metrics_settings(request.user)),
        )

        return Response({"result": "success"})


class PredictionsTableSettingsView(APIView):
    @swagger_auto_schema(responses={200: UserPredictionsTableSerializer},)
    def get(self, request):
        cached_settings = redis_conn.get(
            f"settings:predictions_table:{request.user.id}"
        )
        if cached_settings:
            return Response(loads(cached_settings))

        predictions_table_settings = get_predictions_table_settings(
            request.user
        )
        redis_conn.set(
            f"settings:predictions_table:{request.user.id}",
            dumps(predictions_table_settings),
        )

        return Response(predictions_table_settings)

    @swagger_auto_schema(
        request_body=UserPredictionsTableSerializer,
        responses={200: UserPredictionsTableSerializer},
    )
    def post(self, request):
        data = request.data.copy()

        settings_serializer = UserPredictionsTableSerializer(
            data=data, many=True
        )
        settings_serializer.is_valid(raise_exception=True)

        UserPredictionsTableSerializer.delete_old_fields(data[0]["settings"])
        settings_serializer.save()

        redis_conn.set(
            f"settings:predictions_table:{request.user.id}",
            dumps(get_predictions_table_settings(request.user)),
        )

        return Response({"result": "success"})


class TrainingSettingsView(APIView):
    @swagger_auto_schema(responses={200: UserTrainingSerializer},)
    def get(self, request):
        training_settings = get_training_settings(request.user)

        return Response(training_settings)

    @swagger_auto_schema(
        request_body=UserTrainingSerializer,
        responses={200: UserTrainingSerializer},
    )
    def post(self, request):
        data = request.data.copy()

        data["predictions_table"] = get_predictions_table_settings(
            request.user
        )
        update_resolutions(data, request.user)
        redis_conn.delete(f"settings:predictions_table:{request.user.id}")

        training_serializer = UserTrainingSerializer(data=data)
        training_serializer.is_valid(raise_exception=True)

        update_training_settings(training_serializer.data, request.user)

        return Response({"result": "success"})
