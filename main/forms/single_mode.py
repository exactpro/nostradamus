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


import os
import re
import csv
import json
import pandas


from flask import session, request, render_template, request, jsonify, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
import logging
import datetime
from logging import getLogger
from pathlib import Path

from main.config_processor import check_predictions_parameters_config
from main.data_analysis import get_probabilities
from main.cleaner import clean_description
from main.data_converter import unpack_dictionary_val_to_list
from main.session import check_session


single_mode = Blueprint('single_mode', __name__)


@single_mode.route('/single_description_mode', methods=['POST', 'GET'])
def single_description_mode():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    try:
        # predictions_parameters.ini file verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        error_message = predictions_parameters_verification['err_message']

        if (multiple_mode_status and signle_mode_status):
            fields = {}
            fields['Priority'] = session['predictions_parameters.ini']['predictions_parameters']['priority_classes']
            fields['Resolution'] = unpack_dictionary_val_to_list(
                session['config.ini']['DEFECT_ATTRIBUTES']['resolution'])
            fields['Testing_areas'] = [el for el in session['predictions_parameters.ini'][
                'predictions_parameters']['areas_of_testing_classes'] if el != 'Other']

            return render_template('resultSinglePage.html', json=json.dumps({
                'username': session['username'],
                'categoric': fields,
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status
            }))
        else:
            return render_template('resultSinglePage.html', json=json.dumps({
                'username': session['username'],
                'error': error_message}))
    except Exception as e:
        return render_template('resultSinglePage.html', json=json.dumps({
            'username': session['username'],
            'error': str(e)}))


@single_mode.route('/single_description_mode/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    try:
        # predictions_parameters.ini file verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        orig_descr = request.form['descr']
        cleaned_descr = clean_description(
            orig_descr)

        if cleaned_descr.isspace() or cleaned_descr == 'aftercleaning' or cleaned_descr is None:
            raise Exception(
                'Oops! Description can\'t be analyzed. Please check the text.')

        session['probabilities'] = {}

        session['probabilities']['priority'] = get_probabilities(
            cleaned_descr, session['predictions_parameters.ini']['predictions_parameters']['priority_classes'],
            str(Path(__file__).parents[2]) + '/model/' + 'priority')

        session['probabilities']['ttr_probability'] = get_probabilities(
            cleaned_descr, session['predictions_parameters.ini']['predictions_parameters']['ttr_classes'],
            str(Path(__file__).parents[2]) + '/model/' + 'ttr')
        
        session['probabilities']['resolution_probability'] = {
            resolution: get_probabilities(
                cleaned_descr,
                session['predictions_parameters.ini']['predictions_parameters'][resolution.lower() + '_classes'],
                str(Path(__file__).parents[2]) + '/model/' + secure_filename(resolution)) for resolution in unpack_dictionary_val_to_list(
                session['config.ini']['DEFECT_ATTRIBUTES']['resolution'])
        }

        session['probabilities']['areas_of_testing'] = {
            area: get_probabilities(
                cleaned_descr,
                session['predictions_parameters.ini']['predictions_parameters']['binary_classes'],
                str(
                    Path(__file__).parents[2]) +
                '/model/' +
                secure_filename(area))[1] for area in session['predictions_parameters.ini']['predictions_parameters']['areas_of_testing_classes']}

        filtered_areas = [
            key for key,
            value in session['probabilities']['areas_of_testing'].items() if value > 0.5]
        session['probabilities']['recomendation'] = ' '.join(
            [area for area in filtered_areas]) if filtered_areas else 'no idea'

        return jsonify({'descr': orig_descr,
                        'recom': session['probabilities']['recomendation'],
                        'prio': session['probabilities']['priority'],
                        'ttr': session['probabilities']['ttr_probability'],
                        'resolution_pie': session['probabilities']['resolution_probability'],
                        'areas': session['probabilities']['areas_of_testing'],
                        'user': session['username'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status})
    except Exception as err_mssg:
        return jsonify({'username': session['username'],
                        'error': str(err_mssg)})


@single_mode.route(
    '/single_description_mode/highlight',
    methods=[
        'POST',
        'GET'])
def highlight():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        try:
            request_data = request.form.to_dict(flat=False)
            highlighting_field = ''.join(request_data['field']).split('=')
            description = clean_description(
                ' '.join(
                    request_data['descr']))
            probabilities = session['probabilities']['priority']
            probabilities.update({el: session['probabilities']['resolution_probability'][resolution][el] for resolution in session['probabilities'][
                                 'resolution_probability'] for el in session['probabilities']['resolution_probability'][resolution] if 'not' not in el})
            probabilities.update(session['probabilities']['areas_of_testing'])
            highlighting_terms = []
            if highlighting_field[1]:
                top_terms = pandas.read_csv(
                    str(
                        Path(__file__).parents[2]) +
                    '/model/' +
                    'top_terms.csv')[
                    highlighting_field[1]].dropna().tolist()
                if probabilities[highlighting_field[1]] > 0.05:
                    session['tfidf'].fit_transform([description])
                    for term in session['tfidf'].get_feature_names():
                        if term in top_terms:
                            highlighting_terms.append(term)
            return jsonify(
                {
                    'username': session['username'],
                    'highlight_terms': {
                        'field': {
                            'name': highlighting_field[0],
                            'value': highlighting_field[1]},
                        'terms': highlighting_terms}})
        except Exception as e:
            return jsonify(
                {
                    'username': session['username'],
                    'error': 'Description can\'t be analyzed. Please check the text.\n' + str(e)})

