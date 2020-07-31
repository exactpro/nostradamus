import json
from json import dumps, loads
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
    paginate_bugs,
    calculate_issues_predictions,
    get_predictions_table_fields,
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
    check_filters_equality,
)
from utils.const import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    TRAINING_PARAMETERS_FILENAME,
    UNRESOLVED_BUGS_FILTER,
)
from apps.extractor.main.preprocessor import get_issues_dataframe
from utils.redis import redis_conn

from pandas import DataFrame


class QAMetricsView(APIView):
    @swagger_auto_schema(responses={200: QAMetricsFiltersSerializer},)
    def get(self, request):
        user = request.user

        check_training_files(user)

        cached_filters = redis_conn.get(
            f"qa_metrics:filters:{request.user.id}"
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


class PredictionsInfoView(APIView):
    @swagger_auto_schema(
        request_body=QAMetricsFiltersSerializer,
        responses={200: PredictionsInfoSerializer},
    )
    def post(self, request):
        user = request.user
        offset = DEFAULT_OFFSET
        limit = DEFAULT_LIMIT

        new_filters = request.data.get("filters", [])
        filters = json.loads(json.dumps(get_qa_metrics_settings(user)))
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

        cached_predictions = redis_conn.get(
            f"qa_metrics:predictions_page:{request.user.id}"
        )
        cached_filters = redis_conn.get(
            f"qa_metrics:filters:{request.user.id}"
        )
        cached_filters = loads(cached_filters) if cached_filters else []

        if cached_predictions and check_filters_equality(
            filters, cached_filters
        ):
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
                return Response(
                    {
                        "records_count": {
                            "total": len(
                                get_issues(
                                    fields=["Key"],
                                    filters=[UNRESOLVED_BUGS_FILTER],
                                )
                            ),
                            "filtered": 0,
                        }
                    }
                )

            predictions_table_fields.remove("Description_tr")
            predictions_table_fields.remove("Key")

            predictions_table = get_predictions_table(
                issues=issues,
                fields_settings=predictions_table_fields,
                offset=None,
                limit=None,
            )

            filtered_predictions_count = len(predictions_table)

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
                "records_count": {
                    "total": len(
                        get_issues(
                            fields=["Key"], filters=[UNRESOLVED_BUGS_FILTER]
                        )
                    ),
                    "filtered": filtered_predictions_count,
                },
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
                name=f"qa_metrics:predictions_page:{request.user.id}",
                value=dumps(predictions),
                ex=60 * 30,
            )
            redis_conn.set(
                name=f"qa_metrics:filters:{request.user.id}",
                value=dumps(filters),
                ex=60 * 30,
            )
            redis_conn.set(
                name=f"qa_metrics:predictions_table:{request.user.id}",
                value=dumps(list(predictions_table.T.to_dict().values())),
                ex=60 * 30,
            )

        return Response(predictions)


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

        cached_predictions = redis_conn.get(
            f"qa_metrics:predictions_table:{request.user.id}"
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

        return Response(predictions)
