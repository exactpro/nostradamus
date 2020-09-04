from typing import Dict, Text, Any, List, Union, Optional
from json import loads, JSONDecodeError

from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.forms import FormAction, REQUESTED_SLOT, Form
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset

from .responses import RESPONSES, WORKFLOW

from rasa_sdk import Tracker, Action

from .api.report_generator import (
    generate_report,
    request_values,
    generate_report_payload,
    check_issues,
)


def get_action_with_help_intent(latest_intent: str) -> list:
    """ Get action name for intent name.

    Parameters
    ----------
    latest_intent:
        Bot intent.

    Returns
    ----------
        Actions name list.
    """
    actions = []
    for action, intents in WORKFLOW.items():
        for intent in intents:
            if intent == latest_intent:
                actions.append(action)
    return actions


class ReportForm(FormAction):
    """Collects data for report."""

    def name(self) -> Text:
        return "report_form"

    def validate_period(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate period value."""
        try:
            if isinstance(loads(value), list):
                return {"period": value}
            else:
                dispatcher.utter_message("Incorrect date. Please try again")
                return {"period": None}
        except (JSONDecodeError, TypeError):
            dispatcher.utter_message("Incorrect date. Please try again")
            return {"period": None}

    @staticmethod
    def required_slots(tracker):
        required_slots = ["project", "period"]

        if tracker.get_slot("project") == "Pick a project":
            required_slots.insert(1, "project_selection")

        return required_slots

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "project": self.from_entity(entity="project"),
            "project_selection": self.from_text(),
            "period": self.from_text(),
        }

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        for slot in self.required_slots(tracker):

            if self._should_request_slot(tracker, slot):

                if not check_issues():
                    dispatcher.utter_message(
                        text="Oops! Bugs haven't been uploaded yet. Please try again later"
                    )

                    return [Form(None), AllSlotsReset()]

                if slot == "project_selection":
                    response = request_values("Project")
                    response["operation"] = "filtration"

                    dispatcher.utter_message(
                        json_message=response, timeout=100,
                    )
                elif slot == "period":
                    response = {
                        "operation": "calendar",
                        "title": "Please choose a date",
                    }
                    dispatcher.utter_message(json_message=response)
                else:
                    dispatcher.utter_message(
                        template=f"utter_ask_{slot}", **tracker.slots
                    )
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        payload = generate_report_payload(tracker)
        message = generate_report(payload)

        if not message.get("filename"):
            message = "Oops! There is no data you’re looking for 😔"
            dispatcher.utter_message(text=message, timeout=100)
        else:
            message["operation"] = "report"
            message["filters"] = payload
            dispatcher.utter_message(json_message=message, timeout=100)

        return [AllSlotsReset()]


class ActionFAQSelector(Action):
    """Basic FAQ response selector."""

    def name(self) -> Text:
        return "action_faq_selector"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        intent = tracker.latest_message["intent"].get("name")
        messages = RESPONSES.get("faq").get(intent)
        for message in messages:
            dispatcher.utter_message(text=message)

        return []


class ActionCustomFallback(Action):
    """Action custom fallback."""

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        latest_intent = tracker.latest_message["intent"].get("name")
        actions = get_action_with_help_intent(latest_intent)
        if actions:
            for action in actions:
                if action != tracker.latest_action_name:
                    if action == "action_faq_selector":
                        ActionFAQSelector().run(
                            dispatcher=dispatcher,
                            tracker=tracker,
                            domain=domain,
                        )
                    else:
                        dispatcher.utter_message(template=action)
        elif (
            latest_intent == "affirm"
            and tracker.events[-4].get("text") == "Do you want to learn more?"
        ):
            dispatcher.utter_message(
                template="utter_more_details_analysis_and_training"
            )
        else:
            dispatcher.utter_message(template="utter_cannot_help")

        return [Form(None), AllSlotsReset()]
