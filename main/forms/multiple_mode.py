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


from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory, Blueprint
import os
import json
import pandas
import psycopg2
import multiprocessing
import time
from pathlib import Path


from main.session import check_session
from main.data_analysis import transform_series, get_predictions_table
from main.data_converter import unpack_dictionary_val_to_list

from main.file_processor import save_predictions, check_file_extensions, convert_to_dataframe
from main.validation import document_verification
from main.config_processor import check_predictions_parameters_config
from psycopg2.extras import Json

multiple_mode = Blueprint('multiple_mode', __name__)


def calculate_occurrence_percentage(predictions: dict, charts_names):
    """Calculates words' occurrence percentage.

    Parameters:
        predictions (dict): predictions' dictionary;
        charts_names (str or list): charts names.

    Returns:
        occurrence_percentage(dict): occurrence percentage dictionary.
    """

    occurrence_percentage = {key: {} for key in predictions[list(predictions.keys())[0]].keys() if key in charts_names}
    for issue_key in predictions:
        for field in predictions[issue_key]:
            if field in charts_names:
                if isinstance(predictions[issue_key][field], list):
                    for value in predictions[issue_key][field]:
                        if value not in occurrence_percentage[field].keys():
                            occurrence_percentage[field][value] = 1
                        else:
                            occurrence_percentage[field][value] += 1
                else:
                    if predictions[issue_key][field] not in occurrence_percentage[field].keys():
                        occurrence_percentage[field][predictions[issue_key][field]] = 1
                    else:
                        occurrence_percentage[field][predictions[issue_key][field]] += 1
    for field in occurrence_percentage:
        for value in occurrence_percentage[field]:
            occurrence_percentage[field][value] = round((occurrence_percentage[field][value]*100)/len(predictions), 3)
    return occurrence_percentage


@multiple_mode.route('/multiple_mode', methods=['POST', 'GET'])
def multiple_description_mode():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    if request.method == 'POST':

        # predictions_parameters.ini file verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        error_message = predictions_parameters_verification['err_message']

        return render_template(
            'multiplePage.html',
            json=json.dumps(
                {
                    'username': session['username'],
                    'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
                    'message': error_message,
                    'single_mod': signle_mode_status,
                    'multiple_mod': multiple_mode_status}))


@multiple_mode.route('/multiple_mode/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        file = request.files['file']
        return redirect(url_for('home', expired='1'), code=302)
    if request.method == 'POST':
        try:
            # predictions_parameters.ini file verification
            predictions_parameters_verification = check_predictions_parameters_config()
            multiple_mode_status = predictions_parameters_verification['multiple_mode']
            signle_mode_status = predictions_parameters_verification['single_mode']

            file = request.files.getlist("file")

            df = convert_to_dataframe(file)
            session['backup']['predictions_table'] = '{0}/{1}_{2}.pkl'.format(
                session['backup']['backup_folder'], time.strftime('%y%m%d%H%M%S'), 'predictions_table')

            pool = multiprocessing.Pool()
            predictions_table = [
                pool.apply_async(
                    get_predictions_table,
                    args=(
                        df,
                        index,
                        session['predictions_parameters.ini']['predictions_parameters']['areas_of_testing_classes'],
                        unpack_dictionary_val_to_list(
                            session['config.ini']['DEFECT_ATTRIBUTES']['resolution']),
                        session['predictions_parameters.ini']['predictions_parameters'])) for index in list(
                    range(
                        len(
                            df.index)))]

            predictions_table = dict([el.get() for el in predictions_table])

            charts = {}
            charts['area_of_testing'] = {
                _class: 0 for _class in session['predictions_parameters.ini']['predictions_parameters']['areas_of_testing_classes']}
            charts['area_of_testing'].update(
                calculate_occurrence_percentage(
                    predictions_table,
                    'area_of_testing')['area_of_testing'])
            charts['ttr'] = {_class: 0 for _class in session['predictions_parameters.ini']
                             ['predictions_parameters']['ttr_classes']}
            charts['ttr'].update(
                calculate_occurrence_percentage(
                    predictions_table, 'ttr')['ttr'])

            charts['resolution_pie'] = calculate_occurrence_percentage(
                predictions_table, unpack_dictionary_val_to_list(
                    session['config.ini']['DEFECT_ATTRIBUTES']['resolution']))

            for key in predictions_table:
                if isinstance(predictions_table[key]['area_of_testing'], list):
                    predictions_table[key]['area_of_testing'] = ','.join(
                        predictions_table[key]['area_of_testing'])

            pandas.DataFrame.from_dict(
                predictions_table, orient='index').to_pickle(
                session['backup']['predictions_table'])
            df.to_pickle(
                '{0}/{1}_{2}.pkl'.format(
                    session['backup']['backup_folder'],
                    session['frame_store']['frame_multiple'],
                    session['session_id']))
            return render_template(
                'multiplePage.html',
                json=json.dumps(
                    {
                        'username': session['username'],
                        'table': predictions_table,
                        'message': 'file uploaded successfully',
                        'plot': charts,
                        'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status}))

        except Exception as e:
            return render_template('multiplePage.html',
                                   json=json.dumps({'username': session['username'],
                                                    'message': str(e),
                                                    'single_mod': signle_mode_status,
                                                    'multiple_mod': multiple_mode_status}))

@multiple_mode.route('/multiple_mode/save', methods=['GET', 'POST'])
def save_file():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        try:
            # predictions_parameters.ini file verification
            predictions_parameters_verification = check_predictions_parameters_config()
            multiple_mode_status = predictions_parameters_verification['multiple_mode']
            signle_mode_status = predictions_parameters_verification['single_mode']

            file_name = request.form['fileName']
            predictions_table = pandas.read_pickle(
                session['backup']['predictions_table'])
            save_predictions(predictions_table,
                             os.path.join(session['backup']['backup_folder'],
                                          file_name))
            
            session['temp_files'].append(os.path.join(session['backup']['backup_folder'],
                                          file_name))

            return send_from_directory(session['backup']['backup_folder'],
                                       file_name,
                                       as_attachment=True)
        except Exception as e:
            return render_template('multiplePage.html',
                                   json=json.dumps({'username': session['username'],
                                                    'message': str(e),
                                                    'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                                                    'single_mod': signle_mode_status,
                                                    'multiple_mod': multiple_mode_status,
                                                    'is_train': session['is_train']}))