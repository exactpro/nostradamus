from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from json import dumps, loads

from apps.extractor.main.cleaner import clean_text
from apps.settings.main.archiver import read_from_archive
from apps.qa_metrics.main.predictions_table import (
    calculate_resolution_predictions,
    calculate_area_of_testing_predictions,
    load_models,
)
from utils.const import (
    TRAINING_PARAMETERS_FILENAME,
    TOP_TERMS_FILENAME,
    STOP_WORDS,
)
from utils.data_converter import convert_to_integer
from utils.redis import redis_conn

from utils.predictions import get_probabilities
from apps.settings.main.archiver import get_archive_path
from apps.settings.main.common import get_training_settings
from utils.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer
from utils.warnings import CannotAnalyzeDescriptionWarning

from apps.description_assessment.serializers import (
    DescriptionAssessmentResponseSerializer,
    PredictorResponseSerializer,
    HighlightingResponseSerializer,
    PredictorRequestSerializer,
    HighlightingRequestSerializer,
)
from apps.analysis_and_training.main.training import check_training_files


class DescriptionAssessment(APIView):
    @swagger_auto_schema(
        operation_description="Description Assessment page",
        responses={200: DescriptionAssessmentResponseSerializer},
    )
    def get(self, request):
        user = request.user

        check_training_files(user)

        archive_path = get_archive_path(user)
        settings = get_training_settings(user)

        resolutions = (
            [resolution["value"] for resolution in settings["bug_resolution"]]
            if len(settings["bug_resolution"]) != 0
            else []
        )

        training_parameters = read_from_archive(
            archive_path, TRAINING_PARAMETERS_FILENAME
        )

        if "Other" in training_parameters.get("areas_of_testing"):
            training_parameters["areas_of_testing"].remove("Other")

        context = {
            "Priority": training_parameters.get("Priority"),
            "resolution": resolutions,
            "areas_of_testing": training_parameters.get("areas_of_testing"),
        }

        return Response(context)


class Predictor(APIView):
    @swagger_auto_schema(
        operation_description="Make predictions for a bug-description.",
        request_body=PredictorRequestSerializer,
        responses={200: PredictorResponseSerializer},
    )
    def post(self, request):
        description = clean_text(request.data.get("description"))

        if not description.strip():
            raise CannotAnalyzeDescriptionWarning

        archive_path = get_archive_path(request.user)
        training_parameters = read_from_archive(
            archive_path, TRAINING_PARAMETERS_FILENAME
        )

        models = load_models(
            params=training_parameters, models_path=archive_path
        )

        probabilities = dict()
        for parameter in training_parameters:
            if parameter in ["Time to Resolve", "Priority"]:
                probabilities[parameter] = get_probabilities(
                    description,
                    training_parameters[parameter],
                    models[parameter],
                )
            elif parameter == "Resolution":
                probabilities["resolution"] = calculate_resolution_predictions(
                    description,
                    training_parameters[parameter],
                    models[parameter],
                )
            elif parameter == "areas_of_testing":
                probabilities[
                    parameter
                ] = calculate_area_of_testing_predictions(
                    description,
                    training_parameters[parameter],
                    models[parameter],
                )

        for probability in probabilities:
            if probability == "resolution":
                for resolution in probabilities[probability]:
                    resolution_obj = probabilities[probability][resolution]
                    for metric in resolution_obj:
                        resolution_obj[metric] = convert_to_integer(
                            resolution_obj[metric]
                        )
            else:
                for metric in probabilities[probability]:
                    probabilities[probability][metric] = convert_to_integer(
                        probabilities[probability][metric]
                    )

        redis_conn.set(
            f"user:{request.user.id}:description_assessment:description",
            dumps(description),
        )
        redis_conn.set(
            f"user:{request.user.id}:description_assessment:probabilities",
            dumps(probabilities),
        )

        context = {"probabilities": probabilities}

        return Response(context)


class Highlighting(APIView):
    @swagger_auto_schema(
        operation_description="Highlight terms related to selected metric.",
        request_body=HighlightingRequestSerializer,
        responses={200: HighlightingResponseSerializer},
    )
    def post(self, request):
        user = request.user
        metric = request.data.get("metric")
        value = request.data.get("value")
        probabilities = loads(
            redis_conn.get(
                f"user:{user.id}:description_assessment:probabilities"
            )
        )
        highlighted_terms = []

        if metric == "resolution":
            for resolution in probabilities[metric].copy():
                probabilities[metric].update(probabilities[metric][resolution])

        if probabilities[metric][value] > 0.05:

            archive_path = get_archive_path(user)
            description = loads(
                redis_conn.get(
                    f"user:{user.id}:description_assessment:description"
                )
            )

            index = value
            if metric != "areas_of_testing":
                index = f"{metric.capitalize()}_{value}"

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
