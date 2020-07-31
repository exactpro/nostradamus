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
from apps.analysis_and_training.main.charts import get_defect_submission
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
from apps.settings.main.common import get_training_settings
from apps.settings.main.archiver import delete_training_data, get_archive_path
from utils.const import swagger_desriptions
from apps.extractor.main.preprocessor import get_issues_dataframe
from utils.redis import redis_conn, clear_cache
from utils.exceptions import InvalidSourceField
from drf_yasg.utils import swagger_auto_schema

from utils.warnings import BugsNotFoundWarning


class AnalysisAndTraining(APIView):
    @swagger_auto_schema(
        operation_description="Analysis & Training",
        responses={200: AnalysisAndTrainingSerializer},
    )
    def get(self, request):

        total_count = get_issue_count()
        if not total_count:
            return Response({})

        cache = redis_conn.get(
            f"analysis_and_training:filters:{request.user.id}"
        )

        filters = None
        if cache:
            filters = loads(cache)

        filtered_count = len(get_issues(filters=filters, fields=["Key",]))

        context = {
            "records_count": {
                "total": total_count,
                "filtered": filtered_count,
            },
        }

        return Response(context)


class Filter(APIView):
    @swagger_auto_schema(
        operation_description="Filter card content",
        responses={200: FilterContentSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"analysis_and_training:filters:{request.user.id}"
        )
        if cache:
            filters = loads(cache)
        else:
            fields = get_issues_fields(request.user)
            filters = get_filters(
                request.user, issues=get_issues_dataframe(fields=fields)
            )

            redis_conn.set(
                name=f"analysis_and_training:filters:{request.user.id}",
                value=dumps(filters),
                ex=60 * 30,
            )

        return Response(filters)

    @swagger_auto_schema(
        operation_description=f"Apply or Clear filters.\n{swagger_desriptions['Filter_post']}",
        request_body=FilterActionSerializer,
        responses={200: FilterResultSerializer},
    )
    def post(self, request):
        fields = get_issues_fields(request.user)
        issues = get_issues_dataframe(fields=fields)

        filters = get_filters(request.user, issues=issues,)

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
                f"analysis_and_training:{element}:{request.user.id}",
                dumps(context.get(element)),
            )

        clear_cache("analysis_and_training:defect_submission")

        return Response(context)


class DefectSubmission(APIView):
    @swagger_auto_schema(
        operation_description="Defect Submission rendering",
        responses={200: DefectSubmissionResponseSerializer},
    )
    def get(self, request):
        cached_chart = redis_conn.get(
            f"analysis_and_training:defect_submission:{request.user.id}"
        )
        cached_filters = redis_conn.get(
            f"analysis_and_training:filters:{request.user.id}"
        )
        context = loads(cached_chart) if cached_chart else None
        filters = loads(cached_filters) if cached_filters else None
        if not context:
            default_period = "Month"
            issues = get_issues_dataframe(
                fields=["Key", "Created"], filters=filters
            )

            if issues.empty:
                return Response({})

            coordinates = get_defect_submission(
                df=issues, period=default_period
            )
            context = {
                "defect_submission": coordinates,
                "period": default_period,
            }

            redis_conn.set(
                f"analysis_and_training:defect_submission:{request.user.id}",
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
            f"analysis_and_training:filters:{request.user.id}"
        )
        filters = loads(cache) if cache else None
        issues = get_issues_dataframe(
            fields=["Key", "Created"], filters=filters
        )

        if issues.empty:
            return Response({})

        coordinates = get_defect_submission(issues, period)
        context = {"defect_submission": coordinates, "period": period}

        redis_conn.set(
            f"analysis_and_training:defect_submission:{request.user.id}",
            dumps(context),
        )

        return Response(context)


class SignificantTerms(APIView):
    @swagger_auto_schema(
        operation_description="Significant Terms rendering",
        responses={200: SignificantTermsRenderSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"analysis_and_training:filters:{request.user.id}"
        )
        filters = loads(cache) if cache else None
        settings = get_training_settings(request.user)
        issues = get_issues_dataframe(
            fields=[
                settings["source_field"],
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
            f"analysis_and_training:filters:{request.user.id}"
        )
        filters = loads(cache) if cache else None
        settings = get_training_settings(request.user)

        issues = get_issues_dataframe(
            fields=[
                metric.split()[0],
                settings.get("source_field"),
                "Description_tr",
                "Assignee",
                "Reporter",
            ],
            filters=filters,
        )

        if issues.empty:
            return Response({})

        if metric.split()[0] not in ("Resolution", "Priority"):
            if settings["source_field"] and settings["mark_up_entities"]:
                for area in settings["mark_up_entities"]:
                    if area["area_of_testing"] == metric.split()[0]:
                        issues = mark_up_series(
                            issues,
                            settings["source_field"],
                            metric.split()[0],
                            area["entities"],
                        )

        significant_terms = calculate_significance_weights(issues, metric)
        context = {"significant_terms": significant_terms}

        return Response(context)


class Train(APIView):
    @swagger_auto_schema(
        operation_description="Training",
        responses={200: "{'result': 'success'}"},
    )
    def post(self, request):

        user = request.user

        cache = redis_conn.get(
            f"analysis_and_training:filters:{request.user.id}"
        )
        filters = loads(cache) if cache else None
        fields = get_issues_fields(request.user)
        issues = get_issues_dataframe(filters=filters, fields=fields)

        if issues.empty:
            raise BugsNotFoundWarning

        settings = get_training_settings(request.user)

        if settings["source_field"] not in issues.columns:
            raise InvalidSourceField

        resolutions = (
            [resolution["value"] for resolution in settings["bug_resolution"]]
            if len(settings["bug_resolution"]) != 0
            else []
        )

        areas_of_testing = []

        if settings["source_field"]:
            areas_of_testing = [
                area["area_of_testing"]
                for area in settings["mark_up_entities"]
            ] + ["Other"]
            for area in settings["mark_up_entities"]:
                issues = mark_up_series(
                    issues,
                    settings["source_field"],
                    area["area_of_testing"],
                    area["entities"],
                )
            issues = mark_up_other_data(issues, areas_of_testing)

        delete_training_data(get_archive_path(user))

        train(
            user, issues, areas_of_testing, resolutions,
        )

        clear_cache("qa_metrics:predictions")

        context = {
            "result": "success",
        }
        return Response(context, status=200)


class FrequentlyTerms(APIView):
    @swagger_auto_schema(
        operation_description="Frequently Terms",
        responses={200: FrequentlyTermsResponseSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"analysis_and_training:filters:{request.user.id}"
        )
        filters = loads(cache) if cache else None

        fields = get_issues_fields(request.user.id)
        issues = get_issues_dataframe(fields=fields, filters=filters)

        if issues.empty:
            return Response({})

        freq_terms = calculate_frequently_terms(issues)

        context = {"frequently_terms": freq_terms}

        return Response(context)


class Statistics(APIView):
    @swagger_auto_schema(
        operation_description="Statistics",
        responses={200: StatisticsResponseSerializer},
    )
    def get(self, request):
        cache = redis_conn.get(
            f"analysis_and_training:filters:{request.user.id}"
        )
        filters = loads(cache) if cache else None

        fields = get_issues_fields(request.user.id)
        issues = get_issues_dataframe(fields=fields, filters=filters)

        if issues.empty:
            return Response({})

        statistics = calculate_statistics(
            issues, ["Comments", "Attachments", "Time to Resolve"],
        )
        context = {"statistics": statistics}

        return Response(context)
