## story_greet
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help

## story_goodbye
* goodbye
    - utter_goodbye

## story_thankyou
* thanks
    - utter_noworries

## happy_report_(no_period)
* report
    - report_form
    - form{"name": "report_form"}
    - form{"name": null}

## happy_report_(period)
* form: inform{"period": "today"}
    - form: report_form
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}


## interactive_story_1
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* intro_nostradamus
    - utter_intro_nostradamus
* describe_yourself
    - utter_describe_yourself
    - utter_ask_help
* what_do_you_can
    - utter_what_do_you_can
* thanks
    - utter_noworries
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Today"}
    - form: report_form
    - slot{"period": "Today"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* thanks
    - utter_noworries
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* intro_nostradamus
    - utter_intro_nostradamus
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* what_do_you_can
    - utter_what_do_you_can
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* out_of_scope
    - utter_cannot_help
* out_of_scope
    - utter_cannot_help
* describe_yourself
    - utter_describe_yourself
    - utter_ask_help
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Today"}
    - form: report_form
    - slot{"period": "Today"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* goodbye
    - utter_goodbye

## interactive_story_1
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Yesterday"}
    - form: report_form
    - slot{"period": "Yesterday"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* thanks
    - utter_noworries

## interactive_story_1
* report{"period": "today"}
    - report_form
    - form{"name": "report_form"}
    - slot{"period": "today"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* goodbye
    - utter_goodbye
* what_do_you_can
    - utter_what_do_you_can
* goodbye
    - utter_goodbye
