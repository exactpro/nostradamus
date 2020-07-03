from json import dumps, loads

from rest_framework.response import Response
from rest_framework.views import APIView
from multiprocessing import Process
import pandas as pd

from apps.analysis_and_training.main.significant_terms import (
    calculate_significance_weights,
    get_significant_terms,
)
from apps.analysis_and_training.main.frequently_used_terms import (
    calculate_frequently_terms,
)
from apps.analysis_and_training.main.charts import calculate_defect_submission
from apps.analysis_and_training.main.statistics import calculate_statistics
from apps.analysis_and_training.serializers import (
    FilterRequestSerializer,
    AnalysisAndTrainingSerializer,
    SignificantTermsRequestSerializer,
    SignificantTermsResponseSerializer,
    DefectSubmissionSerializer,
    DefectSubmissionResponseSerializer,
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
from apps.qa_metrics.main.predictions_table import (
    append_predictions,
    delete_old_predictions,
)
from apps.settings.main.common import get_training_settings
from apps.settings.main.archiver import delete_training_data, get_archive_path
from utils.const import swagger_desriptions
from utils.redis import redis_conn
from utils.exceptions import InvalidMarkUpSource
from drf_yasg.utils import swagger_auto_schema


class AnalysisAndTraining(APIView):
    @swagger_auto_schema(
        operation_description="Analysis and Training",
        responses={200: AnalysisAndTrainingSerializer},
    )
    def get(self, request):

        cache = redis_conn.get(f"analysis_and_training:{request.user.id}")
        if cache:
            return Response(loads(cache))
        fields = get_issues_fields(request.user)
        issues = get_issues(fields=fields)
        if not issues:
            # TODO: FE shows progress bar when data is empty
            return Response({})

        issues = pd.DataFrame.from_records(issues)
        freq_terms = calculate_frequently_terms(issues)
        statistics = calculate_statistics(
            df=issues, series=["Comments", "Attachments", "Time to Resolve"]
        )
        defect_submission = calculate_defect_submission(
            df=issues, period="Month"
        )
        significant_terms = get_significant_terms(issues)
        filters = get_filters(request.user, issues=issues)

        context = {
            "records_count": {"total": len(issues), "filtered": len(issues)},
            "frequently_terms": freq_terms,
            "statistics": statistics,
            "submission_chart": defect_submission,
            "significant_terms": significant_terms,
            "filters": filters,
        }
        redis_conn.set(
            name=f"analysis_and_training:{request.user.id}",
            value=dumps(context),
            ex=60 * 30,
        )

        return Response(context)


class DefectSubmission(APIView):
    @swagger_auto_schema(
        operation_description="Defect Submission Chart",
        query_serializer=DefectSubmissionSerializer,
        responses={200: DefectSubmissionResponseSerializer},
    )
    def get(self, request):
        period = request.GET["period"]
        cache = redis_conn.get(f"analysis_and_training:{request.user.id}")
        filters = loads(cache)["filters"] if cache else None
        bugs = pd.DataFrame(
            get_issues(fields=["Key", "Created"], filters=filters)
        )

        if bugs.empty:
            return Response({})

        coordinates = calculate_defect_submission(bugs, period)

        context = {"submission_chart": coordinates}

        return Response(context)


class Filter(APIView):
    """
    @swagger_auto_schema(
        operation_description="The receipt of the filter fields.",
        responses={200: FilterResponseSerializer},
    )
    def get(self, request):
        filters = get_current_settings(request.user)["filters"]
        filters = update_drop_down_fields(filters, request.user)
        return Response(filters)
    """

    @swagger_auto_schema(
        operation_description="Apply or Clear filters.\n{}".format(
            swagger_desriptions["Filter_post"]
        ),
        request_body=FilterRequestSerializer,
        responses={200: AnalysisAndTrainingSerializer},
    )
    def post(self, request):
        fields = get_issues_fields(request.user)

        filters = get_filters(
            request.user,
            issues=pd.DataFrame.from_records(get_issues(fields=fields)),
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
            else:
                issues = get_issues(fields=fields)
        else:
            issues = get_issues(fields=fields)

        if len(issues) == 0:
            context = {
                "records_count": {"total": get_issue_count(), "filtered": 0},
                "frequently_terms": [],
                "statistics": {},
                "submission_chart": {},
                "significant_terms": {},
                "filters": filters,
            }
            redis_conn.set(
                f"analysis_and_training:{request.user.id}", dumps(context)
            )
            return Response({})

        issues = pd.DataFrame.from_records(issues)
        freq_terms = calculate_frequently_terms(issues)
        statistics = calculate_statistics(
            df=issues, series=["Comments", "Attachments", "Time to Resolve"]
        )
        submission_chart = calculate_defect_submission(
            df=issues, period="Month"
        )
        significant_terms = get_significant_terms(
            issues, get_training_settings(request.user)
        )

        context = {
            "records_count": {
                "total": get_issue_count(),
                "filtered": len(issues),
            },
            "frequently_terms": freq_terms,
            "statistics": statistics,
            "submission_chart": submission_chart,
            "significant_terms": significant_terms,
            "filters": filters,
        }
        redis_conn.set(
            f"analysis_and_training:{request.user.id}", dumps(context)
        )

        return Response(context)


class SignificantTerms(APIView):
    @swagger_auto_schema(
        operation_description="Significant terms generating",
        query_serializer=SignificantTermsRequestSerializer,
        responses={200: SignificantTermsResponseSerializer},
    )
    def get(self, request):
        metric = request.GET["metric"]
        cache = redis_conn.get(f"analysis_and_training:{request.user.id}")
        filters = loads(cache)["filters"] if cache else None
        settings = get_training_settings(request.user)

        issues = get_issues(
            fields=[
                metric.split()[0],
                settings.get("mark_up_source"),
                "Description_tr",
                "Assignee",
                "Reporter",
            ],
            filters=filters,
        )

        df = pd.DataFrame.from_records(issues)

        if metric.split()[0] not in ("Resolution", "Priority"):
            if settings["mark_up_source"] and settings["mark_up_entities"]:
                for area in settings["mark_up_entities"]:
                    if area["area_of_testing"] == metric.split()[0]:
                        df = mark_up_series(
                            df,
                            settings["mark_up_source"],
                            metric.split()[0],
                            area["entities"],
                        )

        significant_terms = calculate_significance_weights(df, metric)
        context = {"significant_terms": significant_terms}

        return Response(context)


class Train(APIView):
    @swagger_auto_schema(
        operation_description="Training",
        responses={200: "{'result': 'success'}"},
    )
    def post(self, request):
        instance = request.user

        cache = redis_conn.get(f"analysis_and_training:{request.user.id}")
        filters = loads(cache)["filters"] if cache else None
        fields = get_issues_fields(request.user)
        df = pd.DataFrame(get_issues(filters=filters, fields=fields))

        # New predictions will be appended after training.
        delete_old_predictions()

        settings = get_training_settings(request.user)

        if settings["mark_up_source"] not in df.columns:
            raise InvalidMarkUpSource

        resolutions = (
            [resolution["value"] for resolution in settings["bug_resolution"]]
            if len(settings["bug_resolution"]) != 0
            else []
        )

        areas_of_testing = []

        if settings["mark_up_source"]:
            areas_of_testing = [
                area["area_of_testing"]
                for area in settings["mark_up_entities"]
            ] + ["Other"]
            for area in settings["mark_up_entities"]:
                df = mark_up_series(
                    df,
                    settings["mark_up_source"],
                    area["area_of_testing"],
                    area["entities"],
                )
            df = mark_up_other_data(df, areas_of_testing)

        delete_training_data(get_archive_path(instance))

        train(
            instance, df, areas_of_testing, resolutions,
        )

        context = {
            "result": "success",
        }

        process = Process(target=append_predictions, args=(request.user,))
        process.start()

        return Response(context, status=200)
