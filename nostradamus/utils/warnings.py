from rest_framework.exceptions import APIException

from utils.const import DEFAULT_WARNING_CODE


class BaseAPIWarning(APIException):
    status_code = DEFAULT_WARNING_CODE


class DescriptionCantAnalyzedWarning(BaseAPIWarning, Warning):
    default_detail = (
        "Oops! Description can't be analyzed. Please check the text."
    )
    default_code = "description_cant_be_analyzed"


class BugsNotFoundWarning(BaseAPIWarning, Warning):
    default_detail = "Oops! Bugs haven't been uploaded yet."
    default_code = "bugs_not_found"


class DescriptionAssessmentUnavailableWarning(BaseAPIWarning, Warning):
    default_detail = (
        "Description assessment is unavailable. Please, train models."
    )
    default_code = "description_assessment_unavailable"


class PredictionsNotReadyWarning(BaseAPIWarning, Warning):
    default_detail = "Making predictions... Please, try again later."
    default_code = "prediction_appending"


class ModelsNotTrainedWarning(BaseAPIWarning, Warning):
    default_detail = "Models are not trained. Please, train models."
    default_code = "not_trained_models"
