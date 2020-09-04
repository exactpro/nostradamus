from utils.data_converter import get_utc_datetime

FUNCTION_MAPPING = {
    "Attachments": lambda objects: len(objects or []),
    "Comments": lambda objects: len(objects or []),
    "Resolved": lambda obj: get_utc_datetime(obj),
    "Updated": lambda obj: get_utc_datetime(obj),
    "Created": lambda obj: get_utc_datetime(obj),
    "Labels": lambda objects: ",".join(objects or []),
    "Components": lambda objects: ",".join(objects or []),
    "Version": lambda objects: ",".join(objects or []),
}

REPLACE_MAPPING = {
    "Priority": "Unfilled",
    "Resolution": "Unresolved",
    "Updated": None,
    "Resolved": None,
    "Attachments": 0,
    "Comments": 0,
    "Labels": "",
    "Components": "",
}
