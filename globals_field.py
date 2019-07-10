'''
/*******************************************************************************
* Copyright 2016-2019 Exactpro (Exactpro Systems Limited)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
******************************************************************************/
'''


mandatory_fields = [{'gui_name': 'Issue_key', 'xml_name': 'Issue key',
                     'type': 'text'},
                    {'gui_name': 'Summary', 'xml_name': 'Summary',
                     'type': 'text1'},
                    {'gui_name': 'Status', 'xml_name': 'Status',
                     'type': 'categorical'},
                    {'gui_name': 'Project_name', 'xml_name': 'Project name',
                     'type': 'categorical'},
                    {'gui_name': 'Priority', 'xml_name': 'Priority',
                     'type': 'categorical'},
                    {'gui_name': 'Resolution', 'xml_name': 'QA Resolution',
                     'type': 'categorical'},
                    {'gui_name': 'Components', 'xml_name': 'Components',
                     'type': 'text2'},
                    {'gui_name': 'Labels', 'xml_name': 'Labels',
                     'type': 'text2'},
                    {'gui_name': 'Version', 'xml_name': 'Version',
                     'type': 'text2'},
                    {'gui_name': 'Description', 'xml_name': 'Description',
                     'type': 'text1'},
                    {'gui_name': 'Comments', 'xml_name': 'Comments',
                     'type': 'number'},
                    {'gui_name': 'Attachments', 'xml_name': 'Attachments',
                     'type': 'number'},
                    {'gui_name': 'Created', 'xml_name': 'Date Created',
                     'type': 'date'},
                    {'gui_name': 'Resolved', 'xml_name': 'Date Resolved',
                     'type': 'date'}]

data_types = ['text', 'text1', 'text2', 'number', 'date', 'categorical', 'bool']

referring_to = ["Resolution", "Priority"]

requared_files = ['regularExpression', 'myconf']
