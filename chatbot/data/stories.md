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

## Greet -> Intro -> Describe Yourself -> What do you can -> thanks -> Goodbye
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

## Greet -> Intro -> Goodbye
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* intro_nostradamus
    - utter_intro_nostradamus
* goodbye
    - utter_goodbye

## Greet -> What do you can -> Goodbye
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* what_do_you_can
    - utter_what_do_you_can
* goodbye
    - utter_goodbye

## Greet -> Out of Scope -> Out of Scope -> Describe Yourself
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

## Deny
* deny
    - utter_cannot_help
    
## Affirm
* affirm
    - utter_cannot_help

# ########################## FAQ A&T ########################## #

## FAQ A&T: basic answer
* faq
    - respond_faq

## FAQ A&T: A&T Basic
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training

## FAQ A&T: A&T -> Filter -> Filter WF -> Filter String
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: A&T -> Filter -> Filter WF -> Filter Drop-down
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: A&T -> Filter -> Filter WF -> Filter Date
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_date_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ: A&T -> Filter -> Filter WF -> Filter Numeric
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_numeric_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: Freq terms -> Freq terms WF
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: Signif terms -> Signif terms WF
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: Defect Submission
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: Statistics
* ask_statistics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: A&T -> Filter -> Filter WF
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types

## FAQ A&T: Training Description
* ask_training
    - action_faq_selector
    - utter_training_options

## FAQ A&T: Training Purpose
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options

## FAQ A&T: Training Workflow
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: Training DIY
* ask_training_diy
    - action_faq_selector
    - utter_training_diy_options
* ask_filter_workflow
    - action_faq_selector

## FAQ A&T: DAS basic
* ask_description_assessment
    - action_faq_selector

## FAQ A&T: QAM basic
* ask_qa_metrics
    - action_faq_selector

## FAQ A&T: A&T -> Freq terms -> Freq terms WF -> A&T -> Bug count -> Filter WF -> Filter String
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Filter -> Filter WF -> Filter Date -> Defect Submission -> Freq terms -> 
## Freq terms WF -> Sign terms -> Sign terms WF -> Statistics -> Bug count
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_date_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_statistics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Training -> Training Purpose -> DAS
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_description_assessment
    - action_faq_selector

## FAQ A&T: Training -> Training Workflow
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: Training -> Training DIY -> Filter WF
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_diy
    - action_faq_selector
    - utter_training_diy_options
* ask_filter_workflow
    - action_faq_selector

## FAQ A&T: A&T -> Training -> Training DIY -> Filter WF -> Filter String  
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_diy
    - action_faq_selector
    - utter_training_diy_options
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T -> Training -> Training Purpose 
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_description_assessment
    - action_faq_selector

## FAQ A&T: A&T -> Training ->  Training WF
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## FAQ A&T: Greet -> A&T -> Training -> Training Purpose -> QAM -> Training ->
##      Training WF -> Training -> Training DIY -> Filter WF -> Filter Drop-down ->
##      Bug count -> Filter WF -> Filter Numeric -> Freq terms -> Freq terms WF ->
##      Signif terms -> Signif terms WF -> Statistics 
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_qa_metrics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_diy
    - action_faq_selector
    - utter_training_diy_options
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_numeric_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_statistics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T -> Defect Submission -> Filter -> Filter WF -> 
##      Filter String -> Defect Submission
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_filter
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training

## FAQ A&T: A&T -> Defect Submission -> Training -> Training WF
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training

## FAQ A&T: A&T -> Training -> Training Purpose -> Description Assessment ->
##      Training -> Training Purpose -> Qa Metrics
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_description_assessment
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_qa_metrics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training

## FAQ A&T: A&T -> Frequently Terms -> Frequently Terms WF -> 
##      Training -> Training WF -> Training -> Training DIY ->
##      Filter WF -> Filter String
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_diy
    - action_faq_selector
    - utter_training_diy_options
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training

## FAQ A&T: Filter -> Filter WF -> Filter String -> Defect Submission ->
##      Significant Terms -> Training -> Training Purpose ->
##      Description Assesment -> Bug Count -> Training -> Training Purpose ->
##      Qa metrics -> Significant Terms -> Significant Terms WF
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_description_assessment
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_qa_metrics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T -> Training -> Training WF -> Training -> Training WF ->
##      Defect Submission -> Training -> Training WF -> Bug count ->
##      Filter WF -> Filter String -> Training -> Training Purpose -> 
##      Qa Metrics -> Frequently terms -> Frequently terms WF -> 
##      Significant Terms -> Significant Terms WF
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_qa_metrics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Defect Submission -> Frequently Terms -> Frequently Terms WF ->
##      Significant Terms -> Significant Terms WF -> Statistics ->
##      Training -> Training Purpose -> Description Assessment ->
##      Training -> Training Purpose -> Qa Metrics ->
##      Training -> Training Workflow -> Training ->
##      Training Diy -> Filter WF -> Filter String ->
##      Bug count -> Filter WF -> Filter String
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_statistics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_description_assessment
    - action_faq_selector
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_purpose
    - action_faq_selector
    - utter_training_purpose_options
* ask_qa_metrics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_diy
    - action_faq_selector
    - utter_training_diy_options
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Filter -> Filter WF -> Filter Date -> 
##      Training -> Training WF
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_date_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T -> Frequently Terms -> Frequently Terms WF ->
##      Significant Terms -> Significant Terms WF ->
##      Frequently Terms -> Frequently Terms WF ->
##      Significant Terms -> Significant Terms WF ->
##      Frequently Terms -> Frequently Terms WF ->
##      Significant Terms -> Significant Terms WF 
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Filter -> Filter WF -> Filter Date ->
##      Frequently Terms -> Frequently Terms WF ->
##      Significant Terms -> Significant Terms WF
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_date_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Filter -> Filter WF -> Filter Numerics -> Training ->
##      Training WF -> Bug count -> Filter WF -> Filter Numeric
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_numeric_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_training
    - action_faq_selector
    - utter_training_options
* ask_training_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_numeric_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training

## FAQ A&T: A&T -> Statistics -> Statistics
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_statistics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_statistics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T -> Frequently Terms -> Frequently Terms WF
##      A&T -> Defect Submission
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_defect_submission
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Filter -> Filter WF -> Filter Drop-down ->
##      Filter -> Filter WF -> Filter Drop-down
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else
    
## FAQ A&T: A&T -> Filter -> Filter WF -> Filter String ->
##      Filter -> Filter WF -> Filter Drop-down
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_string_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_filter
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T -> Frequently Terms -> Frequently Terms WF -> Filter ->
##      Filter WF -> Filter Drop-down -> Frequently Terms ->
##      Frequently Terms WF -> Significant terms -> Significant Terms WF
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_filter
    - action_faq_selector
     - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_significant_terms
    - action_faq_selector
    - utter_significant_terms_options
* ask_significant_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: A&T -> Bug count -> Filter WF -> Filter Numeric ->
##      Frequently Terms -> Frequently Terms WF
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_bug_count
    - action_faq_selector
    - action_custom_fallback
    - reset_slots
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_numeric_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training
* ask_frequently_terms
    - action_faq_selector
    - utter_frequently_terms_options
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* affirm
    - utter_more_details_analysis_and_training

## FAQ A&T: Deny more details after A&T
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## FAQ A&T: Deny more details after Filter Drop-Down
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else
    
## FAQ A&T: Deny more details after Frequently Terms WF
* ask_frequently_terms_workflow
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

# ########################## FAQ Settings ########################## #

## FAQ Settings: Training Conf
* ask_training_configuring
    - action_faq_selector
    - utter_ask_more_details_settings

## FAQ Settings: Training Conf
* ask_training_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* deny
    - utter_anything_else
  
## FAQ Settings: Training Conf
* ask_training_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
    

## FAQ Settings: Area of Testing -> Area of Testing Conf
* ask_area_of_testing
    - action_faq_selector
    - utter_area_of_testing_options
* ask_area_of_testing_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
    
## FAQ Settings: Source Field -> Source Field Conf
* ask_source_field
    - action_faq_selector
    - utter_source_field_options
* ask_source_field_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
    
## FAQ Settings: Bug Resolution -> Bug Resolution Conf
* ask_bug_resolution
    - action_faq_selector
    - utter_bug_resolution_options
* ask_bug_resolution_configure
    - action_faq_selector
    - utter_ask_more_details_settings
    
## FAQ Settings: Training Conf -> Source Field -> Source Field Conf
* ask_training_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
* ask_source_field
    - action_faq_selector
    - utter_source_field_options
* ask_source_field_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings

## FAQ Settings: Training Conf -> Area of Testing -> Area of Testing Conf
* ask_training_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
* ask_area_of_testing
    - action_faq_selector
    - utter_area_of_testing_options
* ask_area_of_testing_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings

## FAQ Settings: Training Conf -> Bug resolution -> Bug resolution Conf
* ask_training_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
* ask_bug_resolution
    - action_faq_selector
    - utter_bug_resolution_options
* ask_bug_resolution_configure
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
    
# ########################## Report ########################## #

## Report: Default Report
* report
    - report_form
    - form: {"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Nostradamus"}
    - slot{"project": "Nostradamus"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Yesterday"}
    - form: report_form
    - slot{"period": "Yesterday"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
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

## Report: Report -> Thanks
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Nostradamus"}
    - slot{"project": "Nostradamus"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Yesterday"}
    - form: report_form
    - slot{"period": "Yesterday"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* thanks
    - utter_noworries

## Report: Report -> Goodbye -> What do you can -> Goodbye
* report{"period": "today"}
    - report_form
    - form{"name": "report_form"}
    - slot{"period": "today"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Nostradamus"}
    - slot{"project": "Nostradamus"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Yesterday"}
    - form: report_form
    - slot{"period": "Yesterday"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* goodbye
    - utter_goodbye
* what_do_you_can
    - utter_what_do_you_can
* goodbye
    - utter_goodbye
    
## Report: Report -> Out of Scope -> Report
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* out_of_scope
    - utter_cannot_help
    - form{"name": null}
    - form: reset_slots
    - slot{"requested_slot": null}
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Nostradamus"}
    - slot{"project": "Nostradamus"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Yesterday"}
    - form: report_form
    - slot{"period": "Yesterday"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}

## Report: Report -> Out of Scope -> Report
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "period"}
* out_of_scope
    - utter_cannot_help
    - form{"name": null}
    - form: reset_slots
    - slot{"requested_slot": null}
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Nostradamus"}
    - slot{"project": "Nostradamus"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Today"}
    - form: report_form
    - slot{"period": "Today"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}


## Report: Report -> Out of Scope -> Report
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* out_of_scope
    - action_deactivate_form
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Nostradamus"}
    - slot{"project": "Nostradamus"}
    - slot{"requested_slot": "period"}
* form: inform{"period": "Today"}
    - form: report_form
    - slot{"period": "Today"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}

## Report: Report -> Out of Scope -> Report -> Out of Scope -> Report
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* out_of_scope
    - action_deactivate_form
    - utter_cannot_help
    - form{"name": null}
    - reset_slots
* report
    - report_form
    - slot{"requested_slot": "project"}
* out_of_scope
    - action_deactivate_form
    - utter_cannot_help
    - form{"name": null}
    - reset_slots
* report
    - report_form
    - slot{"requested_slot": "project"}
* out_of_scope
    - action_deactivate_form
    - utter_cannot_help
    - form{"name": null}
    - reset_slots
* report
    - report_form
    - slot{"requested_slot": "project"}

## Report: Greet -> Report -> Out of Scope -> Greet -> Report -> Out of Scope
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "All projects"}
    - slot{"project": "All projects"}
    - form: report_form
    - slot{"project": "All projects"}
    - slot{"requested_slot": "period"}
* form: out_of_scope
    - form: report_form
    - slot{"period": "[\"2020-08-12T20:59:59.000Z\",\"2020-08-12T20:59:59.000Z\"]"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Pick a project"}
    - slot{"project": "Pick a project"}
    - form: report_form
    - slot{"project": "Pick a project"}
    - slot{"requested_slot": "project_selection"}
* form: out_of_scope
    - form: report_form
    - slot{"project_selection": "[\"Lk\"]"}
    - slot{"requested_slot": "period"}
* form: out_of_scope
    - form: report_form
    - slot{"period": "[\"2020-08-12T20:59:59.000Z\",\"2020-08-12T20:59:59.000Z\"]"}
    - form: reset_slots
    - form{"name": null}
    - slot{"requested_slot": null}

## Report: Greet -> Report -> Out of Scope -> Greet
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* form: inform{"project": "Pick a project"}
    - slot{"project": "Pick a project"}
    - form: report_form
    - slot{"project": "Pick a project"}
    - slot{"requested_slot": "project_selection"}
* form: out_of_scope
    - form: report_form
    - slot{"project_selection": "[\"ActiveMQ Artemis\"]"}
    - slot{"requested_slot": "period"}
* form: out_of_scope
    - form: report_form
    - slot{"period": "[\"2020-08-05T20:59:59.000Z\",\"2020-08-06T20:59:59.000Z\"]"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - form: reset_slots
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help


## Report: Report -> Greet -> Training Conf -> Area of Testing ->
##         Area of Testing Conf -> Report -> A&T -> Help
* report
    - report_form
    - form{"name": "report_form"}
    - form{"name": null}
    - reset_slots
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help
* ask_training_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
* ask_area_of_testing
    - action_faq_selector
    - utter_area_of_testing_options
* ask_area_of_testing_configuring
    - action_faq_selector
    - utter_ask_more_details_settings
* deny
    - utter_anything_else
* report
    - report_form
    - form{"name": "report_form"}
    - form{"name": null}
    - reset_slots
* ask_analysis_and_training
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else

## Report: Report -> Out of Scope -> Greet
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* out_of_scope
    - action_deactivate_form
    - form{"name": null}
    - reset_slots
    - utter_cannot_help
* greet
    - utter_greet
    - utter_describe_yourself
    - utter_ask_help

## Report: Report -> Out of Scope -> Out of Scope -> Report
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* out_of_scope 
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_cannot_help
* out_of_scope
    - utter_cannot_help
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}

## Report: Report -> Filter -> Filter WF -> Filter Drop-down
##         Report -> Bug Resolution Conf 
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_filter
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_filter_menu
* ask_filter_workflow
    - action_faq_selector
    - utter_filtration_types
* ask_filter_dropdown_type
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
* deny
    - utter_anything_else
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_bug_resolution_configure
    - action_custom_fallback
    - form{"name": null}
    - reset_slots
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
    
## Report: Report -> A&T
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_analysis_and_training
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## Report: Report -> Filter
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_filter
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_filter_menu

## Report: Report -> Filter WF
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_filter_workflow
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_filtration_types

## Report -> Filter Date
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_filter_date_type
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## Report: Report -> Filter Numeric
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_filter_numeric_type
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## Report: Report -> Frequently Terms
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_frequently_terms
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_frequently_terms_options

## Report: Report -> Frequently Terms WF
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_frequently_terms_workflow
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training
    
## Report: Report -> Significant Terms
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_significant_terms
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_significant_terms_options

## Report: Report -> Significant Terms WF
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_significant_terms_workflow
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## Report: Report -> Defect Submission
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_defect_submission
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## Report: Report -> Statistics
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_statistics
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training


## Report: Report -> Training
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_training
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_training_options

## Report: Report -> Training Purpose
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_training_purpose
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_training_purpose_options

## Report: Report -> Training Workflow
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_training_workflow
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_analysis_and_training

## Report: Report -> Training DIY
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_training_diy
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_training_diy_options

## Report: Report -> DAS
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_description_assessment
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector

## Report: Report -> QAM
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_qa_metrics
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    
## Report: Report -> Training Conf
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_training_configuring
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings
    
## Report: Report -> Source Field
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_source_field
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_source_field_options

## Report: Report -> Source Field Conf
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_source_field_configuring
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings

## Report: Report -> Area of Testing
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_area_of_testing
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_area_of_testing_options

## Report: Report -> Area of Testing Conf
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_area_of_testing_configuring
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings

## Report: Report -> Bug resolution
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_bug_resolution
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_bug_resolution_options
    
## Report: Report -> Bug resolution Conf   
* report
    - report_form
    - form{"name": "report_form"}
    - slot{"requested_slot": "project"}
* ask_bug_resolution_configure
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_faq_selector
    - utter_ask_more_details_settings
* affirm
    - utter_more_details_settings