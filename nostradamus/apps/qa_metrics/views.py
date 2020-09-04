import json
from json import dumps, loads
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analysis_and_training.main.filter import update_drop_down_fields
from apps.extractor.main.connector import get_issue_count
from apps.qa_metrics.main.charts import (
    calculate_aot_percentage,
    calculate_priority_percentage,
    calculate_ttr_percentage,
    calculate_resolution_percentage,
)
from apps.qa_metrics.main.predictions_table import (
    get_predictions_table,
    paginate_bugs,
    calculate_issues_predictions,
    get_predictions_table_fields,
)
from apps.analysis_and_training.main.training import check_training_files
from apps.qa_metrics.serializers import (
    PredictionsInfoSerializer,
    PredictionsTableSerializer,
    QAMetricsFiltersContentSerializer,
    QAMetricsFiltersResultSerializer,
    QAMetricsTableRequestSerializer,
    QAMetricsSerializer,
)
from apps.settings.main.archiver import get_archive_path, read_from_archive
from apps.settings.main.common import (
    get_qa_metrics_settings,
    check_filters_equality,
)
from utils.const import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    TRAINING_PARAMETERS_FILENAME,
    UNRESOLVED_BUGS_FILTER,
)
from apps.extractor.main.preprocessor import get_issues_dataframe
from utils.redis import redis_conn, clear_cache

from pandas import DataFrame


class QAMetricsView(APIView):
    @swagger_auto_schema(
        operation_description="QA metrics.",
        responses={200: QAMetricsSerializer},
    )
    def get(self, request):
        total_count = get_issue_count(filters=[UNRESOLVED_BUGS_FILTER])

        if not total_count:
            Response({})

        cache = redis_conn.get(f"user:{request.user.id}:qa_metrics:filters")

        filters = [UNRESOLVED_BUGS_FILTER]
        if cache:
            filters = loads(cache)

        context = {
            "records_count": {
                "total": total_count,
                "filtered": get_issue_count(filters),
            },
        }
        return Response(context)


class QAMetricsFilterView(APIView):
    @swagger_auto_schema(
        operation_description="Filters card content.",
        responses={200: QAMetricsFiltersContentSerializer},
    )
    def get(self, request):
        user = request.user

        check_training_files(user)

        cached_filters = redis_conn.get(
            f"user:{request.user.id}:qa_metrics:filters"
        )
        if cached_filters:
            filters = loads(cached_filters)
        else:
            filters = get_qa_metrics_settings(user)
            fields = [field["name"] for field in filters]

            issues = get_issues_dataframe(
                fields=fields, filters=[UNRESOLVED_BUGS_FILTER]
            )
            filters = update_drop_down_fields(filters, issues)

        return Response(filters)

    @swagger_auto_schema(
        operation_description="Apply or Clear filters.",
        request_body=QAMetricsFiltersContentSerializer,
        responses={200: QAMetricsFiltersResultSerializer},
    )
    def post(self, request):
        new_filters = request.data.get("filters", [])
        filters = get_qa_metrics_settings(request.user)
        fields = [field["name"] for field in filters]
        filters = update_drop_down_fields(
            filters,
            get_issues_dataframe(
                fields=fields, filters=[UNRESOLVED_BUGS_FILTER]
            ),
        )

        if new_filters:
            for new_filter in new_filters:
                for filter_ in filters:
                    if new_filter["name"] == filter_["name"]:
                        filter_.update(
                            {
                                "current_value": new_filter["current_value"],
                                "filtration_type": new_filter[
                                    "filtration_type"
                                ],
                                "exact_match": new_filter["exact_match"],
                            }
                        )
        filters += [UNRESOLVED_BUGS_FILTER]

        cached_filters = redis_conn.get(
            f"user:{request.user.id}:qa_metrics:filters"
        )
        cached_filters = loads(cached_filters) if cached_filters else []

        context = {
            "records_count": {
                "total": get_issue_count(filters=[UNRESOLVED_BUGS_FILTER]),
                "filtered": get_issue_count(filters),
            },
            "filters": filters,
        }

        if not cached_filters or not check_filters_equality(
            filters, cached_filters
        ):
            clear_cache(
                [
                    "qa_metrics:predictions_table",
                    "qa_metrics:predictions_page",
                ],
                request.user.id,
            )
            for element in context:
                redis_conn.set(
                    f"user:{request.user.id}:qa_metrics:{element}",
                    dumps(context.get(element)),
                )

        return Response(context)


class PredictionsInfoView(APIView):
    @swagger_auto_schema(
        operation_description="Predictions Info cards content.",
        responses={200: PredictionsInfoSerializer},
    )
    def get(self, request):
        user = request.user
        offset = DEFAULT_OFFSET
        limit = DEFAULT_LIMIT

        cached_predictions = redis_conn.get(
            f"user:{request.user.id}:qa_metrics:predictions_page"
        )
        cached_filters = redis_conn.get(
            f"user:{request.user.id}:qa_metrics:filters"
        )
        filters = (
            loads(cached_filters)
            if cached_filters
            else [UNRESOLVED_BUGS_FILTER]
        )

        if cached_predictions:
            predictions = loads(cached_predictions)
        else:
            check_training_files(user)

            archive_path = get_archive_path(user)
            training_parameters = read_from_archive(
                archive_path, TRAINING_PARAMETERS_FILENAME
            )

            predictions_table_fields = get_predictions_table_fields(user)

            issues = calculate_issues_predictions(
                user, predictions_table_fields, filters
            )

            if issues.empty:
                return Response({})

            predictions_table_fields.remove("Description_tr")
            predictions_table_fields.remove("Key")

            predictions_table = get_predictions_table(
                issues=issues,
                fields_settings=predictions_table_fields,
                offset=None,
                limit=None,
            )

            prediction_table = paginate_bugs(predictions_table, offset, limit)

            areas_of_testing_percentage = calculate_aot_percentage(
                predictions_table["Area of Testing"]
            )
            priority_percentage = calculate_priority_percentage(
                predictions_table["Priority"], training_parameters["Priority"]
            )
            ttr_percentage = calculate_ttr_percentage(
                predictions_table["Time to Resolve"],
                training_parameters["Time to Resolve"],
            )

            resolution_percentage = calculate_resolution_percentage(
                predictions_table, training_parameters["Resolution"]
            )

            predictions = {
                "predictions_table": list(
                    prediction_table.T.to_dict().values()
                ),
                "prediction_table_rows_count": len(predictions_table),
                "areas_of_testing_chart": areas_of_testing_percentage,
                "priority_chart": priority_percentage,
                "ttr_chart": ttr_percentage,
                "resolution_chart": resolution_percentage,
            }

            redis_conn.set(
                name=f"user:{request.user.id}:qa_metrics:predictions_page",
                value=dumps(predictions),
                ex=60 * 30,
            )
            redis_conn.set(
                name=f"user:{request.user.id}:qa_metrics:filters",
                value=dumps(filters),
                ex=60 * 30,
            )
            redis_conn.set(
                name=f"user:{request.user.id}:qa_metrics:predictions_table",
                value=dumps(list(predictions_table.T.to_dict().values())),
                ex=60 * 30,
            )

        return Response(predictions)


class PredictionsTableView(APIView):
    @swagger_auto_schema(
        operation_description="Predictions Table card content.",
        request_body=QAMetricsTableRequestSerializer,
        responses={200: PredictionsTableSerializer},
    )
    def post(self, request):
        user = request.user
        offset = int(request.data.get("offset", DEFAULT_OFFSET))
        limit = int(request.data.get("limit", DEFAULT_LIMIT))

        cache = redis_conn.get(f"user:{user.id}:qa_metrics:filters")
        filters = loads(cache) if cache else [UNRESOLVED_BUGS_FILTER]

        check_training_files(user)

        cached_predictions = redis_conn.get(
            f"user:{request.user.id}:qa_metrics:predictions_table"
        )

        if cached_predictions:
            predictions = DataFrame.from_records(loads(cached_predictions))
            predictions = list(
                paginate_bugs(df=predictions, offset=offset, limit=limit)
                .T.to_dict()
                .values()
            )
        else:
            predictions_table_fields = get_predictions_table_fields(user)

            issues = calculate_issues_predictions(
                user, predictions_table_fields, filters
            )

            if issues.empty:
                return Response({})

            predictions_table_fields.remove("Description_tr")
            predictions_table_fields.remove("Key")

            predictions = get_predictions_table(
                issues=issues,
                fields_settings=predictions_table_fields,
                offset=None,
                limit=None,
            ).to_dict("records")

            redis_conn.set(
                name=f"user:{request.user.id}:qa_metrics:predictions_table",
                value=dumps(predictions),
                ex=60 * 30,
            )

        return Response(predictions)
