from typing import Dict, Text, Any, List, Union
from datetime import datetime

from rasa_sdk import Tracker, Action
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset

from parsedatetime import Calendar

import requests


def convert_date(raw_date: str) -> str:
    parser = Calendar()
    date, status = parser.parse(raw_date)
    date = datetime(*date[:3])
    return date.strftime("%Y-%m-%d")


def generate_report(date: str):
    """ Sends request for report generating.

    Parameters
    ----------
    date:
        Date for which report will be generated.

    Returns
    -------
        Report data generator.
    """
    payload = {"date": date}
    url = "http://nostradamus-core:8000/virtual_assistant/generate_report/"

    request = requests.post(url, json=payload)
    yield request.json()


class ReportForm(FormAction):
    """Collects data for report"""

    def name(self) -> Text:
        return "report_form"

    @staticmethod
    def required_slots(tracker):
        return ["period"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"period": self.from_entity(entity="period")}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        period = convert_date(tracker.get_slot("period"))
        message = generate_report(period)
        dispatcher.utter_message(json_message=next(message), timeout=100)
        return [AllSlotsReset()]
