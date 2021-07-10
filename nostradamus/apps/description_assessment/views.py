from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from json import dumps, loads

from apps.extractor.main.cleaner import clean_text

from apps.qa_metrics.main.predictions_table import (
    calculate_resolution_predictions,
    calculate_area_of_testing_predictions,
    load_models,
)
from apps.settings.main.common import get_bug_resolutions
from apps.settings.main.training import (
    get_training_parameters,
    get_top_terms,
    check_training_models,
)
from utils.const import STOP_WORDS
from utils.data_converter import convert_to_integer
from utils.redis import redis_conn

from utils.predictions import get_probabilities
from utils.stemmed_tfidf_vectorizer import StemmedTfidfVectorizer
from utils.warnings import CannotAnalyzeDescriptionWarning

from apps.description_assessment.serializers import (
    DescriptionAssessmentResponseSerializer,
    HighlightingResponseSerializer,
    PredictorRequestSerializer,
    HighlightingRequestSerializer,
    PredictorResponseSerializer,
)


class DescriptionAssessment(APIView):
    @swagger_auto_schema(
        operation_description="Description Assessment page",
        responses={200: DescriptionAssessmentResponseSerializer},
    )
    def get(self, request):
        user = request.user

        check_training_models(user)

        resolutions = (
            [resolution["value"] for resolution in get_bug_resolutions(user)]
            if len(get_bug_resolutions(user)) != 0
            else []
        )

        training_parameters = get_training_parameters(request.user)

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

        training_parameters = get_training_parameters(request.user)

        models = load_models(request.user)

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

        return Response(probabilities)


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

            description = loads(
                redis_conn.get(
                    f"user:{user.id}:description_assessment:description"
                )
            )

            index = value
            if metric != "areas_of_testing":
                index = f"{metric.capitalize()}_{value}"

            top_terms = get_top_terms(request.user)[index].dropna().tolist()

            tfidf = StemmedTfidfVectorizer(stop_words=STOP_WORDS)
            tfidf.fit_transform([description])
            for term in tfidf.get_feature_names():
                if term in top_terms:
                    highlighted_terms.append(term)

        return Response(highlighted_terms)
