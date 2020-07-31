from rest_framework.exceptions import APIException, _get_error_details

from utils.const import DEFAULT_ERROR_CODE


class BaseAPIException(APIException):
    status_code = DEFAULT_ERROR_CODE

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)


class NonexistentJiraUser(BaseAPIException):
    default_detail = "User doesn't exist"
    default_code = "nonexistent_jira_user"


class IncorrectJiraCredentials(BaseAPIException):

    # JIRA blocks user account even with one failed login attempt.
    default_detail = "Incorrect JIRA credentials"
    default_code = "incorrect_jira_credentials"
    message = "Please sign in to BTS to unlock your account"


class IncorrectUserCredentials(BaseAPIException):
    default_detail = "Incorrect username or password"
    default_code = "incorrect_user_credentials"


class SmallNumberRepresentatives(BaseAPIException):
    default_detail = "Oops! Too small number of class representatives."
    default_code = "small_number_representatives"

    def __init__(self, *args):
        super(BaseAPIException, self).__init__(*args)


class LittleDataToAnalyze(BaseAPIException):
    default_detail = (
        "Oops! Too little data to analyze. Model can't be trained."
    )
    default_code = "little_data_to_analyze"


class ResolutionElementsMissed(BaseAPIException):
    default_detail = (
        "Oops! Resolution elements are missed. Model can't be trained."
    )
    default_code = "resolution_elements_missed"

    def __init__(self, *args):
        super(BaseAPIException, self).__init__(*args)


class IncorrectPredictionsTableOrder(BaseAPIException):
    default_detail = "Incorrect predictions table positions order"
    default_code = "incorrect_predictions_table_order"


class NotFilledDefaultFields(BaseAPIException):
    default_detail = "Not all mandatory default fields are specified"
    default_code = "incorrect_default_fields"


class InvalidSourceField(BaseAPIException):
    default_detail = "Source field isn't presented in your data"
    default_code = "invalid_source_field"


class InconsistentGivenData(BaseAPIException):
    default_detail = "Cannot train models. Given data is inconsistent."
    default_code = "inconsistent_data"
