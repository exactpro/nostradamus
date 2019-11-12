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


from datetime import datetime as dt
from decimal import Decimal
import pandas
import datetime
import math
from ast import literal_eval


def parse_period(period):
    if period == '1 week':
        return 'W-SUN'
    if period == '10 days':
        return '10D'
    if period == '3 months':
        return '3M'
    if period == '6 months':
        return '6M'
    if period == '1 year':
        return 'A-DEC'


def unpack_dictionary_val_to_list(dictionary):
    unpacked_list = [
        el for el in dictionary.values() if not isinstance(
            el, list)]
    for el in [el for el in dictionary.values() if isinstance(el, list)]:
        unpacked_list += el
    return unpacked_list


# converts date to DD-MM-YYYY
def convert_date(original_date):
    if not original_date:
        return ''
    formatted_date = dt.strptime(original_date, '%a, %d %b %Y %H:%M:%S %z')
    formatted_date = formatted_date.strftime('%d-%m-%Y')
    return formatted_date


def math_round(number):
    if number - math.floor(number) < 0.5:
        return math.floor(number)
    return math.ceil(number)


def convert_config(original_config):
    """Converts stringified dict values to python datatypes.

    Parameters:
        original_config (dict): config data parsed to dict

    Returns:
        formated_config: dict with values converted to python datatypes.
    """

    formated_config = {}
    for section in original_config:
        formated_config[section] = {}
        for option in original_config[section]:
            try:
                formated_config[section][option] = literal_eval(original_config[section][option])
            except (ValueError,SyntaxError):
                formated_config[section][option] = original_config[section][option]
    return formated_config


def stringify_date(date, step_size):
    """Stringifies date argument value for specific period.

    Parameters:
        date (date): date in original format;
        step_size (str): step size value.

    Returns:
        date(str): stringified date value.
    """

    if date == None:
        return ''

    day = date.day
    month = date.month
    year = date.year

    if step_size == '10D' or step_size == 'W-SUN':
        date = datetime.date(year, month, day).strftime("%Y-%m-%d")
        return date
    if step_size in ['3M', '6M']:
        month = str(month)
        if len(month)==1:
            month = '0' + month
        date = datetime.datetime.date(pandas.to_datetime(str(year) +"-" + month)).strftime("%Y-%m")
        return date
    if step_size == 'A-DEC':
        return datetime.datetime.date(pandas.to_datetime(str(date.year))).strftime("%Y")



