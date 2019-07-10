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


from pathlib import Path
import os
from ldap3 import Server, Connection, SUBTREE, ALL, core
import pandas
import datetime
from werkzeug.utils import secure_filename
from exactpro.config_parser import SettingProvider
from exactpro.exceptions import LDAPError
from exactpro.exceptions import IncorrectValueError, NotExist, NotExistModel, NotExistFile, NotExistField, LDAPError
from flask import session
import numpy


class Checker:
    def is_empty(self, val):
        return not bool(val)

    def is_subset(self, inner, outer):
        return set(inner).issubset(set(outer))

    def no_more(self, val, maxx):
        sum = 0
        for el in val:
            if isinstance(val[el], (list, tuple)):
                sum += len(val[el])
            else:
                sum += 1 
        return sum == maxx

    def get_resolutions(self, data):
        resolutions = [el for el in data.values() if not isinstance(el, list)]
        for el in [el for el in data.values() if isinstance(el, list)]:
            resolutions += el
        return resolutions

    # checks whether the models are exist
    def check_exist_model(self, model_names):
        if not isinstance(model_names, str):
            for name in model_names:
                name = secure_filename(name) # converting the filename to secure form (exmpl: Won't fix -> Wont_fix)
                if not os.path.exists(str(Path(__file__).parents[2])+'/model/'+name+'.sav'):
                    return True, name
            return False, name
        else:
            model_names = secure_filename(model_names)
            if not os.path.exists(str(dirname(dirname(dirname(realpath(__file__)))))+'/model/'+model_names+'.sav'):
                return True, model_names
            return False, model_names

    # user authorisation and authentification
    def check_user(self, username, password, store):
        ad_user = username + store.ad_domain_suffix
        ad_passw = password

        # LDAP-connenction creation
        server = Server(store.ad_server, get_info=ALL)
        conn = Connection(server, user=ad_user, password=ad_passw, auto_bind='NONE', version=3, authentication='SIMPLE',
                          client_strategy='SYNC', auto_referrals=True, check_names=True, read_only=False, lazy=False,
                          raise_exceptions=False)
        try:
            if not conn.bind():
                raise LDAPError('The username or password is incorrect') # raises in case when user can't connect to database
        except core.exceptions.LDAPPasswordIsMandatoryError:
            raise LDAPError('The username or password is incorrect')

        conn.search(store.ad_search_tree, '(memberOf:1.2.840.113556.1.4.1941:='+store.ad_security_group+')',
                    SUBTREE,
                    attributes=['sAMAccountName']
                    )

        user_in_group = False
        for entry in conn.entries:
            if entry.sAMAccountName == username:
                user_in_group = True
                break
        return user_in_group

    def allowed_file(self, filename, store):
        return all(['.' in name for name in [el.filename for el in filename]]) and all([ext in store.allowed_extensions for ext in [el.filename.rsplit('.', 1)[1] for el in filename]])

    def allowed_file1(self, filename, store):
        return '.' in filename and filename.rsplit('.', 1)[1] in store.allowed_extensions

    # drop-down fields preparation
    def prepare_categorical(self, data, fields_data, ref_to_data):
        # checks whether the uploaded file isn't xml
        if Checker.document_verification(self, data, list(fields_data['mandatory_fields'].keys()) + list(fields_data['special_fields'].keys())):
            # getting the unique values of categorical type fields from "mandatory_fields" list to place them inside drop-down fields on GUI
            # use ['null'] to disable field on gui
            self.fields = {k: ['null'] if not data[k].dropna().unique().tolist() else data[k].dropna().unique().tolist()
                           for k in list(fields_data['mandatory_fields'].keys()) 
                           if fields_data['mandatory_fields'][k]['type'] == 'categorical'}
 
            # getting the values list for "Referring to" drop-down field
            self.ref_to = [el+' '+el1 for el in ref_to_data['referring_to'] for el1 in data[el].dropna().unique().tolist()]
            self.fields.update({'ReferringTo': ['null'] if not self.ref_to else self.ref_to})
            
            # getting the unique values of categorical type fields from "special_fields" list to place them inside drop-down fields on GUI
            self.fields.update({el: ['null'] if not data[el].dropna().unique().tolist() else data[el].dropna().unique().tolist()
                                for el in list(fields_data['special_fields'].keys())
                                if fields_data['special_fields'][el]['type'] == 'categorical'})
            return self.fields
        else:
            raise Exception('Document is not valid. Please check that document has the following fields:' + \
                            ','.join(list(fields_data['mandatory_fields'].keys())) + ','.join(list(fields_data['special_fields'].keys())))

    # verifies whether the GUI fields count equals to config fields count
    def document_verification(self, data, fields_data):
        return not bool(set(fields_data).difference(set(data.keys()).intersection(set(fields_data))))

    # fields type converter
    # reason: Pandas could make a mistake with field type initialisation  
    # solution: change NaN field values to default value
    def transform_fields(self, data, fields_data):
        try:
            for self.group in fields_data:
                for self.field in fields_data[self.group]:
                    if fields_data[self.group][self.field]['type'] == 'text':
                        # blocks column if column is empty
                        if len(data[self.field].dropna().unique().tolist()) == 0:
                            continue
                        else:
                            try:
                                if data[self.field].dtype != 'object':
                                        data[self.field] = data[self.field].apply(str)  # applies str data type to column
                                # makes a copy of series with 'text' data type ()
                                data[self.field+'_tr'] = data[self.field].fillna(value='default_'+self.field+'_value')
                            except Exception:
                                # blocks the column in case if data type incorrectly initialized (all values will be cnhanged to NaN)
                                data[self.field+'_tr'] = numpy.nan
                                data[self.field] = numpy.nan
                    if fields_data[self.group][self.field]['type'] in ['text1', 'text2']:
                        if len(data[self.field].dropna().unique().tolist()) == 0:
                            continue
                        else:
                            try:
                                if data[self.field].dtype != 'object':
                                    data[self.field] = data[self.field].apply(str)
                                data[self.field+'_tr'] = data[self.field].fillna(value='default_'+self.field+'_value').str.lower()
                            except Exception:
                                data[self.field+'_tr'] = numpy.nan
                                data[self.field] = numpy.nan
                    if fields_data[self.group][self.field]['type'] == 'date':
                        if len(data[self.field].dropna().unique().tolist()) == 0:
                            continue
                        else:
                            try:
                                data[self.field+'_tr'] = pandas.to_datetime(data[self.field], dayfirst=True)
                            except Exception:
                                data[self.field+'_tr'] = numpy.nan
                                data[self.field] = numpy.nan
            if set(['Resolved', 'Created']).issubset(set(data.keys())):
                # making "Resolved_td_tr" series based on results from "Resolved_tr" (empty values changed to current date)
                data['Resolved_td_tr'] = data['Resolved_tr'].fillna(value=datetime.date.today())
                # creation of "Time to Resolve" series
                data['ttr'] = (data['Resolved_td_tr']-data['Created_tr']).dt.days
                data['ttr_tr'] = data['ttr'].apply(int) # applies int data type to column
                # appends "ttr" field to "special_fields" list
                fields_data['special_fields']['ttr'] = {'name': 'Time to Resolve (TTR)', 'type': 'number'}
            return data
        except Exception:
            raise

    # lock/unclock MULTIPLE/SINGLE DESCRIPTION MODE
    # reason: to avoid user from incorrect system behavior in case when models or configs have some issues
    # solution: restrict acces to these modules
    def unlock_single_mod(self, hardcode, multiple=False):
        try:
            # getting the models names
            self.config_reader = SettingProvider('single_mod.ini')
            self.areas_inner = self.config_reader.get_fields(section='single_mod', categories='columns', evaluate=False)
            self.config_reader = SettingProvider('attributes.ini')
            self.resolution = self.config_reader.get_fields(section='fields', categories='resolution', evaluate=True)['resolution']
            self.exist = Checker.check_exist_model(self, self.get_resolutions(self.resolution) + hardcode
                                                   + self.areas_inner['columns'].split(','))
            # verifies that models are exist for both modules
            if multiple:
                if self.exist[0]:
                    return False
                else:
                    return True
            else:
                if self.exist[0]:
                    return False
                elif os.path.exists('top_terms.csv'):
                    return True
                else:
                    return False
        except (KeyError, FileNotFoundError, SyntaxError):
            return False

    def check_type_fields(self, fields, types):
        for field in fields:
            if field not in types:
                return False
        return True

    def count_frame_rows(self, frame):
        count = len(frame.index)
        if count < 10:
            return count, 'upload error: dataset has less than 10 defect reports, count is {}'.format(count)
        return count, None
    
    def check_config(self):
        try:
            data = {}
            config_reader = SettingProvider('attributes.ini')
            session['fields'] = config_reader.get_fields(section='fields', categories=['mandatory_fields', 'special_fields'], evaluate=True)
            data['special_fields'] = [{'gui_name': k,
                                      'xml_name': session['fields']['special_fields'][k]['name'],
                                      'type': session['fields']['special_fields'][k]['type']} for k in session['fields']['special_fields']]
            session['ref_to'] = config_reader.get_fields(section='fields', categories='referring_to', evaluate=True)
            data['referring_to'] = session['ref_to']['referring_to']
            # get resolutions for single mode
            # these resolutions are also used for models creation
            session['resolution'] = config_reader.get_fields(section='fields', categories='resolution', evaluate=True)['resolution']
            data['resolution'] = session['resolution']
            # get fields for multiple mode
            session['multiple_mod_fields'] = config_reader.get_setting(section='fields', setting='multiple_mod_fields', evaluate=True)
            data['multiple_mod_fields'] = ','.join(session['multiple_mod_fields'])
            # check that used fields are mandatory fields for multiple mod
            if not Checker.check_type_fields(self, ['Issue_key', 'Summary', 'Priority', 'Description'], session['multiple_mod_fields']):
                return False, 'for multiple mod fields Issue_key, Summary, Priority, Description is mandatory', data

            # checks that we use correct data type in fields
            if not Checker.check_type_fields(self, [session['fields'][el][el1][el2] for el in session['fields'] for el1
                                                in session['fields'][el] for el2 in session['fields'][el][el1] if el2 == 'type'],
                                                ['text', 'text1', 'text2', 'number', 'date', 'categorical', 'bool']):
                return False, 'please use only {} types for fields in attributes.ini file'.format(', '.join(['text', 'text1', 'text2', 'number', 'date', 'categorical', 'bool'])), data

            # checks that resolutions number equals to two
            if not Checker.no_more(self, session['resolution'], 2):
                return False, 'resolution field in attributes.ini must contains only two value', data
            
            # checks that mandatory fields are exist
            if Checker.is_empty(self, session['fields']['mandatory_fields']):
                return False, 'please use mandatiry_fields in attributes.ini', data

            # checks that content for "Referring to" field is exist
            if not Checker.is_subset(self, session['ref_to']['referring_to'], [field for group in session['fields']
                                                                            for field in session['fields'][group]]):
                return False, 'referring_to field must be subset of fields in attributes.ini', data
            
            return True, None, data
        except FileNotFoundError as e:
            return False, str(e), data
        except KeyError as e:
            return False, str(e), data
        except SyntaxError as e:
            return False, str(e), data


if __name__ == '__main__':
    check = Checker()
    print(check.check_exist_model('dsg'))