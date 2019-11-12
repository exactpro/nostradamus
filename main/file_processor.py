'''
*******************************************************************************
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
*******************************************************************************
'''

import pandas
import multiprocessing
import time
from uuid import uuid4
from os.path import exists, getsize, join, splitext
from os import getcwd, listdir, chdir, remove
from pandas import DataFrame, merge, read_csv
from csv import writer, DictWriter
from lxml import objectify
from datetime import datetime as dt
from decimal import Decimal
from flask import session
from decimal import Decimal
from pathlib import Path

from main.data_converter import convert_date
from main.validation import is_subset, is_in
from main.data_analysis import reindex_dataframe, transform_series


def check_file_extension(*filenames):
    """ Checks whether the passed files have allowed extension.

    Parameters:
        filenames (str): files' names.

    Returns:
        Boolean value representing checking results.
    """
    return all([is_in(Path(str(file)).suffix.rsplit('.', 1)[1], session['config.ini']['REQUIREMENTS']['file_extensions']) for file in filenames])


def check_file_extensions(files):
    """ Checks whether the file extension is valid.

    Parameters:
        files (list): List of FileStorage objects.

    Returns:
        Boolean value.   

    """
    return all([ext in session['config.ini']['REQUIREMENTS']['file_extensions']
                for ext in [file.filename.rsplit('.', 1)[1] for file in files]])


def is_file_exist(*files, check_size=False):
    """ Checks file's existence.

    Parameters:
        files (args): files' paths;
        check_size (bool): size checking flag.

    Returns:
        Boolean value.

    """
    for file in files:
        if check_size:
            if not exists(file) or getsize(file) == 0:
                return False
        else:
            if not exists(file):
                return False
    return True


def save_file(df, markup, defect_attributes, destination_path):
    """ Saves dataframe to csv file.

        Parameters:
            df (DataFrame): Dataframe;
            markup (int): indicates whether the markup is set;
            defect_attributes(dict): defect attributes;
            destination_path (str): path to a directory where the file to be saved.

    """
    if markup == 0:
        df.to_csv(
            destination_path,
            columns=[
                el for el in defect_attributes['mandatory_attributes']] + [
                el for el in defect_attributes['special_attributes'] if defect_attributes['special_attributes'][el]['name'] != 'ttr'],
            index=False)
    else:
        df.to_csv(
            destination_path,
            columns=[el for el in defect_attributes['mandatory_attributes']] +
            [el for el in defect_attributes['special_attributes'] if defect_attributes['special_attributes'][el]['name'] != 'ttr'] +
            [defect_attributes['mark_up_attributes'][el]['gui_name'] + '_lab' for el in defect_attributes['mark_up_attributes']],
            index=False)


def save_predictions(table, file_path):
    """ Saves the table to the specified address.

        Parameters:
            table (dict): predictions table;
            file_path (str): file's path.

    """
    table['Key'] = table.index.tolist()
    table.to_csv(file_path, index=False)


def remove_models():
    models_dir = str(Path(__file__).parents[1]) + '/model/'
    for model in [join(models_dir, file) for file in listdir(
            models_dir) if file.endswith('.sav')]:
        remove(model)


class FileProcessor():
    def __init__(self, file, backup_path, defect_attributes):
        self.__file = file
        self.__filename, self.__file_extension = splitext(file.filename)
        self.backup_path = backup_path
        self.defect_attributes = defect_attributes

    def read_file(self):
        return self.__file.read()

    def parse_xml(self, xml_file):
        headers = set(self.defect_attributes)
        defects = []
        
        root = objectify.fromstring(xml_file).getchildren()
        multiple_value_fields = ['version', 'component']
        for channel in root:
            for item in channel.getchildren():
                defect = {}
                if item.tag == 'item':
                    defect['Affects_Ver'] = len(
                        [el.text for el in item.iter('version')])
                    defect['Comments'] = 0
                    headers.add('Affects_Ver')
                    headers.add('Comments')
                    for element in multiple_value_fields:
                        name = element.capitalize()
                        text = ','.join(
                            [el.text for el in item.iter(element)]).strip()
                        if element == 'component':
                            name = 'Components'
                        defect[name] = text
                        headers.add(name)
                    for element in item.getchildren():
                        if element.tag not in multiple_value_fields:
                            if element.tag == 'customfields':
                                for custom_field in element.getchildren():
                                    if custom_field.customfieldname:
                                        name = custom_field.customfieldname.text
                                        text = custom_field.customfieldvalues.customfieldvalue.text.strip(
                                        ) if custom_field.customfieldvalues.getchildren() and custom_field.customfieldvalues.customfieldvalue.text else None
                                        defect[name] = text.strip(
                                        ) if text else None
                                        headers.add(name)
                            elif element.tag == 'labels':
                                defect[element.tag.capitalize()] = ','.join(
                                    [el.text for el in element.iter('label')]).strip()
                                headers.add(element.tag.capitalize())
                            elif element.tag == 'comments':
                                defect[element.tag.capitalize()] = len(
                                    element.getchildren())
                                headers.add(element.tag.capitalize())
                            elif element.tag == 'attachments':
                                defect[element.tag.capitalize()] = len(
                                    element.getchildren())
                                headers.add(element.tag.capitalize())
                            else:
                                name = element.tag.capitalize()
                                text = element.text
                                defect[name] = text.strip() if text else None
                                headers.add(name)
                    defects.append(defect)
        return list(headers), defects

    def to_csv(self, header, content):
        with open(self.backup_path, 'w') as file:
            csv_file = DictWriter(file, fieldnames=header)
            csv_file.writeheader()
            for element in content:
                csv_file.writerow(element)
        return read_csv(open(self.backup_path))

    def process_file(self):
        if self.__file_extension == '.csv':
            return read_csv(self.__file)
        elif self.__file_extension == '.xml':
            xml = self.read_file()
            headers, defects = self.parse_xml(xml)
            return self.to_csv(headers, defects)


def convert_to_dataframe(files):
    """ Makes dataframe from passed files.

    Parameters:
        files: xml or csv files' list.

    Returns:
        dataframe with parsed files' data.

    """
    if not check_file_extensions(files):
        raise Exception('Oops! Incorrect file format.\nAllowed formats: {}'.format(
            ','.join(session['config.ini']['REQUIREMENTS']['file_extensions'])))
    session['backup']['uploaded_files'] = []

    pool = multiprocessing.Pool()
    for file in files:
        backup_path = session['backup']['backup_folder'] + \
            str(uuid4()) + '.csv'
        session['backup']['uploaded_files'].append(backup_path)
        pool.apply_async(FileProcessor(file, backup_path, list(
            session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes'].keys()) +
            list(
            session['config.ini']['DEFECT_ATTRIBUTES']['special_attributes'].keys())).process_file())
    pool.close()
    pool.join()
    dataframes = [read_csv(df) for df in session['backup']['uploaded_files']]

    df = transform_series(
        reindex_dataframe(
            pandas.concat(
                dataframes,
                sort=False)),
        session['config.ini']['DEFECT_ATTRIBUTES'])
    if not is_subset(
            list(
                session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes'].keys()),
            df.keys()):
        raise Exception(
            'Oops! Please check that the uploaded file has the following fields:\n{}'.format(
                ', '.join(
                    list(
                        session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes'].keys()))))
    return df

