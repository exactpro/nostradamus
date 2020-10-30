from json import dumps, loads

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analysis_and_training.main.significant_terms import (
    calculate_significance_weights,
    get_significant_terms,
)
from apps.analysis_and_training.main.frequently_used_terms import (
    calculate_frequently_terms,
)
from apps.analysis_and_training.main.charts import (
    get_defect_submission,
    get_max_amount,
)
from apps.analysis_and_training.main.statistics import calculate_statistics
from apps.analysis_and_training.serializers import (
    FilterActionSerializer,
    FilterContentSerializer,
    FilterResultSerializer,
    AnalysisAndTrainingSerializer,
    SignificantTermsRequestSerializer,
    SignificantTermsResponseSerializer,
    SignificantTermsRenderSerializer,
    DefectSubmissionSerializer,
    DefectSubmissionResponseSerializer,
    FrequentlyTermsResponseSerializer,
    StatisticsResponseSerializer,
    StatusResponseSerializer,
)
from apps.analysis_and_training.main.training import train
from apps.analysis_and_training.main.mark_up import (
    mark_up_series,
    mark_up_other_data,
)
from apps.analysis_and_training.main.filter import (
    get_filters,
    get_issues_fields,
)
from apps.extractor.main.connector import get_issue_count, get_issues
from apps.settings.main.common import (
    get_source_field,
    get_bug_resolutions,
    get_mark_up_entities,
)

from apps.extractor.main.preprocessor import get_issues_dataframe
from utils.redis import redis_conn, remove_cache_record, clear_cache
from utils.exceptions import InvalidSourceField
from drf_yasg.utils import swagger_auto_schema

from utils.warnings import BugsNotFoundWarning

SWAGGER_DESCRIPTIONS = {
    "Filter_post": "If filtration_type=string, current_value='string'. If filtration_type=numeric, current_value=[integer array]. \n\
    If filtration_type= 'numeric' or 'date' and one of the values is not entered, null is expected to replace this value. For example: [int/date, null]"
}


class AnalysisAndTrainingView(APIView):
    @swagger_auto_schema(
        operation_description="Analysis & Training",
        responses={200: AnalysisAndTrainingSerializer},
    )
    def get(self, request):

        total_count = get_issue_count()
        if not total_count:
            return Response({})

        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )

        filters = None
        if cache:
            filters = loads(cache)

        filtered_count = get_issue_count(filters)

        context = {
            "records_count": {
                "total": total_count,
                "filtered": filtered_count,
            },
        }

        return Response(context)


class FilterView(APIView):
    @swagger_auto_schema(
        operation_description="Filter card content",
        responses={200: FilterContentSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        if cache:
            filters = loads(cache)
        else:
            fields = get_issues_fields(request.user)
            filters = get_filters(
                request.user, issues=get_issues_dataframe(fields=fields)
            )

            redis_conn.set(
                name=f"user:{request.user.id}:analysis_and_training:filters",
                value=dumps(filters),
                ex=60 * 30,
            )

        return Response(filters)

    @swagger_auto_schema(
        operation_description=f"Apply or Clear filters.\n{SWAGGER_DESCRIPTIONS['Filter_post']}",
        request_body=FilterActionSerializer,
        responses={200: FilterResultSerializer},
    )
    def post(self, request):
        fields = get_issues_fields(request.user)
        issues = get_issues_dataframe(fields=fields)

        filters = get_filters(
            request.user,
            issues=issues,
        )

        if request.data.get("action") == "apply":
            new_filters = request.data.get("filters")
            if new_filters:
                for new_filter in new_filters:
                    for filter_ in filters:
                        if new_filter["name"] == filter_["name"]:
                            filter_.update(
                                {
                                    "current_value": new_filter[
                                        "current_value"
                                    ],
                                    "filtration_type": new_filter[
                                        "filtration_type"
                                    ],
                                    "exact_match": new_filter["exact_match"],
                                }
                            )
                issues = get_issues(filters=filters, fields=fields)

        issues_count = len(issues)
        context = {
            "records_count": {
                "total": get_issue_count(),
                "filtered": issues_count,
            },
            "filters": filters,
        }
        for element in context:
            redis_conn.set(
                f"user:{request.user.id}:analysis_and_training:{element}",
                dumps(context.get(element)),
            )

        remove_cache_record(
            "analysis_and_training:defect_submission", request.user.id
        )

        return Response(context)


class DefectSubmissionView(APIView):
    @swagger_auto_schema(
        operation_description="Defect Submission rendering",
        responses={200: DefectSubmissionResponseSerializer},
    )
    def get(self, request):
        cached_filters = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        context = None
        filters = loads(cached_filters) if cached_filters else None
        if not context:
            default_period = "Month"
            issues = get_issues_dataframe(
                fields=["Key", "Created", "Resolved"], filters=filters
            )

            if issues.empty:
                return Response({})

            coordinates = get_defect_submission(
                issues=issues, period=default_period
            )
            context = {
                **coordinates,
                **get_max_amount(coordinates),
                "period": default_period,
            }

            redis_conn.set(
                f"user:{request.user.id}:analysis_and_training:defect_submission",
                dumps(context),
            )

        return Response(context)

    @swagger_auto_schema(
        operation_description="Defect Submission calculation",
        query_serializer=DefectSubmissionSerializer,
        responses={200: DefectSubmissionResponseSerializer},
    )
    def post(self, request):
        period = request.GET["period"]
        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        filters = loads(cache) if cache else None
        issues = get_issues_dataframe(
            fields=["Key", "Created", "Resolved"], filters=filters
        )

        if issues.empty:
            return Response({})

        coordinates = get_defect_submission(issues, period)
        context = {
            **coordinates,
            **get_max_amount(coordinates),
            "period": period,
        }

        redis_conn.set(
            f"user:{request.user.id}:analysis_and_training:defect_submission",
            dumps(context),
        )

        return Response(context)


class SignificantTermsView(APIView):
    @swagger_auto_schema(
        operation_description="Significant Terms rendering",
        responses={200: SignificantTermsRenderSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        filters = loads(cache) if cache else None
        user = request.user

        issues = get_issues_dataframe(
            fields=[
                get_source_field(user),
                "Priority",
                "Resolution",
                "Description_tr",
                "Assignee",
                "Reporter",
            ],
            filters=filters,
        )

        if issues.empty:
            return Response({})

        settings = {
            "source_field": get_source_field(user),
            "bug_resolution": get_bug_resolutions(user),
            "mark_up_entities": get_mark_up_entities(user),
        }

        significant_terms = get_significant_terms(issues, settings)
        context = {"significant_terms": significant_terms}

        return Response(context)

    @swagger_auto_schema(
        operation_description="Significant terms calculation",
        query_serializer=SignificantTermsRequestSerializer,
        responses={200: SignificantTermsResponseSerializer},
    )
    def post(self, request):
        metric = request.GET["metric"]
        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        filters = loads(cache) if cache else None
        source_field = get_source_field(request.user)

        issues = get_issues_dataframe(
            fields=[
                metric.split()[0],
                source_field,
                "Description_tr",
                "Assignee",
                "Reporter",
            ],
            filters=filters,
        )

        if issues.empty:
            return Response({})

        mark_up_entities = get_mark_up_entities(request.user)
        if metric.split()[0] not in ("Resolution", "Priority"):
            if source_field and mark_up_entities:
                for area in mark_up_entities:
                    if area["area_of_testing"] == metric.split()[0]:
                        issues = mark_up_series(
                            issues,
                            source_field,
                            metric.split()[0],
                            area["entities"],
                        )

        significant_terms = calculate_significance_weights(issues, metric)
        context = {"significant_terms": significant_terms}

        return Response(context)


class TrainView(APIView):
    @swagger_auto_schema(
        operation_description="Training",
        responses={200: "{'result': 'success'}"},
    )
    def post(self, request):

        user = request.user

        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        filters = loads(cache) if cache else None
        fields = get_issues_fields(request.user)
        issues = get_issues_dataframe(filters=filters, fields=fields)

        if issues.empty:
            raise BugsNotFoundWarning

        source_field = get_source_field(user)
        if source_field not in issues.columns:
            raise InvalidSourceField

        resolutions = (
            [resolution["value"] for resolution in get_bug_resolutions(user)]
            if len(get_bug_resolutions(user)) != 0
            else []
        )

        areas_of_testing = []

        mark_up_entities = get_mark_up_entities(user)
        if source_field:
            areas_of_testing = [
                area["area_of_testing"] for area in mark_up_entities
            ] + ["Other"]
            for area in mark_up_entities:
                issues = mark_up_series(
                    issues,
                    get_source_field(user),
                    area["area_of_testing"],
                    area["entities"],
                )
            issues = mark_up_other_data(issues, areas_of_testing)

        train(
            user,
            issues,
            areas_of_testing,
            resolutions,
        )

        clear_cache(
            ["qa_metrics:predictions_page", "qa_metrics:predictions_table"],
            request.user.id,
        )

        context = {
            "result": "success",
        }
        return Response(context, status=200)


class FrequentlyTermsView(APIView):
    @swagger_auto_schema(
        operation_description="Frequently Terms",
        responses={200: FrequentlyTermsResponseSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        filters = loads(cache) if cache else None

        fields = get_issues_fields(request.user.id)
        issues = get_issues_dataframe(fields=fields, filters=filters)

        if issues.empty:
            return Response({})

        freq_terms = calculate_frequently_terms(issues)

        context = {"frequently_terms": freq_terms}

        return Response(context)


class StatisticsView(APIView):
    @swagger_auto_schema(
        operation_description="Statistics",
        responses={200: StatisticsResponseSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"user:{request.user.id}:analysis_and_training:filters"
        )
        filters = loads(cache) if cache else None

        fields = get_issues_fields(request.user.id)
        issues = get_issues_dataframe(fields=fields, filters=filters)

        if issues.empty:
            return Response({})

        statistics = calculate_statistics(
            issues,
            ["Comments", "Attachments", "Time to Resolve"],
        )
        context = {"statistics": statistics}

        return Response(context)


class StatusView(APIView):
    @swagger_auto_schema(
        operation_description="Status",
        responses={200: StatusResponseSerializer},
    )
    def get(self, request):
        context = {"issues_exists": bool(get_issue_count())}
        return Response(context)
