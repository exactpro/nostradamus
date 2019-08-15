from pathlib import Path
import os
from ldap3 import Server, Connection, SUBTREE, ALL, core
import pandas
import datetime
from werkzeug.utils import secure_filename
from exactpro.config_parser import SettingProvider
from exactpro.exceptions import LDAPError
from exactpro.exceptions import IncorrectValueError, NotExist, NotExistModel, NotExistFile, NotExistField, LDAPError, ModelNotFound, ModelsNotFound
from exactpro.config_parser import get_models_names
from flask import session
import numpy


class Checker:
    def get_resolutions(self, data):
        resolutions = [el for el in data.values() if not isinstance(el, list)]
        for el in [el for el in data.values() if isinstance(el, list)]:
            resolutions += el
        return resolutions

    # checks whether the models are exist
    def check_exist_model(self, model_names):
        if not isinstance(model_names, str):
            for name in model_names:
                name = secure_filename(name) # converting the filename to secure form (example: Won't fix -> Wont_fix)
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
            self.ref_to = [el+' '+el1 for el in ref_to_data['referring_to'] if el != 'Areas of testing' for el1 in data[el].dropna().unique().tolist()]
            if 'Areas of testing' in ref_to_data['referring_to']:
                area_values = SettingProvider('predictions_parameters.ini').get_fields(
                                                section='predictions_parameters', 
                                                categories='areas_of_testing'
                                                )['areas_of_testing']
                self.ref_to = self.ref_to + ['Area of testing'+' '+el1 for el1 in area_values.split(',') if el1 != "Other_lab"]
            self.fields.update({'ReferringTo': ['null'] if not self.ref_to else self.ref_to})
            
            # getting the unique values of categorical type fields from "special_fields" list to place them inside drop-down fields on GUI
            self.fields.update({el: ['null'] if not data[el].dropna().unique().tolist() else data[el].dropna().unique().tolist()
                                for el in list(fields_data['special_fields'].keys())
                                if fields_data['special_fields'][el]['type'] == 'categorical'})
            return self.fields
        else:
            raise Exception('Invalid file.\nPlease check that the file has the following fields:\n{}'.format(
        ', '.join(list(fields_data['mandatory_fields'].keys())+list(fields_data['special_fields'].keys()))))

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


def is_empty(val):
    return not bool(val)


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


def verify_file_exist(file_name, is_check_size = False):
    if is_check_size:
        if not os.path.exists(file_name) or os.path.getsize('top_terms.csv') == 0:
            return False
    else:
        if not os.path.exists(file_name):
            return False
    return True


# verifies whether the models do exist
def verify_models_exist(models):
    if not isinstance(models, str):
        not_found_models = []
        for model in models:
            model = secure_filename(model) # converting the filename to secure form (exmpl: Won't fix -> Wont_fix)
            if not verify_file_exist(str(Path(__file__).parents[2]) + '/model/' + model + '.sav'):
                not_found_models.append(model + '.sav')
        if len(not_found_models) > 0:
            raise ModelsNotFound('Can\'t find the following model(s): {}. Please check whether the models exist'
                                                                        ' and correctness of models names'
                                                                        ' in predictions_parameters.ini'.format(', '.join(not_found_models)))
    else:
        models = secure_filename(models)
        if not verify_file_exist(str(Path(__file__).parents[2]) + '/model/' + models + '.sav'):
            raise ModelNotFound('Can\'t find {}.sav. Please check whether the model exist'
                                                    ' and correctness of model name'
                                                    ' in predictions_parameters.ini'.format(models))


# verifies correctness of parameters names
def verify_required_parameters(required_parameters, config_file, section):
    config_reader = SettingProvider('myconf.ini')
    required_parameters = config_reader.get_setting(section='Path', setting=required_parameters, evaluate=False)
    required_parameters = required_parameters.split(',')
    config_reader = SettingProvider(config_file)
    available_parameters = config_reader.get_parameters(section=section)
    if not is_subset(required_parameters, available_parameters):
        raise KeyError('Configuration error: please check correctness of parameters names in {} file.'.format(config_file))


def verify_defect_attributes_config(defect_attributes):
    mandatory_multiple_mode_fields = ['Issue_key', 'Summary', 'Priority', 'Description']
    allowed_data_types = ['text', 'text1', 'text2', 'number', 'date', 'categorical', 'bool']
    try:
        # verifies that received multiple mode's fields are in mandatory fields list
        if not is_subset(session['multiple_mode_fields'], mandatory_multiple_mode_fields):
            return False, '{} are mandatory for multiple description mode.'.format(', '.join(mandatory_multiple_mode_fields))

        # verifies that mandatory/special fields have correct data types
        if not is_subset([session['defect_attributes'][defect_attribute][attribute_parameters][parameter] 
                                            for defect_attribute in session['defect_attributes'] 
                                            for attribute_parameters in session['defect_attributes'][defect_attribute] 
                                            for parameter in session['defect_attributes'][defect_attribute][attribute_parameters] 
                                            if defect_attribute != 'area_of_testing_fields' and parameter == 'type'],
                        allowed_data_types):
            return False, 'please use only {} types for mandatory and special fields in defect_attributes.ini file.'.format(', '.join(allowed_data_types))

        # verifies that quantity of received resolution's elements isn't greater than specified quantity
        # because it cannot have more than two values in the list
        if not is_greater(session['resolution'], 2):
            return False, 'resolution field cannot have more than two values. please check defect_attributes.ini file.'
        
        # verifies that mandatory fields are filled in defect_attributes.ini
        if is_empty(session['defect_attributes']['mandatory_fields']):
            return False, 'please specify mandatory_fields in defect_attributes.ini'

        # verifies that all received Referring to's fields do exist in mandatory/special fields
        is_area = False
        if 'Areas of testing' in session['ref_to']['referring_to']:
            session['ref_to']['referring_to'].remove('Areas of testing')
            is_area = True
        if not is_subset(session['ref_to']['referring_to'], 
                        [attribute for defect_attributes in session['defect_attributes']
                                    for attribute in session['defect_attributes'][defect_attributes]]):
            if is_area:
                session['ref_to']['referring_to'].append('Areas of testing')
            return False, 'referring_to fields should be presented in mandatory or special fields. please check defect_attributes.ini file.'
        if is_area:
            session['ref_to']['referring_to'].append('Areas of testing')
        return True, None
    except FileNotFoundError as e:
        return False, str(e)
    except KeyError as e:
        return False, str(e)
    except SyntaxError as e:
        return False, str(e)


def verify_predictions_parameters_config():
    try:
        config_exist = verify_file_exist('predictions_parameters.ini')
        if not config_exist:
            return {'single_mode': False, 'multiple_mode': False, 'err_message': ''}
        else:
            verify_required_parameters(
                                    required_parameters='required_predictions_parameters',
                                    config_file='predictions_parameters.ini',
                                    section='predictions_parameters'
                                    )
            verify_models_exist(get_models_names() + ['ttr']) # checking existence of common models
            verify_models_exist(['priority']) # checking model existence required for single description mode only
            if not verify_file_exist('top_terms.csv'): # checking top_terms.csv file existence required for single description mode
                raise FileNotFoundError('Can\'t find top_terms.csv file.')
        return {'single_mode': True, 'multiple_mode': True, 'err_message': ''}
    except ModelsNotFound as err:
        return {'single_mode': False, 'multiple_mode': False, 'err_message': str(err)}
    except ModelNotFound as err:
        return {'single_mode': False, 'multiple_mode': True, 'err_message': str(err)}
    except FileNotFoundError as err:
        return {'single_mode': False, 'multiple_mode': True, 'err_message': str(err)}
    except (KeyError, SyntaxError) as err:
        return {'single_mode': False, 'multiple_mode': False, 'err_message': str(err)}


def verify_classes_amount(classes: list, required_amount=2):
    classes_amount = len(classes)
    if classes_amount < required_amount:
        raise ValueError('Error: the received file doesn\'t contain enough data to analyze. Model can\'t be trained.')


def verify_samples_amount(dataframe, series_name, required_amount=5):
    elements_amount = dataframe[series_name].value_counts().tolist()
    for el in elements_amount:
        if el < required_amount:
            raise ValueError('Error: the received file doesn\'t contain enough data to analyze. Model can\'t be trained.')


if __name__ == '__main__':
    check = Checker()
    print(check.check_exist_model('dsg'))

