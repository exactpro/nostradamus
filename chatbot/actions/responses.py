RESPONSES = {
    "faq": {
        "ask_analysis_and_training": [
            "The A&T page is an interactive dashboard that provides insights into your data by analysing:\nThe defect submission chart;\nThe frequently used and significant terms;\nThe statistics.",
            "You can also apply a filter and analyse the data you're interested in, and even train machine learning models!",
        ],
        "ask_filter": [
            "Filter is a tool that helps you to find the data you're searching for.",
            "By default, it has the most commonly used fields only. You can always add more fields, if needed, or configure the existing ones.",
        ],
        "ask_filter_workflow": [
            "Each field has its own filtration type which affects the way data is being filtered.",
        ],
        "ask_filter_string_type": [
            "This filtration type does substring search. It can be applied if a value you're looking for is too long.",
            "There is also an exact-match flag with two options:\n* ON - full-match search;\n* OFF - substring search.\n",
        ],
        "ask_filter_dropdown_type": [
            "This filtration type can be used for fields containing repetitive values like Priority, Resolution, etc.\nThe required elements can be easily chosen from the list.",
            "There is also an exact-match flag with two options:\n* ON - full-match search, which means that all the chosen elements have to be listed in the record;\n* OFF - at least one chosen element has to be listed on a record.\n",
        ],
        "ask_filter_date_type": [
            "This filtration type can be applied to date fields.\nYou can easily choose a single date or even a specific range of dates."
        ],
        "ask_filter_numeric_type": [
            "This filtration type can be applied to the fields that use numeric values such as counting, etc. It's also possible to use a number range here."
        ],
        "ask_bug_count": [
            "The bug count represents two numbers:",
            '"Bugs uploaded" represents the total number of bugs uploaded to Nostradamus at the moment. ',
            '"Bugs filtered" represents the bugs relevant to applied filters.',
        ],
        "ask_frequently_terms": [
            "Frequently used terms display the words most frequently used across all uploaded bug descriptions.",
        ],
        "ask_frequently_terms_workflow": [
            "First of all, I clean bug descriptions from code, logs, etc. This gets rid of all uninformative data.",
            "Next, I identify the stop words which haven't been removed at the first step. They will be ignored in calculations. Here we use the standard sklearn's stopwords set and also extend it with weekdays, months and, of course, the assignees’ and the submitters' names from bugs.",
            "When descriptions are ready to be analysed, I use the TF-IDF algorithm to calculate the most frequently used terms.",
        ],
        "ask_significant_terms": [
            "Significant terms represent the words most often used in bug descriptions for bugs related to specific Priority, Resolution or Area of Testing."
        ],
        "ask_significant_terms_workflow": [
            "First of all, I clean bug descriptions from code, logs, etc., to filter out all uninformative data.",
            "Next, I identify the stop words which haven't been removed at the first step. They will be ignored in calculations.\nHere we use standard sklearn's stop-words set and also extend it with weekdays, months and of course assignees and reporters names from bugs.",
            "When descriptions are ready to be analysed, I use the TF-IDF algorithm to identify the most frequently used words.",
            "As a final step, I calculate significance weights for all identified words in the previous step thus you can easily find dependencies between different Priorities, Resolutions or Areas of Testing.",
        ],
        "ask_defect_submission": [
            "The Defect Submission chart represents the dynamics of bug submission into the BTS.\nYou can always switch between the periods that are relevant for you."
        ],
        "ask_statistics": [
            "The statistics card represents the statistical information about the specific metrics which can be calculated."
        ],
        "ask_training": [
            "Training gives me magical abilities!🧙‍♂️",
            "With training, I can learn on the bugs you uploaded to predict:\n* How long it takes to fix a bug\n* What final decision will be made for a bug\n* What area of testing a bug belongs to\n* And even what priority level a bug will have when submitted!\n",
            "The more bugs you give the more accurate my predictions are! 💪🏽",
            'Training is also the process of creating so-called "models":\n* Priority;\n* Time to Resolve;\n* A model for each area of testing;\n* A model for each resolution.\n',
        ],
        "ask_training_purpose": [
            "Training enables me to produce predictions.\nThey are my superpower 😎",
            "If I have trained and learned enough, I can assess the quality of new bugs being submitted as well as make predictions for the ones that already exist.",
        ],
        "ask_training_workflow": [
            "First of all, it's all about data.\nI only use closed bugs. They have really useful data, don’t they? 🤓\nSo I just filter out the unresolved bugs 🧹",
            "Next, I have to clean descriptions from some uninformative data like code, logs, etc.",
            "Then, I identify the stop words which haven't been removed at the second step. They will be ignored in calculations. Here I use the standard sklearn's stopwords set and extend it with weekdays, months and, of course, the assignees’ and the submitters’ names from bugs.",
            "When descriptions are ready to be analysed, I use the TF-IDF algorithm to convert words into a document-term matrix.",
            "After that, I generate synthetic data for each class to avoid data imbalance. This process is performed for each model.",
            "When the data is prepared, I use sklearn's SelectPercentile and Chi-squared methods to select the most significant words and use them to train the Support vector machine (SVM).",
            "Voila!💫 We're ready to conquer the world!",
        ],
        "ask_training_diy": [
            "To perform training, I need to have some data.\nYou are probably wondering where you could get it. Just wait a little, I'll do it for you 🤓",
            "If you don't want to use specific bugs as training data, you can easily filter them out before training. I won't include them in the training process. But please keep in mind that I can't train models on at least 100 bugs 🙃",
            "What about model configuration? Models for priority and time to resolve don't require any additional configuration, but I need to know what areas of testing you have and what bug resolutions you're interested in ☝🏽\nSo, please, don't forget to configure them in Settings.",
            'If the areas of testing and the bug resolutions are configured, you can start the training process by hitting the "Train Model" button.',
            "Please note that the training process takes some time. Be ready to wait a little because I put a lot of effort into learning 🤓",
        ],
        "ask_description_assessment": [
            "On the Description Assessment page, you assess your description's quality based on the following metrics:\nPriority,\nTime to resolve,\nResolutions\nAreas of testing."
        ],
        "ask_qa_metrics": [
            "On the QA Metrics page, you can analyse the predictions for:\nPriority,\nTime to resolve,\nResolutions\nAreas of testing."
        ],
        # TRAINING CONFIGURING
        "ask_training_configuring": [
            "To successfully train models, you have to configure the following elements on the Settings page:",
            "Source field",
            "Area of testing",
            "Bug resolution",
        ],
        "ask_source_field": [
            "Source field is a free input field specifying what bug attribute system will use as a source for performing the markup."
        ],
        "ask_source_field_configuring": [
            "To configure the Source field, you need to:",
            "Open the Analysis & Training tab in Settings",
            "Find the Source field in the Training section",
            "Finally, click on the input field and choose a value from the opened drop-down field.",
        ],
        "ask_area_of_testing": [
            "Area of testing is a section presented as a list of fields used for setting up the markup entities.\n",
            "Each list element is presented as a pair of the following fields:",
            "Name" "Entities\n",
            "Name is a custom name of the entities set.",
            "Entities is multiple choice drop-down field where elements are presented as tags. Elements are grouped by Names and used for the markup process.",
        ],
        "ask_area_of_testing_configuring": [
            "To configure the Area of testing, you need to:",
            "Open the Analysis & Training tab in Settings",
            "Find the Area of testing section under the Source field",
            "Fill the Name field as you wish",
            "Select one or more elements from the Entities field",
            "Press '+' to add this Area to settings",
        ],
        "ask_bug_resolution": [
            "This section allows the user to set up the bug resolution metrics by which the predictions of the resolution probability will be classified."
        ],
        "ask_bug_resolution_configure": [
            "To configure the Bug resolution you need to:",
            "Open the Analysis & Training tab in Settings",
            "Click on the Values field and select one value from the opened list.",
        ],
    },
}

WORKFLOW = {
    "action_faq_selector": [
        "ask_area_of_testing_configuring",
        "ask_bug_resolution_configure",
        "ask_significant_terms_workflow",
        "ask_frequently_terms_workflow",
        "ask_source_field_configuring",
        "ask_description_assessment",
        "ask_analysis_and_training",
        "ask_filter_dropdown_type",
        "ask_training_configuring",
        "ask_filter_numeric_type",
        "ask_filter_string_type",
        "ask_significant_terms",
        "ask_training_workflow",
        "ask_defect_submission",
        "ask_frequently_terms",
        "ask_filter_date_type",
        "ask_training_purpose",
        "ask_area_of_testing",
        "ask_filter_workflow",
        "ask_bug_resolution",
        "ask_training_diy",
        "ask_source_field",
        "ask_qa_metrics",
        "ask_statistics",
        "ask_bug_count",
        "ask_training",
        "ask_filter",
    ],
    "utter_filter_menu": ["ask_filter", "ask_bug_count"],
    "utter_filtration_types": ["ask_filter_workflow"],
    "utter_ask_more_details_analysis_and_training": [
        "ask_significant_terms_workflow",
        "ask_frequently_terms_workflow",
        "ask_analysis_and_training",
        "ask_filter_dropdown_type",
        "ask_filter_numeric_type",
        "ask_filter_string_type",
        "ask_defect_submission",
        "ask_training_workflow",
        "ask_filter_date_type",
        "ask_statistics",
    ],
    "utter_training_options": ["ask_training"],
    "utter_training_purpose_options": ["ask_training_purpose"],
    "utter_training_diy_options": ["ask_training_diy"],
    "utter_significant_terms_options": ["ask_significant_terms"],
    "utter_frequently_terms_options": ["ask_frequently_terms"],
    "utter_ask_more_details_settings": [
        "ask_bug_resolution_configure",
        "ask_area_of_testing_configuring",
        "ask_source_field_configuring",
        "ask_training_configuring",
    ],
    "utter_source_field_options": ["ask_source_field"],
    "utter_bug_resolution_options": ["ask_bug_resolution"],
    "utter_area_of_testing_options": ["ask_area_of_testing"],
}
