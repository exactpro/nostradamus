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

referring_to = ["Resolution", "Priority", "Areas of testing"]

requared_files = ['regularExpression', 'myconf']

