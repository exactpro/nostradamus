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


from re import sub, compile
from html import unescape
from csv import reader
from pathlib import Path


regular_expressions = [
                compile(reg_expression) for reg_expression_object in reader(
                    open(str(Path(__file__).parents[1]) + '/extensions/' + 'regularExpression.csv'),
                    delimiter=',',
                    quotechar='"') for reg_expression in reg_expression_object if reg_expression]


def clean_description(text, regular_expressions=regular_expressions):
    if not text:
        return 'None'
    else:
        cleaned_text = str(unescape(text).encode(
            "utf-8")).replace('b', '', 1)
        for reg_expression_object in regular_expressions:
            cleaned_text = sub(reg_expression_object, ' ', cleaned_text).strip()
            if not cleaned_text:
                return 'aftercleaning'
        return cleaned_text
