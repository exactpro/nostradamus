import requests

from json import loads, JSONDecodeError
from parsedatetime import Calendar
from datetime import datetime
from pytz import utc

from rasa_sdk import Tracker

API_URL = "http://nostradamus-core:8000/virtual_assistant"


def convert_date(raw_date: str) -> tuple:
    def _get_datetime_range(date: str) -> tuple:
        """ Makes one day period by received date.

        Parameters
        ----------
        date:
            Date for report generating.

        Returns
        -------
            Datetime range.
        """
        date = datetime.strptime(date, "%Y-%m-%d")
        from_date = date.astimezone(utc)
        from_date = from_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        to_date = (
            date.replace(hour=23, minute=59, second=59)
            .astimezone(utc)
            .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        )

        return from_date, to_date

    parser = Calendar()
    date, status = parser.parse(raw_date)
    date = datetime(*date[:3]).strftime("%Y-%m-%d")
    return _get_datetime_range(date)


def generate_report(payload: dict):
    """ Sends request for report generating.

    Parameters
    ----------
    payload:
        Additional filtration info.

    Returns
    -------
        Report data generator.
    """
    url = f"{API_URL}/generate_report/"

    request = requests.post(url, json=payload)
    return request.json()


def generate_report_payload(tracker: Tracker) -> dict:
    """ Creates a filtration payload from report form slots.

    Parameters
    ----------
    tracker:
        The state of conversation.

    Returns
    -------
        Filtration payload.
    """
    slots = tracker.current_slot_values()
    payload = dict()

    for slot in slots:
        if f"{slot}_selection" in slots:
            try:
                payload[slot] = loads(slots[f"{slot}_selection"])
            except (JSONDecodeError, TypeError):
                payload[slot] = slots[f"{slot}_selection"]
        elif slot == "period":
            payload[slot] = loads(slots[slot])

    return payload


def request_values(field: str) -> dict:
    """ Query unique values by field.

    Parameters
    ----------
    field:
        Issue field.

    Returns
    -------
        Unique values.
    """
    params = {"field": field}
    url = f"{API_URL}/request_values/"

    request = requests.get(url, params=params)
    return request.json()


def check_issues() -> bool:
    url = f"{API_URL}/issues_checker/"

    request = requests.get(url)

    return request.json().get("issues_loaded")
