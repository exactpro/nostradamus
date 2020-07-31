from sklearn.feature_extraction import text

from utils.data_converter import convert_date

# Jira limits response size to 1000 per request
MAX_JIRA_BLOCK_SIZE = 1000

JQL = "issuetype=BUG"

BASE_JQL = "issuetype=BUG"

bug_attributes = {
    "built-in": {
        "Labels": "string",
        "Summary": "string",
        "Description": "string",
        "Components": "string",
        "Attachments": "int",
        "Comments": "int",
        "Project": "unique",
        "Priority": "unique",
        "Status": "unique",
        "Key": "unique",
        "Resolution": "unique",
    },
    "raw": {"Resolved": "date", "Created": "date", "Updated": "date"},
}

dtype_conversions = {
    "date": convert_date,
    "int": "int32",
    "float": "float32",
    "unique": "category",
    "string": "string",
    "object": "string",
    "float64": "float32",
    "int64": "int32",
}

WEEKDAYS_SW = [
    "monday",
    "mon",
    "tuesday",
    "tue",
    "wednesday",
    "wed",
    "thursday",
    "thu",
    "friday",
    "fri",
    "saturday",
    "sat",
    "sunday",
    "sun",
]

MONTHS_SW = [
    "january",
    "jan",
    "february",
    "feb",
    "march",
    "mar",
    "april",
    "apr",
    "may",
    "june",
    "jun",
    "july",
    "jul",
    "august",
    "aug",
    "september",
    "sep",
    "october",
    "oct",
    "november",
    "nov",
    "december",
    "dec",
]

STOP_WORDS = text.ENGLISH_STOP_WORDS.difference(
    ("see", "system", "call")
).union(WEEKDAYS_SW, MONTHS_SW, ["having", "couldn"])

PERIOD_MAPPING = {
    "Day": "D",
    "Week": "W-MON",
    "Month": "M",
    "3 Months": "3M",
    "6 Months": "6M",
    "Year": "Y",
}

PERIOD_FORMAT_MAPPING = {
    "Day": "%d.%m.%Y",
    "Week": "%d.%m.%Y",
    "Month": "%b %Y",
    "3 Months": "%b %Y",
    "6 Months": "%b %Y",
    "Year": "%Y",
}

SIGNIFICANT_TERMS_METRICS = ["Resolution", "Priority"]

MIN_CLASS_PERCENTAGE = 0.01

DEFAULT_TEAM = "Nostradamus"
DEFAULT_ROLE = "QA"

DEFAULT_ERROR_CODE = 500
DEFAULT_WARNING_CODE = 209

swagger_desriptions = {
    "Filter_post": "If filtration_type=string, current_value='string'. If filtration_type=numeric, current_value=[integer array]. \n\
    If filtration_type= 'numeric' or 'date' and one of the values is not entered, null is expected to replace this value. For example: [int/date, null]"
}

DEFAULT_PREDICTIONS_TABLE_FIELDS = [
    "Issue Key",
    "Priority",
    "Area of Testing",
    "Time to Resolve",
    "Summary",
]

TRAINING_SETTINGS_FILENAME = "training_settings.pkl"
TRAINING_PARAMETERS_FILENAME = "training_parameters.pkl"
TOP_TERMS_FILENAME = "top_terms.pkl"

# Required for areas of testing prediction.
BINARY_CLASSES = [0, 1]

# Resolution predictions will be mapped separately.
PREDICTIONS_TABLE_FIELD_MAPPING = {
    "Issue Key": "Key",
    "Area of Testing": "areas_of_testing_prediction",
    "Time to Resolve": "Time to Resolve_prediction",
}

PREDICTION_FIELDS = [
    "Resolution_prediction",
    "areas_of_testing_prediction",
    "Time to Resolve_prediction",
]

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 20

UNRESOLVED_BUGS_FILTER = {
    "name": "Resolution",
    "filtration_type": "string",
    "current_value": "Unresolved",
    "exact_match": True,
}

MANDATORY_FIELDS = [
    "Description_tr",
    "Time to Resolve",
    "Resolution",
    "Attachments",
    "Comments",
    "Resolved",
    "Resolution",
    "Created",
    "Updated",
    "Assignee",
    "Reporter",
    "Key",
]
