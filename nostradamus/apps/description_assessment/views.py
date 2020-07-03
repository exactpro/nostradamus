from math import floor

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from json import dumps, loads

from apps.extractor.main.cleaner import clean_text
from apps.settings.main.archiver import read_from_archive, is_file_in_archive
from apps.qa_metrics.main.predictions_table import (
    calculate_resolution_predictions,
    calculate_area_of_testing_predictions,
)
from utils.const import (
    TRAINING_PARAMETERS_FILENAME,
    TOP_TERMS_FILENAME,
    STOP_WORDS,
)
from utils.redis import redis_conn

from utils.predictions import get_probabilities
from apps.settings.main.archiver import get_archive_path
from apps.settings.main.common import get_training_settings
from utils.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer
from utils.warnings import (
    DescriptionCantAnalyzedWarning,
    DescriptionAssessmentUnavailableWarning,
)

from apps.description_assessment.serializers import (
    DescriptionAssessmentResponseSerializer,
    PredictorResponseSerializer,
    HighlightingResponseSerializer,
    PredictorRequestSerializer,
    HighlightingRequestSerializer,
)


class DescriptionAssesment(APIView):
    @swagger_auto_schema(
        operation_description="Go to Description Assessment page",
        responses={200: DescriptionAssessmentResponseSerializer},
    )
    def get(self, request):
        archive_path = get_archive_path(request.user)
        if not is_file_in_archive(archive_path, TRAINING_PARAMETERS_FILENAME):
            raise DescriptionAssessmentUnavailableWarning
        settings = get_training_settings(request.user)

        resolutions = (
            [resolution["value"] for resolution in settings["bug_resolution"]]
            if len(settings["bug_resolution"]) != 0
            else []
        )

        training_parameters = read_from_archive(
            archive_path, TRAINING_PARAMETERS_FILENAME
        )
        context = {
            "priority": training_parameters.get("Priority"),
            "resolution": resolutions,
            "areas_of_testing": training_parameters.get("areas_of_testing"),
        }

        return Response(context)


class Predictor(APIView):
    @swagger_auto_schema(
        operation_description="Predicts probabilities for the following metrics: priority, resolution, area of testing, time to resolve.",
        request_body=PredictorRequestSerializer,
        responses={200: PredictorResponseSerializer},
    )
    def post(self, request):
        def _convert_to_integer(value):
            return int(floor((value * 100) + 0.5))

        description = clean_text(request.data.get("description"))

        if not description.strip():
            raise DescriptionCantAnalyzedWarning

        archive_path = get_archive_path(request.user)
        training_parameters = read_from_archive(
            archive_path, TRAINING_PARAMETERS_FILENAME
        )
        probabilities = {}
        probabilities["resolution"] = calculate_resolution_predictions(
            description, training_parameters["Resolution"], archive_path
        )
        probabilities[
            "areas_of_testing"
        ] = calculate_area_of_testing_predictions(
            description, training_parameters["areas_of_testing"], archive_path
        )

        for metric in ["Time to Resolve", "Priority"]:
            probabilities[metric] = get_probabilities(
                description,
                training_parameters[metric],
                read_from_archive(archive_path, metric + ".sav"),
            )

        for probability in probabilities:
            if probability == "resolution":
                for resolution in probabilities[probability]:
                    resolution_obj = probabilities[probability][resolution]
                    for metric in resolution_obj:
                        resolution_obj[metric] = _convert_to_integer(
                            resolution_obj[metric]
                        )
            else:
                for metric in probabilities[probability]:
                    probabilities[probability][metric] = _convert_to_integer(
                        probabilities[probability][metric]
                    )

        redis_conn.set(f"description:{request.user.id}", dumps(description))
        redis_conn.set(
            f"probabilities:{request.user.id}", dumps(probabilities)
        )

        context = {"probabilities": probabilities}

        return Response(context)


class Highlighting(APIView):
    @swagger_auto_schema(
        operation_description="Calculates terms related to the selected metric.",
        request_body=HighlightingRequestSerializer,
        responses={200: HighlightingResponseSerializer},
    )
    def post(self, request):
        highlighted_terms = []
        user = request.user
        metric = (
            request.data.get("metric")
            if request.data.get("metric") != "Areas of testing"
            else "areas_of_testing"
        )
        value = request.data.get("value")
        probabilities = loads(redis_conn.get(f"probabilities:{user.id}"))

        if probabilities[metric][value] > 0.05:
            archive_path = get_archive_path(user)
            description = loads(redis_conn.get(f"description:{user.id}"))

            index = metric
            if metric != "areas_of_testing":
                index = f"{metric}_{value}"
            top_terms = (
                read_from_archive(archive_path, TOP_TERMS_FILENAME)[index]
                .dropna()
                .tolist()
            )
            tfidf = StemmedTfidfVectorizer(stop_words=STOP_WORDS)
            tfidf.fit_transform([description])
            for term in tfidf.get_feature_names():
                if term in top_terms:
                    highlighted_terms.append(term)

        context = {"terms": highlighted_terms}

        return Response(context)
