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


import configparser
from configparser import ConfigParser

from flask import session
import os
from os.path import exists
from pathlib import Path
from ast import literal_eval

from main.validation import is_empty, is_subset, is_greater
from main.exceptions import ModelNotFound, ModelsNotFound
from main.file_processor import is_file_exist
from main.training import get_models_names, are_models_exist
from main.data_converter import unpack_dictionary_val_to_list, convert_config


class Configuration(ConfigParser):
    def __init__(self, config_path):
        self.config_path = config_path
        self.__config = ConfigParser()
        self.__sections = []
        self.__options = []

    @property
    def sections(self):
        self.read_config()
        self.__sections = self.__config.sections()
        return self.__sections

    @property
    def options(self):
        self.read_config()
        self.__options = [
            option for section in self.sections for option in self.__config.options(section)]
        return self.__options

    def read_config(self):
        self.__config.read(self.config_path)

    def get_settings(self):
        sections = self.sections
        return {section: dict(self.__config.items(section))
                for section in sections}

    def create_config(self, *sections):
        for section in sections:
            self.__config.add_section(section)
        with open(self.config_path, "w") as config_file:
            return self.__config.write(config_file)

    def set_option(self, section, option, value):
        self.read_config()
        self.__config.set(section, option, value)
        with open(self.config_path, "w") as config_file:
            self.__config.write(config_file)


def check_defect_attributes(defect_attributes):
    mandatory_multiple_mode_fields = [
        'Issue_key', 'Summary', 'Priority', 'Description']
    try:
        # checks that received multiple mode's fields are in mandatory
        # attributes list
        if not is_subset(
                defect_attributes['multiple_mode_attributes'],
                mandatory_multiple_mode_fields):
            return False, '{} are mandatory for Multiple Description Mode.'.format(
                ', '.join(mandatory_multiple_mode_fields))

        # checks that mandatory/special attributes have correct data types
        allowed_data_types = [
            'String',
            'Substring',
            'Substring_array',
            'Numeric',
            'Date',
            'Categorical',
            'Boolean']
        if not is_subset([defect_attributes[defect_attributes_group][field]['type']
                            for defect_attributes_group in ['mandatory_attributes', 'special_attributes']
                            for field in defect_attributes[defect_attributes_group]],
                            allowed_data_types):
            return False, 'Oops! Incorrect data type specified in mandatory or special attributes. Allowed data types: {}'.format(
                ', '.join(allowed_data_types))

        # checks that quantity of received resolution's elements isn't greater than specified quantity
        # because it cannot has more than two values in the list
        if not is_greater(defect_attributes['resolution'], 2):
            return False, 'Oops! Resolution field cannot has more than two values.'

        # checks that mandatory attributes are specified in config.ini
        if not is_empty(defect_attributes['mandatory_attributes']):
            return False, 'Oops! Mandatory attributes aren\'t specified.'

        special_attributes = set(defect_attributes['special_attributes'].keys()).union({defect_attributes['special_attributes'][el]['name'] for el in defect_attributes['special_attributes'].keys()})
        mandatory_attributes = set(defect_attributes['mandatory_attributes'].keys()).union({defect_attributes['mandatory_attributes'][el]['name'] for el in defect_attributes['mandatory_attributes'].keys()})
        for attribute in special_attributes:
            if attribute in mandatory_attributes:
                return False, 'Oops! {attribute} is already specified in Mandatory attributes.'.format(attribute=attribute)

        # checks that all received Referring to's fields (except Areas of
        # testing) do exist in mandatory/special attributes
        if not is_subset([el for el in defect_attributes['referring_to'] if el != 'Areas of testing'], list(
                defect_attributes['mandatory_attributes'].keys()) + list(defect_attributes['special_attributes'].keys())):
            return False, 'Oops! Referring to fields should be presented in mandatory or special attributes.'
        
        if ('Areas of testing' in defect_attributes['referring_to']) and not (is_empty(defect_attributes['mark_up_attributes'])):
            return False, 'Oops! Area of testing section is empty.\
            Please specify areas of testing before assigning this element to Referring to section.'
        if 'Areas of testing' in defect_attributes['referring_to'] and (not is_file_exist(str(Path(__file__).parents[1]) + '/model/' + 'top_terms.csv', check_size=True)):
                return False, 'Oops! Areas of testing couldn\'t be added to Referring to field while models aren\'t trained.' \
                    '\nPlease train models firstly.'

        if not set(defect_attributes['resolution'].keys()).issubset(set(field for group in ['mandatory_attributes', 'special_attributes'] for field in defect_attributes[group].keys())):
            return False, 'Oops! Resolution fields should be presented in Mandatory or Special fields.'

        if not all([field_type == 'Categorical' for field_type in {defect_attributes[group][field]['type'] for group in ['mandatory_attributes', 'special_attributes'] for field in defect_attributes['resolution'].keys() if field in defect_attributes[group]}]):
            return False, 'Oops! Resolution fields should have Categorical datatype.'

        return True, None
    except Exception as e:
        return False, str(e)


def check_predictions_parameters_config():
    try:
        config_exist = is_file_exist(
            str(Path(__file__).parents[1]) + '/model/' + 'predictions_parameters.ini')
        if not config_exist:
            return {
                'single_mode': False,
                'multiple_mode': False,
                'err_message': ''}
        else:
            # checking existence of common models
            are_models_exist(get_models_names() + ['ttr'])
            # checking model's existence required for 
            # single description mode only
            are_models_exist(['priority'])
            # checking top_terms.csv file existence which is required 
            # for single description mode
            if not is_file_exist(
                    str(Path(__file__).parents[1]) + '/model/' + 'top_terms.csv'):
                raise FileNotFoundError('Can\'t find top_terms.csv file.')
        return {'single_mode': True, 'multiple_mode': True, 'err_message': ''}
    except ModelsNotFound as err:
        return {
            'single_mode': False,
            'multiple_mode': False,
            'err_message': str(err)}
    except ModelNotFound as err:
        return {
            'single_mode': False,
            'multiple_mode': True,
            'err_message': str(err)}
    except FileNotFoundError as err:
        return {
            'single_mode': False,
            'multiple_mode': True,
            'err_message': str(err)}
    except (KeyError, SyntaxError) as err:
        return {
            'single_mode': False,
            'multiple_mode': False,
            'err_message': str(err)}


def load_base_config():
    session['frame_store'] = {
        'orig_frame': 'orig_frame',
        'new_data': 'new_data',
        'tr_frame': 'tr_frame',
        'frame_multiple': 'frame_multiple'
    }

    session['file_expire'] = {
        'orig_frame': 'orig_frame',
        'new_data': 'new_data',
        'tr_frame': 'tr_frame',
        'frame_multiple': 'frame_multiple'
    }


def add_calculated_fields_to_session(file_name):
    if file_name == 'config.ini':
        session[file_name]['REQUIREMENTS']['max_file_size'] = session[file_name]['REQUIREMENTS']['max_file_size'] * 1000**2
    elif file_name == 'predictions_parameters.ini':
        session[file_name]['predictions_parameters']['available_predictions_parameters'] = [option_name for option_name in session[file_name]['predictions_parameters'] if option_name != 'available_predictions_parameters']


def load_config_to_session(path):
    file_name = path.split('/')[-1]
    session[file_name] = convert_config(Configuration(path).get_settings())
    add_calculated_fields_to_session(file_name)


def update_defect_attributes():

    creator = Configuration('{}/config.ini'.format(os.curdir))

    creator.set_option(
        'DEFECT_ATTRIBUTES',
        'mandatory_attributes',
        str(session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes']))

    creator.set_option(
        'DEFECT_ATTRIBUTES',
        'special_attributes',
        str(session['config.ini']['DEFECT_ATTRIBUTES']['special_attributes']))

    creator.set_option(
        'DEFECT_ATTRIBUTES',
        'mark_up_attributes',
        str(session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes']))

    creator.set_option(
        'DEFECT_ATTRIBUTES',
        'logging_level',
        str(session['config.ini']['DEFECT_ATTRIBUTES']['logging_level'] ))

    creator.set_option(
        'DEFECT_ATTRIBUTES',
        'referring_to',
        str(session['config.ini']['DEFECT_ATTRIBUTES']['referring_to']))

    creator.set_option(
        'DEFECT_ATTRIBUTES',
        'multiple_mode_attributes',
        str(session['config.ini']['DEFECT_ATTRIBUTES']['multiple_mode_attributes']))

    creator.set_option(
        'DEFECT_ATTRIBUTES',
        'resolution',
        str(session['config.ini']['DEFECT_ATTRIBUTES']['resolution']))
