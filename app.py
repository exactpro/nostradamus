#!/usr/bin/python3.5

from re import compile
from csv import reader
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from nltk.stem.snowball import SnowballStemmer
import hashlib
import json
from datetime import datetime as dt
import re
import pandas
import logging
import os
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
import csv
from decimal import Decimal
from configparser import ConfigParser


from main.config_processor import load_config_to_session, load_base_config, check_predictions_parameters_config, check_defect_attributes
from main.exceptions import IncorrectValueError, NotExist, NotExistModel, NotExistFile, NotExistField, LDAPError
from main.file_processor import is_file_exist

from main.session import check_session, is_session_expired, remove_folder, create_folder
from main.forms.analysis_and_training import analysis
from main.forms.settings import settings
from main.forms.multiple_mode import multiple_mode
from main.forms.single_mode import single_mode


#   Flask startup
def start_server():
    app.run(debug=False)


app = Flask(
    __name__,
    template_folder='front_end/templates',
    static_folder='front_end/static')
app.register_blueprint(analysis)
app.register_blueprint(settings)
app.register_blueprint(multiple_mode)
app.register_blueprint(single_mode)


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('logout'))


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: (SnowballStemmer("english").stem(w)
                            for w in analyzer(doc))


# user's session preparation
@app.route("/", methods=['POST', 'GET'])
def home():
    page_name = 'loginPage_portable.html'
    try:
        load_base_config()
        load_config_to_session('config.ini')
        if is_file_exist(
                str(Path(__file__).parents[0]) + '/model/' + 'predictions_parameters.ini', check_size=True):
            load_config_to_session(
                str(Path(__file__).parents[0]) + '/model/' + 'predictions_parameters.ini')

        if request.method == 'GET':
            if is_session_expired():
                return render_template(
                    page_name, json=json.dumps({'error': ''}))
            else:
                return render_template(page_name, json=json.dumps(
                    {'error': 'Session expired. Please login again.'}))

        if request.method == 'POST':
            # checks required file's existence
            regular_expressions = str(
                Path(__file__).parents[0]) + '/extensions/' + 'regularExpression.csv'
            config_path = str(Path(__file__).parents[0]) + '/config.ini'
            if not is_file_exist(
                    regular_expressions,
                    config_path,
                    check_size=True):
                raise NotExistFile(
                    'Please check existence of config.ini and regularExpression.csv files.')
            session['is_train'] = False

            session['session_id'] = session.sid[:32]
            session['backup'] = {}
            session['backup']['backup_folder'] = '{0}/backup/{1}/files/'.format(os.path.abspath(os.curdir), session['session_id'])
            session['cache'] = {}
            session['cache'][session['session_id']] = {}

            session['temp_files'] = []  # temp files' paths storage
            session['temp_files'].append(
                    "{cur}/files/{id}".format(cur=os.curdir, id=session['session_id']))

            if not os.path.exists(
                session['backup']['backup_folder']):
                create_folder(session['backup']['backup_folder'])
            app.config['UPLOAD_FOLDER'] = session['backup']['backup_folder']

            session.permanent = False
            session['username'] = 'user'            

            # vectorizer settings creation
            session['tfidf'] = StemmedTfidfVectorizer(
                norm='l2',
                sublinear_tf=True,
                min_df=1,
                stop_words=text.ENGLISH_STOP_WORDS.difference(('see', 'system', 'call')).union(
                    session['config.ini']['MACHINE_LEARNING']['asignee_reporter'],
                    session['config.ini']['MACHINE_LEARNING']['weekdays_stop_words'],
                    session['config.ini']['MACHINE_LEARNING']['months_stop_words'],
                    ['having', 'couldn']),
                analyzer='word')

            session['markup'] = 1 if (
                '1' if session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes'] else '0') == '1' else 0
            session['backup']['source_df'] = ''
            session['backup']['filtered_df'] = ''
            session['backup']['predictions_table'] = ''
            session['new_settings'] = False

            # defect attributes verification
            verification_status, error_message = check_defect_attributes(
                session['config.ini']['DEFECT_ATTRIBUTES'])
            if verification_status:
                return redirect('/analysis_and_training', code=307)
            else:
                return render_template(
                    'setting.html',
                    json=json.dumps(
                        {
                            'error': error_message,
                            'mandatory_attributes': session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes'],
                            'data_types': session['config.ini']['REQUIREMENTS']['allowed_data_types'],
                            'referring_to': session['config.ini']['DEFECT_ATTRIBUTES']['referring_to'],
                            'logging_level': session['config.ini']['DEFECT_ATTRIBUTES']['logging_level'] ,
                            'config_data': session['config.ini']['DEFECT_ATTRIBUTES']}))
    except Exception as e:
        return render_template(page_name, json=json.dumps({'error': str(e)}))


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='0'), code=302)

    remove_folder(session['backup']['backup_folder'])

    page_name = 'loginPage_portable.html'
    session.clear()
    return render_template(page_name)


@app.route('/remove_temp_files', methods=['GET', 'POST'])
def remove_temp_files():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'))
    if request.method == 'POST':
        for path in session['temp_files']:
            if os.path.isfile(path):
                os.remove(path)
        session['temp_files'] = []
        return 'done'
