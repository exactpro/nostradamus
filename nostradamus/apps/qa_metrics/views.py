from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analysis_and_training.main.filter import update_drop_down_fields
from apps.extractor.main.connector import get_issues
from apps.qa_metrics.main.charts import (
    calculate_aot_percentage,
    calculate_priority_percentage,
    calculate_ttr_percentage,
    calculate_resolution_percentage,
)
from apps.qa_metrics.main.predictions_table import (
    get_predictions_table,
    check_predictions,
    paginate_bugs,
    get_qa_metrics_fields,
)
from apps.analysis_and_training.main.training import check_training_files
from apps.qa_metrics.serializers import (
    PredictionsInfoSerializer,
    PredictionsTableSerializer,
    QAMetricsFiltersSerializer,
    QAMetricsTableRequestSerializer,
)
from apps.settings.main.archiver import get_archive_path, read_from_archive
from apps.settings.main.common import (
    get_qa_metrics_settings,
    get_predictions_table_settings,
)
from utils.const import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    TRAINING_PARAMETERS_FILENAME,
    UNRESOLVED_BUGS_FILTER,
)

from pandas import DataFrame


class QAMetricsView(APIView):
    @swagger_auto_schema(responses={200: QAMetricsFiltersSerializer},)
    def get(self, request):
        user = request.user

        check_training_files(user)
        check_predictions()

        fields = get_qa_metrics_fields(user)
        issues = DataFrame.from_records(
            get_issues(filters=[UNRESOLVED_BUGS_FILTER], fields=fields)
        )

        filters = get_qa_metrics_settings(user)
        filters = update_drop_down_fields(filters, issues)

        return Response(filters)


class PredictionsInfoView(APIView):
    @swagger_auto_schema(
        request_body=QAMetricsFiltersSerializer,
        responses={200: PredictionsInfoSerializer},
    )
    def post(self, request):
        user = request.user
        filters = request.data.get("filters", [])
        offset = DEFAULT_OFFSET
        limit = DEFAULT_LIMIT

        check_training_files(user)
        check_predictions()

        archive_path = get_archive_path(user)
        training_parameters = read_from_archive(
            archive_path, TRAINING_PARAMETERS_FILENAME
        )

        predictions_table_settings = get_predictions_table_settings(user)
        predictions = get_predictions_table(
            predictions_table_settings, filters, None, None
        )

        if predictions.empty:
            return Response({})

        prediction_table = paginate_bugs(predictions, offset, limit)

        areas_of_testing_percentage = calculate_aot_percentage(
            predictions["Area of Testing"]
        )
        priority_percentage = calculate_priority_percentage(
            predictions["Priority"], training_parameters["Priority"]
        )
        ttr_percentage = calculate_ttr_percentage(
            predictions["Time to Resolve"],
            training_parameters["Time to Resolve"],
        )

        resolution_percentage = calculate_resolution_percentage(
            predictions, training_parameters["Resolution"]
        )

        result = {
            "predictions_table": prediction_table.T.to_dict().values(),
            "prediction_table_rows_count": len(predictions),
            "areas_of_testing_chart": areas_of_testing_percentage,
            "priority_chart": priority_percentage,
            "ttr_chart": ttr_percentage,
            "resolution_chart": resolution_percentage,
        }

        return Response(result)


class PredictionsTableView(APIView):
    @swagger_auto_schema(
        request_body=QAMetricsTableRequestSerializer,
        responses={200: PredictionsTableSerializer},
    )
    def post(self, request):
        user = request.user
        filters = request.data.get("filters", [])
        offset = int(request.data.get("offset", DEFAULT_OFFSET))
        limit = int(request.data.get("limit", DEFAULT_LIMIT))

        check_training_files(user)
        check_predictions()

        predictions_table_settings = get_predictions_table_settings(user)
        bugs_predictions = get_predictions_table(
            predictions_table_settings, filters, offset, limit
        )

        return Response(bugs_predictions.to_dict("records"))
