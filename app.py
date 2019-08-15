#!/usr/bin/python3.5

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask import session
from flask_redisSession import RedisSession
from flask_sessionstore import Session
from datetime import timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from nltk.stem.snowball import SnowballStemmer
import hashlib
import json
from datetime import datetime as dt
import re
import logging
from flask import send_from_directory
import os
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
from psycopg2.extras import Json
import psycopg2
import csv
from globals_field import mandatory_fields, data_types, referring_to, requared_files
from decimal import Decimal
from exactpro import file_expire
from exactpro.config_parser import SettingProvider, ConfigCreator, load_defect_attributes
from configparser import ConfigParser
from exactpro.data_checker import Checker, verify_defect_attributes_config, verify_predictions_parameters_config, verify_file_exist
from exactpro.xml_parser import FileSwitcher, clean_description
from exactpro.markup_data import mark_up_area_of_testing, mark_up_other_data
from exactpro.informer import StatInfo
from exactpro.charts import *
from exactpro.filter import Filter
from exactpro.model import Model, Insert, train_model, create_top_terms_file
from exactpro.my_multithread import Multithreaded
from exactpro.file import File, ReduceFrame
from exactpro.exceptions import IncorrectValueError, NotExist, NotExistModel, NotExistFile, NotExistField, LDAPError


# class for saving global information
class GuardianState:
    def __call__(self):
        return self.__dict__


# use this variables to set name of temp frames and link to file_expire module variables
frame_store = GuardianState()
frame_store.orig_frame = 'orig_frame'
frame_store.new_data = 'new_data'
frame_store.tr_frame = 'tr_frame'
frame_store.frame_multiple = 'frame_multiple'

file_expire.tr_frame = frame_store.tr_frame
file_expire.new_data = frame_store.new_data
file_expire.orig_frame = frame_store.orig_frame
file_expire.frame_multiple = frame_store.frame_multiple

# variables for data storing
ldap_store = GuardianState()
db_store = GuardianState()
version_store = GuardianState()
file_info_store = GuardianState()


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: (SnowballStemmer("english").stem(w) for w in analyzer(doc))


#   Flask startup
def start_server():
    app.run(debug=False)


def start_expire(other=None):
    # other is flask process for session shutdown if redis service is not started
    file_expire.start(other=other)


def check_session():
    return 'username' not in session or not hasattr(version_store, 'session_id')


app = Flask(__name__, static_url_path='/static')


@app.errorhandler(413)
def request_entity_too_large(error):
    # predictions_parameters.ini file verification
    predictions_parameters_verification = verify_predictions_parameters_config()
    multiple_mode_status = predictions_parameters_verification['multiple_mode']
    signle_mode_status = predictions_parameters_verification['single_mode']
    
    return render_template('filterPage.html', json=json.dumps({
                                                            'username': session['username'],
                                                            'message': 'File size is bigger than maximum file size,'
                                                            ' maximum size is equal to {} mb'.format(file_info_store.max_file_size/1000**2),
                                                            'fields': session['defect_attributes'],
                                                            'inner': version_store.inner,
                                                            'single_mod': signle_mode_status,
                                                            'multiple_mod': multiple_mode_status,
                                                            'isTrain':session['isTrain']
                                                            })), 413

@app.errorhandler(404)
def page_not_found(e):
    return logout()


@app.route("/", methods=['POST', 'GET'])
def home():
    if version_store.inner == '1':
        page_name = 'loginPage.html'
    else:
        page_name = 'loginPage_portable.html'
    if request.method == 'POST':
        try:
            checker = Checker()
            # check permission for user
            if version_store.inner == '1':
                config_reader = SettingProvider('myconf.ini')
                if not verify_file_exist('top_terms.csv', True):
                    raise NotExistModel('for single mod not exist {} file or is it empty'.format('top_terms.csv'))
                # read ldap settings
                ldap_store.ad_domain_suffix = config_reader.get_setting(section='Path', setting='ad_domain_suffix', evaluate=False)
                ldap_store.ad_server = config_reader.get_setting(section='Path', setting='ad_server', evaluate=False)
                ldap_store.ad_search_tree = config_reader.get_setting(section='Path', setting='ad_search_tree', evaluate=False)
                ldap_store.ad_security_group = config_reader.get_setting(section='Path', setting='ad_security_group', evaluate=False)
                # read DB settings
                db_store.dbname_insert = config_reader.get_setting(section='Path', setting='dbname_insert', evaluate=False)
                db_store.dbname_admin = config_reader.get_setting(section='Path', setting='dbname_admin', evaluate=False)
                db_store.user = config_reader.get_setting(section='Path', setting='user', evaluate=False)
                db_store.password = config_reader.get_setting(section='Path', setting='password', evaluate=False)
                db_store.devHost = config_reader.get_setting(section='Path', setting='devHost', evaluate=False)
                db_store.host_local = config_reader.get_setting(section='Path', setting='host_local', evaluate=False)
                db_store.prodHost = config_reader.get_setting(section='Path', setting='prodHost', evaluate=False)
                db_store.port = config_reader.get_setting(section='Path', setting='port', evaluate=False)
                db_store.connection_parameters_insert_local = {
                    'dbname': db_store.dbname_insert,
                    'user': db_store.user,
                    'password': db_store.password,
                    'host': db_store.host_local
                }
                check = checker.check_user(request.form['username'], request.form['password'], ldap_store)
                if check:
                    session.permanent = True  # set time delta for expired session
                    session['username'] = request.form['username']
                    session['password'] = hashlib.md5(str.encode(request.form['password'])).hexdigest()
                else:
                    raise LDAPError('You have not permission for work with nostradamus')
            else:
                session.permanent = False
                session['username'] = 'user'

            # vectorizer settings declaration
            session['weekdays_sw'] = [
                                    'monday', 'mon', 'tuesday', 'tue', 'wednesday', 'wed', 
                                    'thursday', 'thu', 'friday', 'fri', 'saturday',
                                    'sat', 'sunday', 'sun', 'january', 'jan', 'february',
                                    'feb', 'march', 'mar', 'april', 'may', 'june', 'july',
                                    'august', 'aug', 'september', 'sep', 'octomber', 'oct',
                                    'november', 'nov', 'december', 'dec']
            session['asigneeReporter'] = []
            
            session['tfidf'] = StemmedTfidfVectorizer(
                                        norm='l2',
                                        sublinear_tf=True,
                                        min_df=1,
                                        stop_words=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'], session['weekdays_sw']), 
                                        analyzer='word')
            
            config_reader = SettingProvider('myconf.ini')
            session['description1'] = ''  # save description for single mod
            session['tempFiles'] = []  # store temp files to del them after logout
            version_store.session_id = session.session_id if version_store.inner == '1' else session.sid[:32]

            # check that mandatory config files do exist
            session['requared_files'] = config_reader.get_setting(section='Path', setting='required_files', evaluate=True)
            if set(requared_files).issubset(set(session['requared_files'].keys())):
                for path in session['requared_files'].values():
                    if not os.path.exists(path):
                        raise NotExistFile('please create {} file in nostradamus folder'.format(path))
            else:
                raise IncorrectValueError('please use all required files(regularExpression.csv, '
                                            'defect_attributes.ini, myconf.ini) in config')
            # geting file store settings
            file_info_store.upload_folder = os.path.abspath(os.curdir)+'/files'
            # creating /files folder if this folder doesn't exist
            if not os.path.exists(file_info_store.upload_folder):
                # use os.chmod to grant required permissions
                os.makedirs(file_info_store.upload_folder)
                os.chmod(file_info_store.upload_folder, 0o775)

            
            # getting available file formats from config file
            file_info_store.allowed_extensions = set(config_reader.get_setting(section='Path',
                                                                                setting='allowed_extensions',
                                                                                evaluate=False).split(','))
            try:
                # getting the max file size (bytes)
                file_info_store.max_file_size = float(config_reader.get_setting(section='Path', setting='max_file_size', evaluate=True))*1000**2
            except TypeError as e:
                return render_template(page_name, json=json.dumps({'error': 'incorrect value for max_file_size in myconf.ini',
                                                                   'mandatory_fields': mandatory_fields,
                                                                   'data_types': data_types,
                                                                   'referring_to': referring_to}))
            # log learning process
            try:
                file_info_store.log_train = int(config_reader.get_setting(section='Path', setting='log_train', evaluate=False))
                if file_info_store.log_train not in (0, 1):
                    raise IncorrectValueError('please use for log parameter only 0 or 1 values')
            except ValueError:
                raise ValueError('please use for log parameter only 0 or 1 values')

            # specify location where Flask will store session data
            app.config['UPLOAD_FOLDER'] = file_info_store.upload_folder
            # app.config['MAX_CONTENT_LENGTH'] = file_info_store.max_file_size

            # defect_attributes.ini file verification
            defect_attributes = load_defect_attributes()
            verification_status, error_message = verify_defect_attributes_config(defect_attributes)
            if not verify_file_exist('top_terms.csv', True):
                session['isTrain'] = True
            else: 
                session['isTrain'] = False
            
            # if defect_attributes.ini isn't correct open settings.ini
            if verification_status:
                return redirect('/enterlog', code=307)
            else:
                if version_store.inner == '1':
                    # creating the folder for session files
                    if not os.path.exists(os.path.abspath(os.curdir)+'/files/'+version_store.session_id):
                        os.makedirs('files/'+version_store.session_id)
                return render_template('setting.html', json=json.dumps({'error': 'please setup attributes:\n{}'.format(error_message),
                                                                        'mandatory_fields': mandatory_fields,
                                                                        'data_types': data_types,
                                                                        'referring_to': referring_to,
                                                                        'config_data': defect_attributes}))

        except LDAPError as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except FileNotFoundError as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except KeyError as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except SyntaxError as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except NameError as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except IncorrectValueError as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except ValueError as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except NotExistFile as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
        except NotExistModel as e:
            return render_template(page_name, json=json.dumps({'error': str(e)}))
    else:
        if 'expired' in dict(request.args).keys():
            if request.args['expired'] == '1':
                return render_template(page_name, json=json.dumps({'error': 'Session expired. Please login again.'}))
            else:
                return render_template(page_name, json=json.dumps({'error': ''}))
        else:
            return render_template(page_name, json=json.dumps({'error': ''}))


# files/ folder creation for session's files storing
@app.route('/set_config', methods=['POST', 'GET'])
def set_config():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    try:
        data = request.form.to_dict(flat=False)

        default_area_of_testing = session['orig_settings']["area_of_testing_fields"]

        mondatory_fields = {el['gui_name']: {'name': el['xml_name'], 'type': el['type']} for el
                            in json.loads(data['mandatory_fields'][0])}

        if len(json.loads(data['special_fields'][0])[0]) != 0:
            special_fields = {el['gui_name']: {'name': el['xml_name'], 'type': el['type']} for el 
                            in json.loads(data['special_fields'][0])}
        else:
            special_fields = []
        if len(json.loads(data['area_of_testing_fields'][0])[0]) != 0:
            area_of_testing_fields = {el["gui_name"]: {"gui_name":el["gui_name"], 'name': el['name']} for el 
                                    in json.loads(data['area_of_testing_fields'][0])}
        else:
            area_of_testing_fields = []

        default_areas_difference = [x for x in default_area_of_testing if x not in json.loads(data['area_of_testing_fields'][0])]
        new_areas_difference = [x for x in json.loads(data['area_of_testing_fields'][0]) if x not in default_area_of_testing]
        if (not verify_file_exist('top_terms.csv', True)) and len(area_of_testing_fields) != 0:
            session['isTrain'] = True
        elif len(area_of_testing_fields) == 0:
            session['isTrain'] = False
        elif len(default_areas_difference) == 0 and len(new_areas_difference) == 0 and not session['isTrain']:
            session['isTrain'] = False
        else:
            session['isTrain'] = True

        referring_to_fields = data['referring_to[]']

        if 'Areas of testing' in referring_to_fields and (not verify_file_exist('top_terms.csv', True)):
            return jsonify({
            'error': "Models aren't trained. You can't use Areas of testing element in Referring to field." \
                "\nPlease train models firstly.",
            'mandatory_fields': mandatory_fields,
            'data_types': data_types,
            'referring_to': referring_to
            })

        multiple_mode_fields = data['multiple_mode_fields'][0].split(',')
        
        resolution1value = ''.join(data['resolution1value'])
        resolution1name = ''.join(data['resolution1name'])
        resolution2value = ''.join(data['resolution2value'])
        resolution2name = ''.join(data['resolution2name'])
        resolution_fields = {resolution1name: [resolution1value]}
        if resolution2name in resolution_fields:
            resolution_fields[resolution2name].append(resolution2value)
        else:
            resolution_fields[resolution2name] = resolution2value

        creator = ConfigCreator()
        creator.create_config('{}/defect_attributes.ini'.format(os.curdir), 'defect_attributes')
        
        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'mandatory_fields',
            str(mondatory_fields)
            )
        if len(special_fields) == 0:
            special_fields = {}
        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'special_fields',
            str(special_fields)
            )
        
        if len(area_of_testing_fields) == 0:
            area_of_testing_fields = {}
        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'area_of_testing_fields',
            str(area_of_testing_fields)
            )

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'referring_to',
            str(referring_to_fields)
            )

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'multiple_mode_fields',
            str(multiple_mode_fields)
            )

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'resolution',
            str(resolution_fields)
            )

        checker = Checker()
        
        # defect_attributes.ini file verification
        defect_attributes = load_defect_attributes()
        verification_status, error_message = verify_defect_attributes_config(defect_attributes)

    except KeyError: # appears when any field isn't filled in on GUI
        return jsonify({
            'error': 'Field couldn\'t be empty.\nPlease fill in all required fields.',
            'mandatory_fields': mandatory_fields,
            'data_types': data_types,
            'referring_to': referring_to
            })

    if verification_status:
        if version_store.inner == '1':
            try:
                config_reader = SettingProvider('predictions_parameters.ini')
                session['areas_inner'] = config_reader.get_fields(section='predictions_parameters', categories='areas_of_testing', evaluate=False)
                # checking that models for:  ttr,  priority, areas_inner and resolution do exist
                exist = checker.check_exist_model(['ttr', 'priority']+session['areas_inner']['areas_of_testing'].split(',')
                                                    + checker.get_resolutions(session['resolution']))
                if exist[0]:
                    return jsonify({'error': '{} model do not exist for single mode'.format(exist[1]),
                                    'mandatory_fields': mandatory_fields,
                                    'data_types': data_types,
                                    'referring_to': referring_to})
            except (FileNotFoundError, KeyError, ValueError) as e:
                return jsonify({'error': str(e),
                                'mandatory_fields': mandatory_fields,
                                'data_types': data_types,
                                'referring_to': referring_to})

        return jsonify(dict(redirect=url_for('enterlog'), isTrain = session['isTrain']))
    else:
        return jsonify({'error': 'please setup attributes:\n{}'.format(error_message),
                        'special_fields':special_fields,
                        'area_of_testing_fields':area_of_testing_fields,
                        'mandatory_fields': mandatory_fields,
                        'data_types': data_types,
                        'referring_to': referring_to,
                        'config_data': defect_attributes})


@app.route('/attribute_setting', methods=['POST', 'GET'])
def setting():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)

    #checker = Checker()

    # defect_attributes.ini file verification
    defect_attributes = load_defect_attributes()
    defect_attributes_verification, err_msg_attr_verif = verify_defect_attributes_config(defect_attributes)
    session['orig_settings'] = defect_attributes

    # predictions_parameters.ini file verification
    predictions_parameters_verification = verify_predictions_parameters_config()
    multiple_mode_status = predictions_parameters_verification['multiple_mode']
    signle_mode_status = predictions_parameters_verification['single_mode']
    error_message = predictions_parameters_verification['err_message']

    if defect_attributes_verification:
        return render_template('setting.html', json=json.dumps({'error': error_message,
                                                                'mandatory_fields': mandatory_fields,
                                                                'data_types': data_types,
                                                                'referring_to': referring_to,
                                                                'config_data': defect_attributes,
                                                                'single_mod': signle_mode_status,
                                                                'multiple_mod': multiple_mode_status}))
        
    else:
        return render_template('setting.html', json=json.dumps({'error': err_msg_attr_verif,
                                                                'mandatory_fields': mandatory_fields,
                                                                'data_types': data_types,
                                                                'referring_to': referring_to,
                                                                'config_data': defect_attributes,
                                                                'single_mod': signle_mode_status,
                                                                'multiple_mod': multiple_mode_status}))


@app.route('/enterlog', methods=['POST', 'GET'])
def enterlog():
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)

    # predictions_parameters.ini file verification
    predictions_parameters_verification = verify_predictions_parameters_config()
    multiple_mode_status = predictions_parameters_verification['multiple_mode']
    signle_mode_status = predictions_parameters_verification['single_mode']
    error_message = predictions_parameters_verification['err_message']
    try:
        if version_store.inner == '0':
            session['tempFiles'].append("{cur}/files/{id}".format(cur=os.curdir, id=version_store.session_id))
        if not os.path.exists(os.path.abspath(os.curdir)+'/files/'+version_store.session_id):
            os.makedirs('files/'+version_store.session_id)
            os.chmod('files/'+version_store.session_id, 0o775)
        return render_template('filterPage.html', json=json.dumps({
                                                            'username': session['username'],
                                                            'message': error_message,
                                                            'fields': session['defect_attributes'],
                                                            'inner': version_store.inner,
                                                            'file_size': file_info_store.max_file_size,
                                                            'single_mod': signle_mode_status,
                                                            'multiple_mod': multiple_mode_status,
                                                            'isTrain': session['isTrain']
                                                            }))
    except Exception:
        return render_template('filterPage.html', json=json.dumps({
                                                            'username': session['username'],
                                                            'message': 'System error: something went wrong while rendering Analysis & Training page.',
                                                            'fields': session['defect_attributes'],
                                                            'inner': version_store.inner,
                                                            'file_size': file_info_store.max_file_size,
                                                            'single_mod': signle_mode_status,
                                                            'multiple_mod': multiple_mode_status,
                                                            'isTrain': True
                                                            }))


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='0'), code=302)
    for root, dirs, files in os.walk('files/'+version_store.session_id):
        if files:
            for file_name in files:
                os.chmod('{root}/{file_name}'.format(root=root, file_name=file_name), 0o664)
    shutil.rmtree('files/'+version_store.session_id)
    session.clear()
    if version_store.inner == '1':
        page_name = 'loginPage.html'
    else:
        page_name = 'loginPage_portable.html'
    return render_template(page_name, json=json.dumps({'error': ''}))


# File uploading process
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        file = request.files.getlist("file[]") # if session expired but user have sent any file to back-end 
                                               # the system firstly accepts the file
        return redirect(url_for('home', expired='1'), code=302)

    if request.method == 'POST':
        checker = Checker()
        files = request.files.getlist("file[]") # list of all uploaded files
        
        # reset area fields in case when murkup = 0
        session['defect_attributes']['area_of_testing_fields'] = {}
        
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        error_message = predictions_parameters_verification['err_message']
        if all(files) and checker.allowed_file(files, file_info_store): # allowed_file - checks file format, 
                                                                        # all - checks that all array elements are exist
            defect_attributes = load_defect_attributes()
            session['murkup'] = 0 if version_store.inner == '1' else 1 if ('1' if defect_attributes['area_of_testing_fields'] else '0') == '1' else 0
            session['asigneeReporter'] = []     # stop-words container for Name/Surname values
            session['origFrame'] = 'files/{0}/{1}_{2}.pkl'.format(version_store.session_id, frame_store.orig_frame, version_store.session_id)
            try:
                # creates the list of names of numeric fields from configuration (num_fields_to_convert)
                # for using it in data type conversion process in csv-file processing in Pandas (open_file method)
                manfi_num = list({k: v for k, v in session['defect_attributes']['mandatory_fields'].items() if k
                                                        in [el for group in session['defect_attributes'] for el in session['defect_attributes'][group] if
                                                        group != 'area_of_testing_fields' and session['defect_attributes'][group][el]['type'] == 'number']}.keys())
                spefi_num = list({k: v for k, v in session['defect_attributes']['special_fields'].items() if k
                                                        in [el for group in session['defect_attributes'] for el in session['defect_attributes'][group] if
                                                        group != 'area_of_testing_fields' and session['defect_attributes'][group][el]['type'] == 'number' and not session['defect_attributes'][group][el]['name'] == 'Time to Resolve (TTR)']}.keys())
                num_fields_to_convert = manfi_num + spefi_num
                frames = [] # DataFrames container
                for file in files:
                    file_switcher = FileSwitcher(file_info_store, file, session) # makes class instance for each file
                    # parses and converts values of XML file to Pandas DataFrame
                    frame = file_switcher.open_file(list(session['defect_attributes']['mandatory_fields'].keys()),
                                                    list(session['defect_attributes']['special_fields'].keys()),
                                                    num_fields_to_convert)
                    frames.append(frame)
                # concatenates DataFrames to consolidated table
                data = Filter().reindex_data(pandas.concat(frames)) # reindex_data - makes row reindexing
                                                                    # of concatenated table (otherwise indices will be like '0 1 2 0 1 2 3')
            except Exception as e:
                return render_template('filterPage.html', json=json.dumps({
                                                                        'username': session['username'],
                                                                        'message': str(e),
                                                                        'fields': session['defect_attributes'],
                                                                        'inner': version_store.inner,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'isTrain': True
                                                                        }))
            
            session['frame_count'], session['frame_count_error'] = checker.count_frame_rows(data)  # count of filtered defects
            if session['frame_count_error']:
                return render_template('filterPage.html', json=json.dumps({
                                                                        'username': session['username'], 
                                                                        'message': session['frame_count_error'],
                                                                        'fields': session['defect_attributes'],
                                                                        'inner': version_store.inner,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'isTrain': session['isTrain']
                                                                        }))
            # alternative for pickle from pandas is HDFStore
            # store = pandas.HDFStore(filename+'.h5')
            # store['orig_frame'] = data
            # temp file creaftion
            data.to_pickle(session['origFrame'])

            # save placeholder values for fields of DataFrame
            session['placeholder'] = {k: str(pandas.read_pickle(session['origFrame'])[k].iloc[0])
                                      for k in pandas.read_pickle(session['origFrame']).keys()}

            # markup engine
            if session['murkup'] == 1:
                session['defect_attributes']['area_of_testing_fields']['Other'] = {'type': 'bool', 'name': 'Other'} 
                # areas fields saving to session['defect_attributes'] to use them on GUI and in subset saving process
                session['defect_attributes']['area_of_testing_fields'] = {
                                                                        el.strip()+'_lab': {
                                                                        'gui_name': el.strip(), 
                                                                        'type': 'bool'}
                                                                        for el in session['defect_attributes']['area_of_testing_fields']}
                for pattern in defect_attributes['area_of_testing_fields_for_models']:
                    data = mark_up_area_of_testing(
                                                pandas.read_pickle(session['origFrame']),
                                                'Components',
                                                pattern.strip(''),
                                                '',
                                                defect_attributes['area_of_testing_fields_for_models'][pattern]['name'].strip()
                                                ) 
                    data.to_pickle(session['origFrame']) 
                defect_attributes['area_of_testing_fields_for_models']["Other_lab"] = {"gui_name":"Other","name": 'Other'}
                data = mark_up_other_data(
                                        data,
                                        [el.strip() for el in list(session['defect_attributes']['area_of_testing_fields'].keys()) if el != 'Other_lab']
                                        )
                data.to_pickle(session['origFrame'])
            
            try:
                # drop-down fields preparation
                session['categoricDict'] = checker.prepare_categorical(pandas.read_pickle(session['origFrame']),    
                                                                        fields_data=session['defect_attributes'],
                                                                        ref_to_data=session['ref_to'])
                # paths and file names creation for future temp files storing
                session['newData'] = 'files/{0}/{1}_{2}.pkl'.format(version_store.session_id, frame_store.new_data, version_store.session_id)
                session['trFrame'] = 'files/{0}/{1}_{2}.pkl'.format(version_store.session_id, frame_store.tr_frame, version_store.session_id)

                # data types setting, empty fields blocking, ttr calculation
                data = checker.transform_fields(pandas.read_pickle(session['origFrame']), session['defect_attributes'])
                # reduce = ReduceFrame()
                # data_reduce = reduce.reduce(data)
                data.to_pickle(session['newData']) # filtered DataFrame
                data.to_pickle(session['origFrame']) # initial DataFrame
                data.to_pickle(session['trFrame'])  # transformed DataFrame

                stat_info = StatInfo()
                # STAT INFO calculations
                session['statInfo'] = stat_info.get_statInfo(pandas.read_pickle(session['trFrame']), pandas.read_pickle(session['origFrame']))
                # setting up period for chart calculation in CUMULATIVE CHART OF DEFECT SUBMISSION
                session['period'] = 'W-SUN'
                # THE TOP OF THE MOST FREQUENTLY USED TERMS calculation
                session['origFreqTop'] = stat_info.friquency_stat(pandas.read_pickle(session['trFrame']),
                                                                    sw=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'], session['weekdays_sw']))

            except KeyError as e:
                return render_template('filterPage.html', json=json.dumps({
                                                                        'username': session['username'],
                                                                        'message': str(e),
                                                                        'fields': session['defect_attributes'],
                                                                        'inner': version_store.inner,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'isTrain': True
                                                                        }))
            except Exception as e:
                return render_template('filterPage.html', json=json.dumps({
                                                                        'username': session['username'],
                                                                        'message': str(e),
                                                                        'fields': session['defect_attributes'],
                                                                        'inner': version_store.inner,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'isTrain': True
                                                                        }))

            charts = PlotChart()
            # if cateforical fields are empty then we don't build significance top
            if session['categoricDict']['ReferringTo'] == ['null']:
                session['SignificanceTop'] = 'null'
                session['clearDictionary'] = {'SignificanceTop': session['SignificanceTop'],
                                              'ReferringTo': 'Priority ' + session['categoricDict']['Priority'][0],
                                              'freqTop': session['origFreqTop']}
                # use update for attributes to disable empty ones
                attr = {'SignificanceTop': session['SignificanceTop'], 
                        'ReferringTo': 'Priority '+session['categoricDict']['Priority'][0], 
                        'freqTop': session['origFreqTop']
                        }
                # blocking empty fields on gui
                attr.update({el: None for el in  list(data) if len(data[el].dropna().unique().tolist()) == 0})
                return render_template('filterPage.html', json=json.dumps({
                                                            'username': session['username'],
                                                            'message': 'file uploaded successfully',
                                                            'statInfo': session.get('statInfo'),
                                                            'categoric': session.get('categoricDict'),
                                                            'plot': charts.combine_charts(
                                                                                        charts.prepare_data(
                                                                                                data=pandas.read_pickle(session['trFrame']), 
                                                                                                x='ttr', 
                                                                                                y='Relative Frequency', 
                                                                                                step_size='', 
                                                                                                period=''), 
                                                                                        charts.prepare_data(
                                                                                                data=pandas.read_pickle(session['trFrame']), 
                                                                                                y='Dynamic', 
                                                                                                period=session['period'])),
                                                            'murkup': str(session.get('murkup')),
                                                            'file_size': file_info_store.max_file_size,
                                                            'attributes': attr,
                                                            'fields': session['defect_attributes'],
                                                            'placeholder': session['placeholder'],
                                                            'inner': version_store.inner,
                                                            'single_mod': signle_mode_status,
                                                            'multiple_mod': multiple_mode_status,
                                                            'isTrain': session['isTrain']
                                                            }))
            else:
                try:
                    data_set = session['categoricDict']['ReferringTo'][0]
                    data_splitted = session['categoricDict']['ReferringTo'][0].split()
                    metric = data_splitted[0] + '_' + ' '.join(data_splitted[1:len(data_splitted)])
                    field = session['categoricDict']['ReferringTo'][0].split()[0]
                    
                    session['SignificanceTop'] = {
                        data_set: stat_info.top_terms(
                                                    pandas.read_pickle(session['origFrame']),
                                                    metric,
                                                    field,
                                                    sw=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'], session['weekdays_sw'])
                                                    )}
                except Exception as e:
                    return render_template('filterPage.html', json=json.dumps({
                                                                        'username': session['username'],
                                                                        'message': str(e),
                                                                        'fields': session['defect_attributes'],
                                                                        'inner': version_store.inner,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'isTrain':True
                                                                        }))
                # use update for attributes to disable empty ones
                attr = {'SignificanceTop': session['SignificanceTop'][session['categoricDict']['ReferringTo'][0]],
                        'ReferringTo': 'Resolution '+session['categoricDict']['Resolution'][0], 
                        'freqTop': session['origFreqTop']
                        }
                attr.update({el: None for el in  list(data) if len(data[el].dropna().unique().tolist()) == 0})
                session['clearDictionary'] = {
                                            'SignificanceTop': session['SignificanceTop'][session['categoricDict']['ReferringTo'][0]], 
                                            'ReferringTo': 'Resolution '+session['categoricDict']['Resolution'][0], 
                                            'freqTop': session['origFreqTop']
                                            }
                return render_template('filterPage.html', json=json.dumps({
                                                                    'username': session['username'],
                                                                    'message': 'file uploaded successfully',
                                                                    'statInfo': session.get('statInfo'),
                                                                    'categoric': session.get('categoricDict'),
                                                                    'plot': charts.combine_charts(
                                                                                        charts.prepare_data(
                                                                                                data=pandas.read_pickle(session['trFrame']), 
                                                                                                x='ttr', 
                                                                                                y='Relative Frequency', 
                                                                                                step_size='', 
                                                                                                period=''), 
                                                                                        charts.prepare_data(
                                                                                                data=pandas.read_pickle(session['trFrame']), 
                                                                                                y='Dynamic', 
                                                                                                period=session['period'])),
                                                                    'murkup': str(session.get('murkup')),
                                                                    'file_size': file_info_store.max_file_size,
                                                                    'attributes': attr,
                                                                    'fields': session['defect_attributes'],
                                                                    'placeholder': session['placeholder'],
                                                                    'inner': version_store.inner,
                                                                    'single_mod': signle_mode_status,
                                                                    'multiple_mod': multiple_mode_status,
                                                                    'isTrain': session['isTrain']
                                                                    }))
        else:
            return render_template('filterPage.html', json=json.dumps({
                                                                'username': session['username'],
                                                                'message': 'incorrect file format. Please use only {}'.
                                                                            format(','.join(file_info_store.allowed_extensions)),
                                                                'fields': session['defect_attributes'],
                                                                'inner': version_store.inner,
                                                                'single_mod': signle_mode_status,
                                                                'multiple_mod': multiple_mode_status,
                                                                'isTrain': True
                                                                }))


# CUMULATIVE CHART OF DEFECT SUBMISSION calculation
@app.route('/buildChart/onlyDynamic/', methods=['GET', 'POST'])
def build_onlyDynamic_chart():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        charts = PlotChart()
        checker = Checker()
        session['period'] = charts.parse_period(request.args.get('period', default='W-SUN', type=str))

        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        return jsonify({'username': session['username'],
                        'message': 'chart builded',
                        'statInfo': session['statInfo'],
                        'categoric': session['categoricDict'],
                        'plot': charts.prepare_data(data=pandas.read_pickle(session['newData']), y='Dynamic',
                                                    period=session['period']),
                        'attributes': session['clearDictionary'],
                        'murkup': str(session['murkup']),
                        'fields': session['defect_attributes'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                        })


@app.route('/buildChart/onlyDistribution/', methods=['GET', 'POST'])
def build_onlyDistribution_chart():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        session['scale'] = request.form['scale']
        session['stepSize'] = request.form['stepSize']
        session['x'] = request.form['x']
        session['y'] = request.form['y']
        charts = PlotChart()
        checker = Checker()

        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        error_message = predictions_parameters_verification['err_message']

        if len(pandas.read_pickle(session['newData'])) <= 1 and session['y'] == 'Frequency density':
            return jsonify({'username': session['username'],
                            'message': 'Frequency density chart couldn\'t be created with only one received value.',
                            'statInfo': session['statInfo'],
                            'categoric': session['categoricDict'],
                            'attributes': session['clearDictionary'],
                            'plot': charts.prepare_data(pandas.read_pickle(session['newData']),
                                                        session['x'],
                                                        'Relative Frequency', '', ''),
                            'murkup': str(session['murkup']),
                            'fields': session['defect_attributes'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status
                            })
        try:
            if charts.check_scale_step(session['scale'],
                                       session['stepSize'],
                                       session['x'],
                                       session['statInfo']):
                return jsonify({'username': session['username'],
                                'message': 'chart builded',
                                'statInfo': session['statInfo'],
                                'categoric': session['categoricDict'],
                                'plot': charts.prepare_data(pandas.read_pickle(session['newData']),
                                                                               session['x'],
                                                                               session['y'],
                                                                               session['scale'],
                                                                               session['stepSize']),
                                'attributes': session['clearDictionary'],
                                'murkup': str(session['murkup']),
                                'fields': session['defect_attributes'],
                                'single_mod': signle_mode_status,
                                'multiple_mod': multiple_mode_status
                                })
            else:
                return jsonify({'username': session['username'],
                                'message': 'please use Xmax and StepSize value in the array [0,maxValue from stat info]',
                                'statInfo': session['statInfo'],
                                'categoric': session['categoricDict'],
                                'attributes': session['clearDictionary'],
                                'plot': charts.prepare_data(pandas.read_pickle(session['newData']),
                                                            session['x'],
                                                            session['y'], '', ''),
                                'murkup': str(session['murkup']),
                                'fields': session['defect_attributes'],
                                'single_mod': signle_mode_status,
                                'multiple_mod': multiple_mode_status
                                })
        except ValueError:
            return jsonify({'username': session['username'],
                            'message': 'incorrect value for Xmax or StepSize',
                            'statInfo': session['statInfo'],
                            'categoric': session['categoricDict'],
                            'attributes': session['clearDictionary'],
                            'plot': charts.prepare_data(pandas.read_pickle(session['newData']),
                                                        session['x'],
                                                        session['y'], '', ''),
                            'murkup': str(session['murkup']),
                            'fields': session['defect_attributes'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status
                            })


# ATTRIBUTES LIST FILTRATION filtration
@app.route('/filtering', methods=['GET', 'POST'])
def filter():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        # fields with non-empty values
        session['clearDictionary'] = {k: v[0] if len(v) == 1 else ','.join(v) for k, v in
                                      request.form.to_dict(flat=False).items() if v != ['']}
        session['clearDictionary']['ReferringTo'] = request.args.get('ReferringTo', type=str)
        session['clearDictionary'].update({k: Decimal(v) for k, v in session['clearDictionary'].items() if k[:-1]
                                           in [el for group in session['defect_attributes'] for el in session['defect_attributes'][group] if
                                               session['defect_attributes'][group][el]['type'] == 'number']})
        session['clearDictionary'].update({k: pandas.to_datetime(dt.strptime(v, '%d-%m-%Y')) for k, v in
                                           session['clearDictionary'].items() if k[:-1]
                                           in [el for group in session['defect_attributes'] for el in session['defect_attributes'][group] if
                                               session['defect_attributes'][group][el]['type'] == 'date']})
        session['clearDictionary'].update({k: True if v.lower() == 'yes' else False for k, v in session['clearDictionary'].items() if k
                                           in [el for group in session['defect_attributes'] for el in session['defect_attributes'][group] if
                                               session['defect_attributes'][group][el]['type'] == 'bool']})
        checker = Checker()
        charts = PlotChart()
        stat_info = StatInfo()
        filter = Filter()
        # filtration process
        for key in session['clearDictionary']:
            filter.filtration(key,
                              session['clearDictionary'][key],
                              pandas.read_pickle(session['newData']),
                              fields=session['defect_attributes'],
                              store=session['newData'])
            if pandas.read_pickle(session['newData']).empty:
                filter.drop_filter(session)

                session['categoricDict'] = checker.prepare_categorical(pandas.read_pickle(session['origFrame']),
                                                                       fields_data=session['defect_attributes'],
                                                                       ref_to_data=session['ref_to'])
                
                if session['categoricDict']['ReferringTo'] == ['null']:
                    session['SignificanceTop'] = 'null'
                    session['clearDictionary'].update({'SignificanceTop': session['SignificanceTop'],
                                                       'ReferringTo': 'Priority '+session['categoricDict']['Priority'][0],
                                                       'freqTop': session['origFreqTop']})
                else:
                    session['clearDictionary'].update({
                        'SignificanceTop': session['SignificanceTop'][session['categoricDict']['ReferringTo'][0]],
                        'ReferringTo': 'Priority '+session['categoricDict']['Priority'][0], 'freqTop': session['origFreqTop'],
                        'freqTop': session['origFreqTop']})

                # converts date fields to str format for correct displaying on GUI
                session['clearDictionary'].update({k: str(v.date()) for k, v in session['clearDictionary'].items() if k[:-1] in
                    [field for group in session['defect_attributes'] for field in
                    session['defect_attributes'][group] if session['defect_attributes'][group][field]['type'] == 'date']})
                # converts decimal fields to str format for correct JSON serialisation
                session['clearDictionary'].update({k: str(v) for k, v in session['clearDictionary'].items() if k[:-1] in 
                                           [field for group in session['defect_attributes'] for field in
                                            session['defect_attributes'][group] if session['defect_attributes'][group][field]['type'] == 'number']})

                return jsonify({'username': session['username'],
                                'message': 'there are no rows corresponding to the condition',
                                'statInfo': stat_info.get_statInfo(pandas.read_pickle(session['newData']),
                                                                   pandas.read_pickle(session['origFrame'])),
                                'categoric': session.get('categoricDict'),
                                'attributes': session.get('clearDictionary'),
                                'plot': charts.combine_charts(charts.prepare_data(data=pandas.read_pickle(session['origFrame']),
                                                                                  x='ttr',
                                                                                  y='Relative Frequency',
                                                                                  step_size='',
                                                                                  period=''),
                                                              charts.prepare_data(data=pandas.read_pickle(session['origFrame']),
                                                                                  y='Dynamic',
                                                                                  period='W-SUN')),
                                'murkup': str(session['murkup']),
                                'freqTop': stat_info.friquency_stat(pandas.read_pickle(session['origFrame']),
                                                                    sw=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'],
                                                                                                     session['weekdays_sw'])),
                                'fields': session['defect_attributes'],
                                'single_mod': signle_mode_status,
                                'multiple_mod': multiple_mode_status
                                })

        session['statInfo'] = stat_info.get_statInfo(pandas.read_pickle(session['newData']),
                                                     pandas.read_pickle(session['origFrame']))
        session['categoricDict'] = checker.prepare_categorical(pandas.read_pickle(session['newData']),
                                                               fields_data=session['defect_attributes'],
                                                               ref_to_data=session['ref_to'])
        session['clearDictionary']['freqTop'] = stat_info.friquency_stat(pandas.read_pickle(session['newData']),
                                                                         sw=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'],
                                                                                                          session['weekdays_sw']))
        # creates list of categorical fields for GUI
        session['clearDictionary'].update({k: v.split(',') for k, v in session['clearDictionary'].items() if k in
                                           [field for group in session['defect_attributes'] for field in
                                            session['defect_attributes'][group] if session['defect_attributes'][group][field]['type'] == 'categorical']})
        # converts date fields to str format for correct displaying on GUI
        session['clearDictionary'].update({k: str(v.date()) for k, v in session['clearDictionary'].items() if k[:-1] in
                                           [field for group in session['defect_attributes'] for field in
                                            session['defect_attributes'][group] if session['defect_attributes'][group][field]['type'] == 'date']})
        # convert decimal fields to str format for correct JSON serialisation
        session['clearDictionary'].update({k: str(v) for k, v in session['clearDictionary'].items() if k[:-1] in 
                                           [field for group in session['defect_attributes'] for field in
                                            session['defect_attributes'][group] if session['defect_attributes'][group][field]['type'] == 'number']})
        if session['categoricDict']['ReferringTo'] == ['null']:
            session['clearDictionary']['SignificanceTop'] = 'null'
            return jsonify({'username': session.get('username'),
                            'message': 'data filtered',
                            'statInfo': session.get('statInfo'),
                            'categoric': session.get('categoricDict'),
                            'attributes': session.get('clearDictionary'),
                            'plot': charts.combine_charts(charts.prepare_data(data=pandas.read_pickle(session['newData']),
                                                          x='ttr',
                                                          y='Relative Frequency',
                                                          step_size='',
                                                          period=''),charts.prepare_data(data=pandas.read_pickle(session['newData']),
                                                                                          y='Dynamic',
                                                                                          period='W-SUN')),
                            'murkup': str(session.get('murkup')),
                            'fields': session['defect_attributes'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status
                            })
        else:
            session['clearDictionary']['SignificanceTop'] = stat_info.save_significanceTop(
                                                                            pandas.read_pickle(session['newData']),
                                                                            session['clearDictionary']['ReferringTo'],
                                                                            session['SignificanceTop'],
                                                                            sw=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'], 
                                                                            session['weekdays_sw']))
            return jsonify({'username': session.get('username'),
                            'message': 'data filtered',
                            'statInfo': session.get('statInfo'),
                            'categoric': session.get('categoricDict'),
                            'attributes': session.get('clearDictionary'),
                            'plot': charts.combine_charts(charts.prepare_data(data=pandas.read_pickle(session['newData']),
                                                                              x='ttr',
                                                                              y='Relative Frequency',
                                                                              step_size='',
                                                                              period=''),
                                                          charts.prepare_data(data=pandas.read_pickle(session['newData']),
                                                                              y='Dynamic',
                                                                              period='W-SUN')),
                            'murkup': str(session.get('murkup')),
                            'fields': session['defect_attributes'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status
                            })
            

@app.route('/resetFilter', methods=['GET', 'POST'])
def resetFilter():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        filter = Filter()
        charts = PlotChart()
        stat_info = StatInfo()
        filter.drop_filter(session)
        return jsonify({'username': session['username'],
                        'message': 'filter dropped',
                        'statInfo': stat_info.get_statInfo(pandas.read_pickle(session['newData']),
                                                           pandas.read_pickle(session['origFrame'])),
                        'categoric': session['categoricDict'],
                        'plot': charts.combine_charts(charts.prepare_data(data=pandas.read_pickle(session['origFrame']),
                                                                          x='ttr',
                                                                          y='Relative Frequency',
                                                                          step_size='',
                                                                          period=''),
                                                      charts.prepare_data(data=pandas.read_pickle(session['origFrame']),
                                                                          y='Dynamic',
                                                                          period='W-SUN')),
                        'murkup': str(session['murkup']),
                        'attributes': {'SignificanceTop': session['clearDictionary']['SignificanceTop'], 'ReferringTo': session['categoricDict']['ReferringTo'][0], 'freqTop': session['origFreqTop']},
                        'fields': session['defect_attributes'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                        })


@app.route('/resetSettings', methods=['GET', 'POST'])
def reset_settings():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        default_settings = session['orig_settings']
        data_form = request.form.to_dict(flat=False)

        mandatory_fields_for_file = {el['gui_name']: {'name': el['xml_name'],
                                    'type': el['type']} for el in json.loads(data_form['mandatory_fields'][0])}

        special_fields = {el['gui_name']: {'name': el['xml_name'],
                        'type': el['type']} for el in default_settings['special_fields']}

        area_of_testing_fields = {el['gui_name']: {"gui_name":el['gui_name'],
                                'name': el['name']} for el in default_settings['area_of_testing_fields']}

        referring_to_fields = default_settings['referring_to']

        multiple_mode_fields = default_settings['multiple_mode_fields'].split(',')

        creator = ConfigCreator()
        creator.create_config('{}/defect_attributes.ini'.format(os.curdir),
                              'defect_attributes')

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'mandatory_fields',
            str(mandatory_fields_for_file))

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'special_fields',
            str(special_fields))

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'area_of_testing_fields',
            str(area_of_testing_fields))

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'referring_to',
            str(referring_to_fields))

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'multiple_mode_fields',
            str(multiple_mode_fields))

        creator.update_setting(
            '{}/defect_attributes.ini'.format(os.curdir),
            'defect_attributes',
            'resolution',
            str(default_settings['resolution']))

        checker = Checker()
        return render_template('setting.html', json=json.dumps({'error': '',
                                                            'mandatory_fields': mandatory_fields,
                                                            'special_fields': special_fields,
                                                            'area_of_testing_fields': area_of_testing_fields,
                                                            'data_types': data_types,
                                                            'referring_to': referring_to,
                                                            'config_data': default_settings,
                                                            'single_mod': signle_mode_status,
                                                            'multiple_mod': multiple_mode_status
                                                            }))

@app.route('/saveSubset', methods=['GET', 'POST'])
def saveSubset():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        file = File()
        checker = Checker()
        session['fileName'] = request.form['fileName']
        try:
            file.save_file(pandas.read_pickle(session['newData']),
                           session['fileName'],
                           session['murkup'],
                           file_info_store.upload_folder,
                           session['defect_attributes'])
        except Exception as e:
            return render_template('filterPage.html', json=json.dumps({'username': session['username'],
                                                                       'message': str(e),
                                                                       'fields': session['defect_attributes'],
                                                                       'inner': version_store.inner,
                                                                       'single_mod': signle_mode_status,
                                                                       'multiple_mod': multiple_mode_status,
                                                                       'isTrain': True
                                                                       }))
        # save path to file in order to delete after usage
        session['tempFiles'].append(file_info_store.upload_folder+'/'+session['fileName'])
        return send_from_directory(file_info_store.upload_folder,
                                   session['fileName'],
                                   as_attachment=True)


@app.route('/delTempFiles', methods=['GET', 'POST'])
def delTempFiles():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        for path in session['tempFiles']:
            if os.path.isfile(path):
                os.remove(path)
        session['tempFiles'] = []
        return 'done'


@app.route('/significanceTop', methods=['GET', 'POST'])
def significanceTop():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        stat_info = StatInfo()
        checker = Checker()
        session['ReferringTo'] = request.form['ReferringTo']
        if session['ReferringTo'].split()[0] == 'Area':
            top_terms = pandas.read_csv('top_terms.csv')[session['ReferringTo'].split()[-1]].dropna().tolist()
            return jsonify({'SignificanceTop': top_terms,
                        'fields': session['defect_attributes'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                        })
                
        return jsonify({'SignificanceTop': stat_info.save_significanceTop(
                                                                    pandas.read_pickle(session['newData']),
                                                                    session['ReferringTo'],
                                                                    session['SignificanceTop'],
                                                                    sw=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'],
                                                                                                     session['weekdays_sw'])),
                        'fields': session['defect_attributes'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                        })


# model training
@app.route('/training_model', methods=['GET', 'POST'])
def training_model():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        try:
            # predictions_parameters.ini file verification
            predictions_parameters_verification = verify_predictions_parameters_config()
            multiple_mode_status = predictions_parameters_verification['multiple_mode']
            signle_mode_status = predictions_parameters_verification['single_mode']

            model = Model()
            charts = PlotChart()

            train_model(
                    str(os.path.abspath(os.pardir))+'/model/',
                    session['newData'],
                    list(session['defect_attributes']['area_of_testing_fields'].keys()),
                    session['resolution'],
                    text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'],
                                                  session['weekdays_sw']),
                    log=file_info_store.log_train)
            create_top_terms_file(pandas.read_pickle(session['newData']),
                                                     session['resolution'])
            session['isTrain'] = False
        except ValueError as e: 
            print(e)
            session['isTrain'] = True
            return jsonify({'message': str(e),
                            'username': session['username'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status,
                            'isTrain': session['isTrain']
                            })
        except KeyError as e: 
            print(e)
            session['isTrain'] = True
            return jsonify({'message': 'Error: the received file doesn\'t contain enough data to analyze. Model can\'t be trained.',
                            'username': session['username'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status,
                            'isTrain': session['isTrain']})
        except Exception as e: 
            print(e)
            session['isTrain'] = True
            return jsonify({'message': 'Error: Model can\'t be trained. Please check predictions_parameters.ini file.',
                            'username': session['username'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status,
                            'isTrain': session['isTrain']
                            })
        try:
            checker = Checker()
            stat_info = StatInfo()
            defect_attributes = load_defect_attributes()
            session['categoricDict'] = checker.prepare_categorical(pandas.read_pickle(session['origFrame']),    
                                                                   fields_data=session['defect_attributes'],
                                                                   ref_to_data=session['ref_to'])
            data_set = session['categoricDict']['ReferringTo'][0]
            data_splitted = session['categoricDict']['ReferringTo'][0].split()
            metric = data_splitted[0] + '_' + ' '.join(data_splitted[1:len(data_splitted)])
            field = session['categoricDict']['ReferringTo'][0].split()[0]                          
            session['SignificanceTop'] = {data_set: stat_info.top_terms(
                                                                    pandas.read_pickle(session['origFrame']),
                                                                    metric,
                                                                    field,
                                                                    sw=text.ENGLISH_STOP_WORDS.union(session['asigneeReporter'], 
                                                                                                     session['weekdays_sw']))}
            # use update for attributes to disable empty ones
            attr = {'SignificanceTop': session['SignificanceTop'], 
                    'ReferringTo': 'Priority '+session['categoricDict']['Priority'][0], 
                    'freqTop': session['origFreqTop']}
            # blocking empty fields on gui
            data_frame = pandas.read_pickle(session['origFrame'])
            attr.update({el: None for el in list(data_frame) if len(data_frame[el].dropna().unique().tolist()) == 0})
            return jsonify({
                        'username': session['username'],
                        'message': 'Model has been successfully trained.',
                        'statInfo': session.get('statInfo'),
                        'categoric': session.get('categoricDict'),
                        'plot': charts.combine_charts(
                                            charts.prepare_data(
                                                    data=pandas.read_pickle(session['trFrame']),
                                                    x='ttr',
                                                    y='Relative Frequency',
                                                    step_size='',
                                                    period=''),
                                            charts.prepare_data(
                                                    data=pandas.read_pickle(session['trFrame']),
                                                    y='Dynamic',
                                                    period=session['period'])),
                        'murkup': False,
                        'file_size': file_info_store.max_file_size,
                        'attributes': attr,
                        'fields': session['defect_attributes'],
                        'placeholder': session['placeholder'],
                        'inner': version_store.inner,
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status,
                        'isTrain': session['isTrain']})
        except Exception as e:
            print(e)
            session['isTrain'] = False
            return jsonify({'message': 'Error occured while page rendering. Please try again later.',
                            'username': session['username'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status,
                            'isTrain': session['isTrain']
                            })


@app.route('/singleMod', methods=['POST', 'GET'])
def singleMod():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    checker = Checker()
    try:
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        error_message = predictions_parameters_verification['err_message']

        if (multiple_mode_status and signle_mode_status):
            config_reader = SettingProvider('predictions_parameters.ini')
            prior = config_reader.get_setting(section='predictions_parameters',
                                              setting='priority_classes',
                                              evaluate=False).split(',')
            resol = checker.get_resolutions(session['resolution'])
            areas_of_testing = config_reader.get_setting(section='predictions_parameters',
                                                         setting='areas_of_testing',
                                                         evaluate=False).split(',')
            areas_of_testing = [el for el in areas_of_testing if el != 'Other_lab']
            categoric = {'Priority': prior,
                         'Resolution': resol,
                         'Testing_areas': areas_of_testing}
            return render_template('resultSinglePage.html', json=json.dumps({
                                                                        'username': session['username'],
                                                                        'description1': session['description1'],
                                                                        'categoric': categoric,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'inner': version_store.inner
                                                                        }))
        else:
            return render_template('resultSinglePage.html', json=json.dumps({
                                                                        'username': session['username'],
                                                                        'descr': error_message}))
    except FileNotFoundError as e:
        return render_template('resultSinglePage.html', json=json.dumps({
                                                                    'username': session['username'],
                                                                    'descr': str(e)}))
    except KeyError as e:
        return render_template('resultSinglePage.html', json=json.dumps({
                                                                    'username': session['username'],
                                                                    'descr': str(e)}))

# SINGLE DESCRIPTION MODE: description value processing
@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    try:
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        setting_provader = SettingProvider('predictions_parameters.ini')
        model = Model()
        checker = Checker()
        session['descr'] = request.form['descr']
        if str(session['descr']).isspace():
            raise ValueError
        text_descr = clean_description(session['descr'])
        session['priority_prob'] = model.proc_text(text_descr,
                                                   setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                'priority_classes', False).split(','),
                                                   'priority',
                                                   str(os.path.abspath(os.pardir))+'/model/')

        session['ttr_prob'] = model.proc_text(text_descr,
                                              setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                           'ttr_classes', False).split(','),
                                              'ttr',
                                              str(os.path.abspath(os.pardir))+'/model/')
        session['resolution_pie'] = {}
        for el in checker.get_resolutions(session['resolution']):
            session['resolution_pie'][el] = model.proc_text(text_descr,
                                                            setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                         el+'_classes', False).split(','),
                                                            secure_filename(el),
                                                            str(os.path.abspath(os.pardir))+'/model/')

        session['area_prob'] = {}
        for area in setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                 'areas_of_testing', False).split(','):
            tmp = model.proc_text(text_descr,
                                  setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                               'binary_classes', False).split(','),
                                  secure_filename(area),
                                  str(os.path.abspath(os.pardir))+'/model/')
            # session['area_prob'].update({area.split('_')[0]: float(tmp['1'])})
            session['area_prob'].update({area: float(tmp['1'])})

        session['t'] = tuple(key for key, value in session['area_prob'].items() if value > 0.5)
        session['s'] = ''
        session['recom'] = ''
        for i in range(len(session['t'])):
            session['s'] = session['s'] + session['t'][i]+'    '
        if session['s']=='':
            session['recom'] = "no idea"
        else:
            session['recom'] = session['s']

        session['nastArea'] = {}
        for el in session['area_prob']:
            session['nastArea'][el] = session['area_prob'][el]

        session['nastPrior'] = {}
        for el in session['priority_prob']:
            session['nastPrior'][el] = session['priority_prob'][el]

        return jsonify({'descr': session['descr'],
                        'recom': session['recom'],
                        'prio': session['priority_prob'],
                        'ttr': session['ttr_prob'],
                        'resolution_pie': session['resolution_pie'],
                        'areas': session['area_prob'],
                        'user': session['username'],
                        'inner': version_store.inner,
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                        })
    except ValueError:
                    return jsonify({'username': session['username'],
                                    'error': 'Description can\'t be analyzed. Please check the text.'})
    except KeyError as e:
        return jsonify({'username': session['username'],
                        'error': str(e)})
    except SyntaxError as e:
        return jsonify({'username': session['username'],
                        'error': str(e)})
    except Exception:
        return jsonify({'username': session['username'],
                        'error': 'Please fill in description field.'})


@app.route('/ul_submit', methods=['POST', 'GET'])
def ul_submit():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))

    session['userPrediction'] = {}
    if request.method == 'POST':
        try:
            insert = Insert()
            session['userPrediction']['description'] = request.form['descr']
            session['userPrediction']['label'] = request.form['uslab']
            session['userPrediction']['priority'] = request.form['uspriority']
            session['userPrediction']['username'] = session['username']
            session['nastArea']['description'] = request.form['descr']
            session['nastArea']['critical'] = session['nastPrior']['Critical']
            session['nastArea']['high'] = session['nastPrior']['High']
            session['nastArea']['medium'] = session['nastPrior']['Medium']
            session['nastArea']['low'] = session['nastPrior']['Low']
            session['nastArea']['advice'] = request.form['predlab']
            logger = logging.getLogger("ul_submit")
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler("app.log")
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.info("insert to predictions is started")
            insert.insert_to_predictions(db_store.connection_parameters_insert_local,
                                         '''INSERT INTO {} (date, nastradamusPrediction, userPrediction) VALUES ('{}', {}, {})'''.format('predictions',
                                                                                                                                         datetime.datetime.now(),
                                                                                                                                         Json(session['nastArea']),
                                                                                                                                         Json(session['userPrediction'])))
            logger.info("insert to predictions is finished")
            session['description1'] = ''
            return jsonify({'msg': 'submission is successful'})
        except Exception:
             return jsonify({'username': session['username'],
                             'description1': 'error of inserting data to database'})


@app.route('/highlight_terms', methods=['POST', 'GET'])
def highlight_terms():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        field = ''.join(data['field']).split('=')
        descr = ' '.join(data['descr'])

        with open('regularExpression.csv', 'r') as csv_data:
            for i in [re.compile(el1) for el in csv.reader(csv_data, delimiter=',', quotechar='"') for el1 in el if el1]:
                descr = re.sub(i, ' ', descr)

        terms = []
        # use persentage from single_mod to exclude field with percent less than 1,
        priority_proc = session['priority_prob']
        priority_proc.update({el1: session['resolution_pie'][el][el1] for el in session['resolution_pie']
                              for el1 in session['resolution_pie'][el] if 'not' not in el1})
        priority_proc.update(session['area_prob'])

        if field[1]:
            if priority_proc[field[1]] > 0.05:
                try:
                    tfs = session['tfidf'].fit_transform([descr])
                    top_terms = pandas.read_csv('top_terms.csv')[field[1]].dropna().tolist()
                    for term in session['tfidf'].get_feature_names():
                        if term in top_terms:
                            terms.append(term)
                    return jsonify({'username': session['username'],
                                    'highlight_terms': {'field': {'name': field[0], 'value': field[1]}, 'terms': terms}})
                except FileNotFoundError as e:
                    return jsonify({'username': session['username'],
                                    'error': str(e)})
                except ValueError as e:
                    return jsonify({'username': session['username'],
                                    'error': 'Description can\'t be analyzed. Please check the text.'})
            else:
                return jsonify({'username': session['username'],
                                'highlight_terms': {'field': {'name': field[0], 'value': field[1]}, 'terms': terms}})
        else:
            return jsonify({'username': session['username'],
                            'highlight_terms': {'field': {'name': field[0], 'value': field[1]}, 'terms': terms}})


@app.route('/multipleMod', methods=['POST', 'GET'])
def multipleMod():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        error_message = predictions_parameters_verification['err_message']

        if (multiple_mode_status and signle_mode_status):
            return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                        'file_size': file_info_store.max_file_size,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'inner': version_store.inner}))
        else:
            return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                        'file_size': file_info_store.max_file_size,
                                                                        'message': error_message,
                                                                        'single_mod': signle_mode_status,
                                                                        'multiple_mod': multiple_mode_status,
                                                                        'inner': version_store.inner}))


@app.route('/uploaderMultiple', methods=['POST', 'GET'])
def uploaderMultiple():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        file = request.files['file']
        return redirect(url_for('home', expired='1'), code=302)
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        checker = Checker()
        stat_info = StatInfo()
        chart = MultupleChart()
        file = request.files['file']
        if file and checker.allowed_file1(file.filename, file_info_store):
            try:
                session['asigneeReporter'] = []
                file_switcher = FileSwitcher(file_info_store, file, session)
                data = file_switcher.open_file(mandatory_fields=session['multiple_mode_fields'])
            except Exception as e:
                return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                             'message': str(e),
                                                                             'single_mod': signle_mode_status,
                                                                             'multiple_mod': multiple_mode_status
                                                                             }))

            session['frameMultiple'] = 'files/{0}/{1}_{2}.pkl'.format(version_store.session_id, frame_store.frame_multiple, version_store.session_id)
            # for correct prediction processing fill in NaN values to Description
            data['Description'] = data['Description'].fillna(value='default_value')
            # reduce = ReduceFrame()
            # data_reduce = reduce.reduce(data)
            data.to_pickle(session['frameMultiple'])
            if not checker.document_verification(pandas.read_pickle(session['frameMultiple']),
                                                 session['multiple_mode_fields']):
                return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                             'message': 'document is not valid. Please check that document have following fields:' + '\n' + '\'Issue_key\', \'Project_name\', \'Description\'',
                                                                             'single_mod': signle_mode_status,
                                                                             'multiple_mod': multiple_mode_status}))
            try:
                data = pandas.read_pickle(session['frameMultiple'])
                setting_provader = SettingProvider('predictions_parameters.ini')
                session['newDictionary'] = stat_info.max_data(data,
                                                                setting_provader.get_setting('predictions_parameters.ini'.split('.')[0], 'areas_of_testing', False).split(','),
                                                                checker.get_resolutions(session['resolution']))
                if version_store.inner == '1':
                    insert = Insert()
                    for key in session['newDictionary']:
                        insert.insert_to_predictions(db_store.connection_parameters_insert_local,
                                                        '''INSERT INTO {} (issue_key, nastradamusPrediction) VALUES ('{}', {})'''.format('multiple_predictions',
                                                                                                                                        key,
                                                                                                                                        Json(session['newDictionary'][key])))
            
            except (psycopg2.DatabaseError, KeyboardInterrupt):
                return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                             'message': 'database error',
                                                                             'single_mod': signle_mode_status,
                                                                             'multiple_mod': multiple_mode_status
                                                                             }))
            except FileNotFoundError as e:
                return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                             'message': str(e),
                                                                             'single_mod': signle_mode_status,
                                                                             'multiple_mod': multiple_mode_status
                                                                             }))
            except Exception as e:
                return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                             'message': str(e),
                                                                             'single_mod': signle_mode_status,
                                                                             'multiple_mod': multiple_mode_status
                                                                             }))
            try:
                setting_provader = SettingProvider('predictions_parameters.ini')
                session['multiple_plot'] = {}
                session['multiple_plot']['area_of_testing'] = {el: 0 for el in 
                                                                setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                             'areas_of_testing', False).split(',')}
                session['multiple_plot']['area_of_testing'].update(chart.data_for_multiple_plot(session['newDictionary'],
                                                                                                'area_of_testing')['area_of_testing'])
                session['multiple_plot']['ttr'] = {el: 0 for el in 
                                                    setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                 'ttr_classes', False).split(',')}
                session['multiple_plot']['ttr'].update(chart.data_for_multiple_plot(session['newDictionary'], 'ttr')['ttr'])

                session['multiple_plot']['resolution_pie'] = chart.data_for_multiple_plot(session['newDictionary'],
                                                                            checker.get_resolutions(session['resolution']))
            except FileNotFoundError as e:
                return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                             'message': str(e),
                                                                             'single_mod': signle_mode_status,
                                                                             'multiple_mod': multiple_mode_status}))

            return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                         'table': session['newDictionary'],
                                                                         'message': 'file uploaded successfully',
                                                                         'plot': session['multiple_plot'],
                                                                         'file_size': file_info_store.max_file_size,
                                                                         'single_mod': signle_mode_status,
                                                                         'multiple_mod': multiple_mode_status}))
        return render_template('multiplePage.html', json=json.dumps({'username': session['username'],
                                                                     'message': 'incorrect file format. Please use only xml',
                                                                     'single_mod': signle_mode_status,
                                                                     'multiple_mod': multiple_mode_status}))


@app.route('/save_multiple_subset', methods=['GET', 'POST'])
def save_multiple_subset():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = verify_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        file = File()
        checker = Checker()
        session['fileName'] = request.form['fileName']
        try:
            file.save_multiple_file1(session['newDictionary'],
                                     session['fileName'],
                                     file_info_store.upload_folder)
        except Exception as e:
            return render_template('filterPage.html', json=json.dumps({'username': session['username'],
                                                                       'message': str(e),
                                                                       'fields': session['defect_attributes'],
                                                                       'inner': version_store.inner,
                                                                       'single_mod': signle_mode_status,
                                                                       'multiple_mod': multiple_mode_status,
                                                                       'isTrain': True}))
        # save path to file in order to delete after usage
        session['tempFiles'].append(app.config['UPLOAD_FOLDER']+'/'+session['fileName'])
        return send_from_directory(file_info_store.upload_folder,
                                   session['fileName'],
                                   as_attachment=True)

# application startup
if __name__ == "__main__":
    # session data saved to redis. when we logout redis deletes data from session store but creates it again on login page 
    # session timeout - 30mins
    try:
        config_reader = SettingProvider('myconf.ini')
        version_store.inner = config_reader.get_setting(section='Path',
                                                        setting='inner',
                                                        evaluate=False)
        if int(version_store.inner) not in (0, 1):
            raise IncorrectValueError('Please use only 0 or 1 values for inner parameter in myconf.ini')
        # setting up session
        if int(version_store.inner) == 1: # for company needs only (session stored to redis)
            config = ConfigParser()
            config.read('myconf.ini')
            SESSION_TYPE = 'redis'
            PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # minutes=30 seconds=10
            REDIS_PASSWORD = config['Path']['redis_password']
            app.config['USE_SECRET_KEY'] = False
        else:
            SESSION_TYPE = 'filesystem' # FOR OPENSOURCE NEEDS (session stored to HDD)
            app.config['SECRET_KEY'] = os.urandom(12)
            
        # Flask setting up
        app.config.from_object(__name__)
        RedisSession(app) if int(version_store.inner) == 1 else Session(app)
        Bootstrap(app)

    except (FileNotFoundError, KeyError, SyntaxError, ValueError, IncorrectValueError) as error:
        print(str(error))

    else:
        if int(version_store.inner) == 1:
            parallel = Multithreaded()
            parallel.run_in_parallel(flask=start_server, redis_expire=start_expire)
        else:
            app.run(debug=False)

