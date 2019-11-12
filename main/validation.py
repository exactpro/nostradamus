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


def is_empty(val):
    return bool(val)


# verifies that all fields from current_elements are subset of mandatory_elements
def is_subset(current_elements, mandatory_elements):
    return set(current_elements).issubset(set(mandatory_elements))


def is_greater(attributes, max_quantity):
        attr_count = 0
        for attribute in attributes:
            if isinstance(attributes[attribute], (list, tuple)):
                attr_count += len(attributes[attribute])
            else:
                attr_count += 1
        return attr_count == max_quantity


def is_zero(val):
        if val < 0:
            return 0
        else:
            return val


# verifies whether the GUI fields count equals to config fields count
def document_verification(data, fields_data):
    return not bool(set(fields_data).difference(set(data.keys()).intersection(set(fields_data))))


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_in(available, mandatory):
    return available in mandatory

