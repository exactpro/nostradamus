from rest_framework.exceptions import APIException


class NonexistentJiraUser(APIException):
    default_detail = "User doesn't exist"
    default_code = "nonexistent_jira_user"


class IncorrectJiraCredentials(APIException):

    # JIRA blocks user account even with one failed login attempt.
    default_detail = "Incorrect JIRA credentials"
    default_code = "incorrect_jira_credentials"
    message = "Please sign in to BTS to unlock your account"


class IncorrectUserCredentials(APIException):
    default_detail = "Incorrect username or password"
    default_code = "incorrect_user_credentials"


class SmallNumberRepresentatives(APIException):
    default_detail = "Oops! Too small number of class representatives."
    default_code = "small_number_representatives"


class LittleDataToAnalyze(APIException):
    default_detail = (
        "Oops! Too little data to analyze. Model can't be trained."
    )
    default_code = "little_data_to_analyze"


class ResolutionElementsMissed(APIException):
    default_detail = (
        "Oops! Resolution elements are missed. Model can't be trained."
    )
    default_code = "resolution_elements_missed"


class IncorrectPredictionsTableOrder(APIException):
    default_detail = "Incorrect predictions table positions order"
    default_code = "incorrect_predictions_table_order"


class NotFilledDefaultFields(APIException):
    default_detail = "Not all mandatory default fields are specified"
    default_code = "incorrect_default_fields"


class InvalidSourceField(APIException):
    default_detail = "Source field isn't presented in your data"
    default_code = "invalid_source_field"


class InconsistentGivenData(APIException):
    default_detail = "Cannot train models. Given data is inconsistent."
    default_code = "inconsistent_data"
