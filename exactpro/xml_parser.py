import os
import pandas
from werkzeug.utils import secure_filename
from lxml import objectify
import csv
from datetime import datetime as dt
import re
from decimal import Decimal, InvalidOperation
from html import unescape


def clean_description(original_text):
    if not original_text:
        return 'default_descr_value'
    else:
        cleaned_text = str(unescape(original_text).encode("utf-8")).replace('b', '', 1)
        with open('regularExpression.csv') as csv_file:
            for reg_expression_object in [re.compile(reg_expression) for reg_expression_object in
                                           csv.reader(csv_file, delimiter=',', quotechar='"') for reg_expression in
                                           reg_expression_object if
                                           reg_expression]:
                cleaned_text = re.sub(reg_expression_object, ' ', cleaned_text)
                if cleaned_text.isspace():
                    cleaned_text = 'aftercleaning'
        return cleaned_text.strip()


class XMLParser:
    def __init__(self, xml_file, path):
        self.file = open(path, 'w')
        self.csvwriter = csv.writer(self.file)
        self.count_version = 0
        self.count_comment = 0
        self.count_attachments = 0
        self.count_component = ''
        self.count_labels = ''
        self.count_item = 0
        self.version = ''
        self.asignee_reporter = []
        self.xml = xml_file.read()
        self.root = objectify.fromstring(self.xml)

    def parse_xml(self, mandatory_fields, special_fields, asignee_reporter_store):
        try:
            self.head = mandatory_fields + ['Affects_Ver'] + special_fields
            self.row = {k: None for k in self.head}
            self.csvwriter.writerow(self.head)

            for self.rssChilds in self.root.getchildren():
                if self.rssChilds.tag != 'channel':
                    raise Exception('XML has no valid tree, channel child is absent')
                for self.channelChilds in self.rssChilds.getchildren():
                    if self.channelChilds.tag == 'item':
                        self.count_item = self.count_item + 1
                        try:
                            for self.chield in self.channelChilds.getchildren():
                                if self.chield.tag == 'key':
                                    self.row["Issue_key"] = self.chield.text
                                if self.chield.tag == 'status':
                                    self.row["Status"] = self.chield.text
                                if self.chield.tag == 'summary':
                                    self.row["Summary"] = self.chield.text
                                if self.chield.tag == 'project':
                                    self.row["Project_name"] = self.chield.text
                                if self.chield.tag == 'priority':
                                    self.row["Priority"] = self.chield.text
                                if self.chield.tag == 'resolution':
                                    self.row["Resolution"] = self.chield.text
                                if self.chield.tag == 'created':
                                    self.row["Created"] = XMLParser.get_date(self, self.chield.text)
                                if self.chield.tag == 'resolved':
                                    self.row["Resolved"] = XMLParser.get_date(self, self.chield.text)
                                if self.chield.tag == 'description':
                                    self.row["Description"] = clean_description(self.chield.text)
                                if self.chield.tag == 'version':
                                    self.count_version = self.count_version + 1
                                    if self.version != '':
                                        self.version = self.version + ',' + self.chield.text
                                    else:
                                        self.version = self.chield.text
                                if self.chield.tag == 'component':
                                    if self.count_component != '':
                                        self.count_component = self.count_component + ',' + self.chield.text
                                    else:
                                        self.count_component = self.chield.text
                                if self.chield.tag == 'labels':
                                    for self.chieldLab in self.chield.getchildren():
                                        if self.chieldLab.text is not None:
                                            if self.count_labels != '':
                                                self.count_labels = self.count_labels + ',' + self.chieldLab.text
                                            else:
                                                self.count_labels = self.chieldLab.text
                                if self.chield.tag == 'customfields':
                                    if bool(special_fields):
                                        for self.chieldCust in self.chield.getchildren():
                                            try:
                                                if self.chieldCust.customfieldname.text in special_fields:
                                                    if self.chieldCust.customfieldvalues.getchildren():
                                                        value = self.chieldCust.customfieldvalues.customfieldvalue.text
                                                        self.row[self.chieldCust.customfieldname.text] = value
                                                    else:
                                                        self.row[self.chieldCust.customfieldname.text] = None
                                                        
                                            except AttributeError as e:
                                                raise Exception(str(e))
                                if self.chield.tag == 'comments':
                                    for comment in self.chield.getchildren():
                                        self.count_comment = self.count_comment + 1
                                if self.chield.tag == 'attachments':
                                    for attachment in self.chield.getchildren():
                                        self.count_attachments = self.count_attachments + 1
                                if self.chield.tag == 'assignee':
                                    self.asignee_reporter = self.asignee_reporter + self.chield.text.lower().split()
                                if self.chield.tag == 'reporter':
                                    self.asignee_reporter = self.asignee_reporter + self.chield.text.lower().split()

                            self.row["Comments"] = self.count_comment
                            self.row["Attachments"] = self.count_attachments
                            self.row["Version"] = self.version
                            self.row["Affects_Ver"] = self.count_version
                            self.row["Components"] = self.count_component
                            self.row["Labels"] = self.count_labels
                            
                            self.csvwriter.writerow([self.row[el] for el in self.head])

                            self.count_version = 0
                            self.count_component = ''
                            self.count_labels = ''
                            self.row = {k: None for k, v in self.row.items()}
                            self.count_attachments = 0
                            self.count_comment = 0
                            self.version = ''
                        except AttributeError as e:
                            raise Exception(str(e))
            if asignee_reporter_store['asigneeReporter']:
                asignee_reporter_store['asigneeReporter'] = list(set(self.asignee_reporter))
            self.file.close()
        except Exception as e:
            raise Exception(str(e))

    def get_date(self, date):
        if not date:
            return ''
        self.d = dt.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        self.day = self.d.day.__str__()
        self.month = self.d.month.__str__()
        if self.d.day.__str__().__len__() == 1:
            self.day = '0' + self.day
        if self.month.__str__().__len__() == 1:
            self.month = '0' + self.month

        date = self.day + '-' + self.month + '-' + self.d.year.__str__()
        return date


class FileSwitcher(XMLParser):
    def __init__(self, file_info_store, xml_file, asignee_reporter_store):
        self.file_info_store = file_info_store
        self.xml_file = xml_file
        self.asignee_reporter_store = asignee_reporter_store
        self.filename, self.file_extension = os.path.splitext(self.xml_file.filename)
        if self.file_extension == '.xml':
            XMLParser.__init__(self, xml_file, '{0}/{1}.csv'.format(file_info_store.upload_folder, secure_filename(xml_file.filename) if
                                                                    secure_filename(xml_file.filename) != 'xml.csv'
                                                                    else asignee_reporter_store.sid+secure_filename(xml_file.filename)))

    @staticmethod
    def decimal_from_value(value):
        return Decimal(value)

    def open_file(self, mandatory_fields, special_fields=[], fields_to_convert=[]):
        if self.file_extension == '.csv':
            self.data = pandas.read_csv(self.xml_file)
            return self.data
        else:
            try:
                XMLParser.parse_xml(self, mandatory_fields, special_fields, self.asignee_reporter_store)
                # convertion to Pandas DataFrame (read_csv method)
                # Decimal data type assigning for numeric fields (field names are listed in "converters" parameter)
                self.data = pandas.read_csv(open('{0}/{1}.csv'.format(self.file_info_store.upload_folder, secure_filename(self.xml_file.filename) if
                                                  secure_filename(self.xml_file.filename) != 'xml.csv'
                                                  else self.asignee_reporter_store.sid+secure_filename(self.xml_file.filename)), 'r'),
                                                  converters={field : self.decimal_from_value for field in fields_to_convert}
                                                      )
                if self.data.empty:
                    raise Exception('loading empty file, please load not empty')
                return self.data
            except Exception as e:
                raise Exception(str(e))
            finally:
                # remove file after uploading to RAM
                os.remove('{0}/{1}.csv'.format(self.file_info_store.upload_folder, secure_filename(self.xml_file.filename)))

