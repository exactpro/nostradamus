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

import time
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, Blueprint
from flask import redirect, url_for, render_template, session
import os
import json
import pandas
from sklearn.feature_extraction import text
from decimal import Decimal
from datetime import datetime as dt
from pathlib import Path
from time import strftime

from main.data_analysis import rollback_filter, filter_dataframe, mark_up_series, mark_up_other_data, create_top_terms_file, calculate_significant_terms, transform_series, check_bugs_count, get_statistical_info, get_records_count, get_frequently_terms
from main.validation import is_subset
from main.config_processor import check_predictions_parameters_config, load_config_to_session
from main.file_processor import save_file, convert_to_dataframe, is_file_exist, FileProcessor
from main.training import train_model, is_class_more_than
from main.data_converter import parse_period
from main.charts import add_disrtibution_charts, calculate_coordinates, check_scale_and_step
from main.session import check_session, create_folder
from main.exceptions import InconsistentDataError


analysis = Blueprint('analysis', __name__)


def load_categorical_defect_attributes(dataframe, defect_attributes):
    return {field: ['null'] if not field in dataframe.keys() or not dataframe.get(field).dropna().unique().tolist()
            else dataframe.get(field).dropna().unique().tolist()
            for field in defect_attributes
            if defect_attributes[field]['type'] == 'Categorical'}


def load_categorical_referring_to(dataframe, referring_to_fields):
    referring_to = [field + ' ' + field_value for field in referring_to_fields if field != 'Areas of testing' for field_value in dataframe[field].dropna().unique().tolist() if is_class_more_than(percentage = 0.005, in_series=dataframe[field], _class = field_value) and field_value != 'Unresolved']
    if 'Areas of testing' in referring_to_fields:
        referring_to = referring_to + ['Areas of testing'+ ' ' + area for area in session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes'] if is_class_more_than(percentage = 0.005, in_series = dataframe[area+'_lab'], _class = 1)]
        
    return {'ReferringTo': ['null'] if not referring_to else referring_to}


def get_categorical_fields(dataframe, defect_attributes, referring_to_fields):
    prepared_fields = load_categorical_defect_attributes(dataframe, defect_attributes['mandatory_attributes'])
    prepared_fields.update(load_categorical_referring_to(dataframe, referring_to_fields))
    prepared_fields.update(load_categorical_defect_attributes(dataframe, defect_attributes['special_attributes']))

    return prepared_fields


def get_placeholders(dataframe):
    """ Makes placeholders for GUI fields.

    Parameters:
        dataframe (dataframe): file's data parsed to pandas dataframe.

    Returns:
        dictionary where keys are series names and values are theirs' first non-empty value.
    """
    return {k: str(dataframe[k].iloc[dataframe[k].first_valid_index()])
            for k in dataframe.keys() if len(dataframe[k].dropna().unique().tolist()) > 0}


def get_analysis_data(df, defect_attributes, stop_words):
    """ Prepares data for Analysis & Training page.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame;
        defect_attributes (dict): defect attributes configurations;
        stop_words (list): stop words.

    Returns:
        dictionary containing calculated data.

    """
    processed_data = {}
    processed_data['placeholder'] = get_placeholders(df)
    processed_data['categorical_fields'] = get_categorical_fields(df,
                                                defect_attributes=defect_attributes,
                                                referring_to_fields=defect_attributes['referring_to'])
    processed_data['frequently_terms'] = get_frequently_terms(
        df['Description_tr'])

    processed_data['significant_terms'] = {
        processed_data['categorical_fields']['ReferringTo'][0]: calculate_significant_terms(
            df,
            processed_data['categorical_fields']['ReferringTo'][0],
            sw=text.ENGLISH_STOP_WORDS.union(stop_words))}

    processed_data['gui_attributes'] = {
        'significant_terms': processed_data['significant_terms'][processed_data['categorical_fields']['ReferringTo'][0]],
        'ReferringTo': processed_data['categorical_fields']['ReferringTo'][0],
        'frequently_terms': processed_data['frequently_terms']
    }
    
    processed_data['gui_attributes'].update({el: None for group in ['mandatory_attributes', 'special_attributes'] for el in session['config.ini']['DEFECT_ATTRIBUTES'][group].keys()
                                         if el not in df.columns or not df.get(el).dropna().unique().tolist()})

    processed_data['statistical_info'] = get_statistical_info(df)

    processed_data['charts'] = add_disrtibution_charts(
        calculate_coordinates(
            dataframe=df,
            x='ttr',
            y='Relative Frequency',
            step_size='',
            period=''),
        calculate_coordinates(
            dataframe=df,
            y='Dynamic',
            period='W-SUN'))
    return processed_data


@analysis.route('/analysis_and_training/upload_file', methods=['GET', 'POST'])
def upload_file():
    """ 
        Uploads file from GUI, transforms it to pandas dataframe and saves it as pickle object to HDD.
    """
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if request.method == 'POST':
        try:
            predictions_parameters_verification = check_predictions_parameters_config()
            multiple_mode_status = predictions_parameters_verification['multiple_mode']
            signle_mode_status = predictions_parameters_verification['single_mode']

            uploaded_files = request.files.getlist("file[]")
            df = convert_to_dataframe(uploaded_files)
            if not check_bugs_count(df, 1):
                raise InconsistentDataError(
                    'Oops! Uploaded dataset should has at least one defect.')
            session['backup']['source_df'] = '{0}/{1}_{2}.pkl'.format(
                session['backup']['backup_folder'], strftime('%y%m%d%H%M%S'), 'source_df')
            session['backup']['filtered_df'] = '{0}/{1}_{2}.pkl'.format(
                session['backup']['backup_folder'], strftime('%y%m%d%H%M%S'), 'filtered_df')

            session['config.ini']['MACHINE_LEARNING']['asignee_reporter'] = list(
                {
                    name for full_name in [
                        full_name.lower().split() for full_name in df['Assignee'].tolist() +
                        df['Reporter'].tolist()] for name in full_name})
            
            session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'] = {}
            if session['markup']:
                session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'] = {
                    area.strip(): {
                        'series_name': area.strip() + '_lab',
                        'elements': session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes'][area]['name'].strip(),
                        'gui_name': area.strip()
                    } for area in session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes']
                }
                for area in session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing']:
                    df = mark_up_series(
                        df,
                        session['config.ini']['DEFECT_ATTRIBUTES']['markup_series'],
                        session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'][area]['series_name'],
                        session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'][area]['elements'].lower()
                    )
                df = mark_up_other_data(df, [session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'][area]['series_name']
                                            for area in session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'] if area != 'Other'])
                session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing']['Other'] = {
                    'series_name': 'Other_lab', 'elements': 'Other', 'gui_name': 'Other'}

                df.to_pickle(session['backup']['source_df'])
                df.to_pickle(session['backup']['filtered_df'])

            session['cache'][session['session_id']] = get_analysis_data(df,
                                            session['config.ini']['DEFECT_ATTRIBUTES'],
                                            session['config.ini']['MACHINE_LEARNING']['asignee_reporter'] +
                                            session['config.ini']['MACHINE_LEARNING']['weekdays_stop_words'] +
                                            session['config.ini']['MACHINE_LEARNING']['months_stop_words']
                                                        )
            session['cache'][session['session_id']]['categorical_fields'] = get_categorical_fields(df,
                                                defect_attributes=session['config.ini']['DEFECT_ATTRIBUTES'],
                                                referring_to_fields=session['config.ini']['DEFECT_ATTRIBUTES']['referring_to'])

            session['cache'][session['session_id']]['statistical_info'] = dict(session['cache'][session['session_id']]['statistical_info'],
                **get_records_count(filtered_df=df, source_df=df))

        
            session['filename'] = '\n'.join([str(file.filename) for file in uploaded_files])

            df.to_pickle(session['backup']['source_df'])
            df.to_pickle(session['backup']['filtered_df'])

            session['is_train'] = True if session['markup'] else False
            return render_template('filterPage.html', json=json.dumps({
                'username': session['username'],
                'message': 'file uploaded successfully',
                'statistical_info': session['cache'][session['session_id']]['statistical_info'],
                'categoric': session['cache'][session['session_id']]['categorical_fields'],
                'plot': session['cache'][session['session_id']]['charts'],
                'markup': str(session['markup']),
                'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
                'attributes': session['cache'][session['session_id']]['gui_attributes'],
                'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                'placeholder': session['cache'][session['session_id']]['placeholder'],
                'inner': session['config.ini']['APP']['version'],
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status,
                'is_train': session['is_train']
            }))

        except (InconsistentDataError, Exception) as err_msg:
            # predictions_parameters.ini file verification
            predictions_parameters_verification = check_predictions_parameters_config()
            multiple_mode_status = predictions_parameters_verification['multiple_mode']
            signle_mode_status = predictions_parameters_verification['single_mode']
            return render_template('filterPage.html', json=json.dumps({
                'username': session['username'],
                'message': str(err_msg),
                'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                'inner': session['config.ini']['APP']['version'],
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status,
                'is_train': session['is_train']
            }))


@analysis.route('/analysis_and_training', methods=['POST', 'GET'])
def analysis_and_training():
    if check_session():
        return redirect(url_for('home', expired='1'))
    try:
        # predictions_parameters.ini config verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        error_message = predictions_parameters_verification['err_message']
        if not is_file_exist(session['backup']['source_df']):
            session['is_train'] = False
            return render_template('filterPage.html', json=json.dumps({
                'username': session['username'],
                'message': error_message,
                'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                'inner': session['config.ini']['APP']['version'],
                'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status,
                'is_train': session['is_train']
            }))
        else:
            if session['new_settings']:
                df = pandas.read_pickle(
                    session['backup']['source_df'])
                session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'] = {}
                if session['markup']:
                    session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'] = {
                        area.strip(): {
                            'series_name': area.strip() + '_lab',
                            'elements': session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes'][area]['name'].strip(),
                            'gui_name': area.strip()
                        } for area in session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes']
                    }
                    for area in session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing']:
                        df = mark_up_series(
                            df,
                            session['config.ini']['DEFECT_ATTRIBUTES']['markup_series'],
                            session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'][area]['series_name'],
                            session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'][area]['elements'].lower()
                        )
                    df = mark_up_other_data(df, [session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'][area]['series_name']
                                                for area in session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'] if area != 'Other'])
                    session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing']['Other'] = {
                        'series_name': 'Other_lab', 'elements': 'Other', 'gui_name': 'Other'}
                    df.to_pickle(session['backup']['source_df'])
                    df.to_pickle(session['backup']['filtered_df'])

                session['cache'][session['session_id']] = get_analysis_data(df,
                                            session['config.ini']['DEFECT_ATTRIBUTES'],
                                            session['config.ini']['MACHINE_LEARNING']['asignee_reporter'] +
                                            session['config.ini']['MACHINE_LEARNING']['weekdays_stop_words'] +
                                            session['config.ini']['MACHINE_LEARNING']['months_stop_words']
                                                        )
                session['cache'][session['session_id']]['categorical_fields'] = get_categorical_fields(df,
                                                defect_attributes=session['config.ini']['DEFECT_ATTRIBUTES'],
                                                referring_to_fields=session['config.ini']['DEFECT_ATTRIBUTES']['referring_to'])

                session['cache'][session['session_id']]['statistical_info'] =dict(session['cache'][session['session_id']]['statistical_info'],
                    **get_records_count(filtered_df=df, source_df=df))
                session['config.ini']['DEFECT_ATTRIBUTES']['special_attributes']['ttr'] = {'type': 'Numeric', 'name': 'Time to Resolve (TTR)'}
                session['new_settings'] = False
                session['markup'] = 0 if session['config.ini']['APP']['version'] == 1 else 1 if ('1' if session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes'] else '0') == '1' else 0
                session['is_train'] = True if session['markup'] else False
            return render_template('filterPage.html', json=json.dumps({
                'username': session['username'],
                'message': session['filename'] + '\n' + error_message,
                'statistical_info': session['cache'][session['session_id']]['statistical_info'],
                'categoric': session['cache'][session['session_id']]['categorical_fields'],
                'plot': session['cache'][session['session_id']]['charts'],
                'markup': str(session['markup']),
                'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
                'attributes': session['cache'][session['session_id']]['gui_attributes'],
                'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                'placeholder': session['cache'][session['session_id']]['placeholder'],
                'inner': session['config.ini']['APP']['version'],
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status,
                'is_train': session['is_train']
            }))

    except Exception:
        return render_template('filterPage.html', json=json.dumps({
            'username': session['username'],
            'message': 'Oops! Something went wrong. Please try again later.',
            'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
            'inner': session['config.ini']['APP']['version'],
            'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
            'single_mod': signle_mode_status,
            'multiple_mod': multiple_mode_status,
            'is_train': session['is_train']
        }))


@analysis.route('/analysis_and_training/defect_submission_chart', methods=['GET', 'POST'])
def get_defect_submission_chart():
    """Calculates distribution chart coordinates based on the selected period.

    Returns:
        stringified json-objects containing calculated coordinates.
    """
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'))
    if request.method == 'POST':
        period = parse_period(request.args.get('period', default='W-SUN', type=str))

        # predictions_parameters.ini file verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']
        return jsonify({'username': session['username'],
                        'message': 'chart builded',
                        'statistical_info': session['cache'][session['session_id']]['statistical_info'],
                        'categoric': session['cache'][session['session_id']]['categorical_fields'],
                        'plot': calculate_coordinates(dataframe=pandas.read_pickle(session['backup']['filtered_df']), y='Dynamic',
                                                    period=period),
                        'attributes': session['cache'][session['session_id']]['gui_attributes'],
                        'markup': str(session['markup']),
                        'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                        })

@analysis.route('/analysis_and_training/build_chart/distribution/', methods=['GET', 'POST'])
def get_defect_submission_chart_coordinates():
    """Calculates distribution chart coordinates based on the selected period.

    Returns:
        stringified json-objects containing calculated coordinates.
    """
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'))
    if request.method == 'POST':
        scale = request.form['scale']
        step_size = request.form['stepSize']
        x = request.form['x']
        y = request.form['y']

        # predictions_parameters.ini file verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        if check_scale_and_step(scale,
                                    step_size,
                                    x,
                                    session['cache'][session['session_id']]['statistical_info']):
            return jsonify({'username': session['username'],
                            'message': 'chart builded',
                            'statistical_info': session['cache'][session['session_id']]['statistical_info'],
                            'categoric': session['cache'][session['session_id']]['categorical_fields'],
                            'plot': calculate_coordinates(pandas.read_pickle(session['backup']['filtered_df']),
                                                                            x,
                                                                            y,
                                                                            scale,
                                                                            step_size),
                            'attributes': session['cache'][session['session_id']]['gui_attributes'],
                            'markup': str(session['markup']),
                            'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status
                            })
        else:
            return jsonify({'username': session['username'],
                        'message': 'please use Xmax and StepSize value in the array [0,maxValue from stat info]',
                        'statistical_info': session['cache'][session['session_id']]['statistical_info'],
                        'categoric': session['cache'][session['session_id']]['categorical_fields'],
                        'attributes': session['cache'][session['session_id']]['gui_attributes'],
                        'plot': calculate_coordinates(pandas.read_pickle(session['backup']['filtered_df']),
                                                    x,
                                                    y, '', ''),
                        'markup': str(session['markup']),
                        'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                    })


@analysis.route('/analysis_and_training/filtrate', methods=['GET', 'POST'])
def filtrate():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'))
    if request.method == 'POST':

        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        msg = ''

        filters = {
            k: v[0] if len(v) == 1 else ','.join(v) for k,
            v in request.form.to_dict(
                flat=False).items() if v != ['']}

        source_df = pandas.read_pickle(
                session['backup']['source_df'])

        filtered_df = source_df.to_pickle(session['backup']['filtered_df'])

        for field in filters:
            if not pandas.read_pickle(
                session['backup']['filtered_df']).empty:
                filtered_df = filter_dataframe(
                    field,
                    filters[field],
                    pandas.read_pickle(
                    session['backup']['filtered_df']),
                    defect_attributes=session['config.ini']['DEFECT_ATTRIBUTES'])
                filtered_df.to_pickle(session['backup']['filtered_df'])

        filtered_df = pandas.read_pickle(
                session['backup']['filtered_df'])


        if pandas.read_pickle(
            session['backup']['filtered_df']).empty:
                rollback_filter(session['backup'])
                msg = 'there are no rows corresponding to the condition'
        else:
            session['cache'][session['session_id']] = get_analysis_data(
                                    pandas.read_pickle(
                                    session['backup']['filtered_df']),
                                    session['config.ini']['DEFECT_ATTRIBUTES'],
                                    session['config.ini']['MACHINE_LEARNING']['asignee_reporter'] +
                                    session['config.ini']['MACHINE_LEARNING']['weekdays_stop_words'] +
                                    session['config.ini']['MACHINE_LEARNING']['months_stop_words'])
            session['cache'][session['session_id']]['statistical_info'] = dict(session['cache'][session['session_id']]['statistical_info'],
                                                            **get_records_count(filtered_df=filtered_df, source_df=source_df))
            msg = 'data filtered'

        session['cache'][session['session_id']]['categorical_fields'] = get_categorical_fields(pandas.read_pickle(
            session['backup']['source_df']), session['config.ini']['DEFECT_ATTRIBUTES'], session['config.ini']['DEFECT_ATTRIBUTES']['referring_to'])
        session['cache'][session['session_id']]['categorical_fields']['ReferringTo'] = load_categorical_referring_to(pandas.read_pickle(
            session['backup']['filtered_df']), referring_to_fields=session['config.ini']['DEFECT_ATTRIBUTES']['referring_to'])['ReferringTo']
        session['cache'][session['session_id']]['gui_attributes'].update(filters)
        return jsonify(
            {
                'username': session['username'],
                'message': msg,
                'statistical_info':session['cache'][session['session_id']]['statistical_info'],
                'categoric': session['cache'][session['session_id']]['categorical_fields'],
                'attributes': session['cache'][session['session_id']]['gui_attributes'],
                'plot': session['cache'][session['session_id']]['charts'],
                'markup': str(session['markup']),
                'freqTop': session['cache'][session['session_id']]['frequently_terms'],
                'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status,
                'placeholder':session['cache'][session['session_id']]['placeholder'],
                'is_train': session['is_train']})


@analysis.route('/analysis_and_training/reset_filter', methods=['GET', 'POST'])
def reset_filter():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'))
    if request.method == 'POST':
        # predictions_parameters verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        rollback_filter(session['backup'])

        source_df = pandas.read_pickle(session['backup']['source_df'])

        session['cache'][session['session_id']] = get_analysis_data(source_df,
                                            session['config.ini']['DEFECT_ATTRIBUTES'],
                                            session['config.ini']['MACHINE_LEARNING']['asignee_reporter'] +
                                            session['config.ini']['MACHINE_LEARNING']['weekdays_stop_words'] +
                                            session['config.ini']['MACHINE_LEARNING']['months_stop_words']
                                                        )
        session['cache'][session['session_id']]['categorical_fields'] = get_categorical_fields(source_df,
                                                defect_attributes=session['config.ini']['DEFECT_ATTRIBUTES'],
                                                referring_to_fields=session['config.ini']['DEFECT_ATTRIBUTES']['referring_to'])
        session['cache'][session['session_id']]['statistical_info'] = dict(session['cache'][session['session_id']]['statistical_info'],
            **get_records_count(filtered_df=source_df, source_df=source_df))
        return jsonify(
            {
                'username': session['username'],
                'message': 'filter dropped',
                'statistical_info':session['cache'][session['session_id']]['statistical_info'],
                'categoric': session['cache'][session['session_id']]['categorical_fields'],
                'attributes': session['cache'][session['session_id']]['gui_attributes'],
                'plot': session['cache'][session['session_id']]['charts'],
                'markup': str(
                    session['markup']),
                'attributes': session['cache'][session['session_id']]['gui_attributes'],
                'freqTop': session['cache'][session['session_id']]['frequently_terms'],
                'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status,
                'is_train': session['is_train']})


@analysis.route('/download_subset', methods=['GET', 'POST'])
def download_subset():
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
            save_file(pandas.read_pickle(session['backup']['filtered_df']),
                        session['markup'],
                        session['config.ini']['DEFECT_ATTRIBUTES'], 
                        os.path.join(session['backup']['backup_folder'], file_name))

            session['temp_files'].append(os.path.join(session['backup']['backup_folder'], file_name))
            return send_from_directory(session['backup']['backup_folder'],
                                    file_name,
                                    as_attachment=True)
        except Exception as e:
            return render_template('filterPage.html', json=json.dumps({'username': session['username'],
                                                                       'message': str(e),
                                                                       'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                                                                       'inner': session['config.ini']['APP']['version'],
                                                                       'single_mod': signle_mode_status,
                                                                       'multiple_mod': multiple_mode_status,
                                                                       'is_train': session['is_train']
                                                                       }))


@analysis.route(
    '/analysis_and_training/significant_terms',
    methods=[
        'GET',
        'POST'])
def significant_terms():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        # predictions_parameters.ini file verification
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        referr_to = request.form['ReferringTo']
        significant_terms = {
            referr_to: calculate_significant_terms(
                pandas.read_pickle(
                    session['backup']['filtered_df']),
                referr_to,
                sw=text.ENGLISH_STOP_WORDS.union(
                    session['config.ini']['MACHINE_LEARNING']['asignee_reporter'],
                    session['config.ini']['MACHINE_LEARNING']['weekdays_stop_words'],
                    session['config.ini']['MACHINE_LEARNING']['months_stop_words']))}
        return jsonify({'significant_terms': significant_terms[referr_to],
                        'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                        'single_mod': signle_mode_status,
                        'multiple_mod': multiple_mode_status
                        })


@analysis.route('/analysis_and_training/train', methods=['GET', 'POST'])
def train():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        try:
            source_df = pandas.read_pickle(session['backup']['filtered_df'])
            filtered_df = pandas.read_pickle(session['backup']['filtered_df'])
            train_model(
                str(Path(__file__).parents[2]) + '/model/',
                session['backup']['filtered_df'],
                session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing'],
                session['config.ini']['DEFECT_ATTRIBUTES']['resolution'])
            load_config_to_session(str(
                Path(__file__).parents[2]) +
                '/model/' +
                'predictions_parameters.ini')

            create_top_terms_file(
                filtered_df,
                session['config.ini']['DEFECT_ATTRIBUTES']['resolution'],
                session['predictions_parameters.ini']['predictions_parameters']['priority_classes'],
                session['predictions_parameters.ini']['predictions_parameters']['areas_of_testing_classes'])

            session['cache'][session['session_id']] = get_analysis_data(
                filtered_df,
                session['config.ini']['DEFECT_ATTRIBUTES'],
                session['config.ini']['MACHINE_LEARNING']['asignee_reporter'] +
                session['config.ini']['MACHINE_LEARNING']['weekdays_stop_words'] +
                session['config.ini']['MACHINE_LEARNING']['months_stop_words'])
            
            session['cache'][session['session_id']]['categorical_fields'] = get_categorical_fields(source_df,
                                                defect_attributes=session['config.ini']['DEFECT_ATTRIBUTES'],
                                                referring_to_fields=session['config.ini']['DEFECT_ATTRIBUTES']['referring_to'])

            session['cache'][session['session_id']]['statistical_info'] = dict(session['cache'][session['session_id']]['statistical_info'],
                **get_records_count(filtered_df=filtered_df, source_df=source_df))
                

            # predictions_parameters.ini file verification
            predictions_parameters_verification = check_predictions_parameters_config()
            multiple_mode_status = predictions_parameters_verification['multiple_mode']
            signle_mode_status = predictions_parameters_verification['single_mode']
            
            return jsonify({
                'username': session['username'],
                'message': 'Model has been successfully trained.',
                'statistical_info': session['cache'][session['session_id']]['statistical_info'],
                'categoric': session['cache'][session['session_id']]['categorical_fields'],
                'plot': session['cache'][session['session_id']]['charts'],
                'markup': False,
                'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
                'attributes': session['cache'][session['session_id']]['gui_attributes'],
                'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                'placeholder': session['cache'][session['session_id']]['placeholder'],
                'inner': session['config.ini']['APP']['version'],
                'single_mod': signle_mode_status,
                'multiple_mod': multiple_mode_status,
                'is_train': session['is_train']})

        except Exception as e:
            print(e)
            predictions_parameters_verification = check_predictions_parameters_config()
            multiple_mode_status = predictions_parameters_verification['multiple_mode']
            signle_mode_status = predictions_parameters_verification['single_mode']
            return jsonify({'message': str(e),
                            'username': session['username'],
                            'single_mod': signle_mode_status,
                            'multiple_mod': multiple_mode_status,
                            'is_train': session['is_train'],
                            'categoric': session['cache'][session['session_id']]['categorical_fields'],
                            'file_size': session['config.ini']['REQUIREMENTS']['max_file_size'],
                            'attributes': session['cache'][session['session_id']]['gui_attributes'],
                            'fields': session['config.ini']['DEFECT_ATTRIBUTES'],
                            'placeholder': session['cache'][session['session_id']]['placeholder']
                            })

