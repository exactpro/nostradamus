'''
*******************************************************************************
* Copyright 2016-2019 Exactpro (Exactpro Systems Limited)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file_ except in compliance with the License.
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


from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Blueprint, send_from_directory, Response
from main.session import check_session
import json
import os
from pathlib import Path
import zipfile
from shutil import copy
from io import BytesIO
import shutil

from main.file_processor import is_file_exist, remove_models, is_file_extensions_zip, delete_set_models
from main.config_processor import check_defect_attributes, check_predictions_parameters_config, Configuration
from main.config_processor import load_config_to_session, update_defect_attributes
from main.data_converter import unpack_dictionary_val_to_list
from main.session import create_folder


settings = Blueprint('settings', __name__)


def get_settings_from_gui(page_data):
    """ Returns parsed defect attributes settings.

    Parameters:
        page_data: dictionary with parsed page's data.

    Returns:
        parsed_settings dictionary: defect attributes settings converted to specific format.

    """
    parsed_settings = {}
    parsed_settings['mandatory_attributes'] = {
        el['xml_name']: {
            'name': el['gui_name'],
            'type': el['type']} for el in json.loads(
            page_data['mandatory_attributes'][0])}

    if json.loads(page_data['special_attributes'][0])[0]:
        parsed_settings['special_attributes'] = {
            el['xml_name']: {
                'name': el['gui_name'],
                'type': el['type']} for el in json.loads(
                page_data['special_attributes'][0])}
    else:
        parsed_settings['special_attributes'] = {}

    if json.loads(page_data['mark_up_attributes'][0])[0]:
        parsed_settings['mark_up_attributes'] = {
            el["gui_name"]: {
                "gui_name": el["gui_name"],
                'name': el['name']} for el in json.loads(
                page_data['mark_up_attributes'][0])}
    else:
        parsed_settings['mark_up_attributes'] = {}

    parsed_settings['referring_to'] = page_data['referring_to[]']

    parsed_settings['logging_level'] = page_data['logging_level']

    parsed_settings['multiple_mode_attributes'] = page_data['multiple_mode_attributes[]']

    resol_pie_chart_val_1 = ''.join(page_data['resolution1value'])
    resol_pie_chart_name_1 = ''.join(page_data['resolution1name'])
    resol_pie_chart_val_2 = ''.join(page_data['resolution2value'])
    resol_pie_chart_name_2 = ''.join(page_data['resolution2name'])
    parsed_settings['resolution'] = {
        resol_pie_chart_name_1: [resol_pie_chart_val_1]}
    if resol_pie_chart_name_2 in parsed_settings['resolution']:
        parsed_settings['resolution'][resol_pie_chart_name_2].append(
            resol_pie_chart_val_2)
    else:
        parsed_settings['resolution'][resol_pie_chart_name_2] = [
            resol_pie_chart_val_2]

    return parsed_settings


@settings.route('/export_models', methods=['POST'])
def export_models():    
    file_name = request.get_data(as_text=True)
    if not os.path.exists(str(Path(__file__).parents[2]) + '/models/archived/' + file_name+'.zip'):
        return Response(status=302)
    return send_from_directory(str(Path(__file__).parents[2]) + '/models/archived/', file_name+'.zip',
                                       as_attachment=True, mimetype="Content-Type: application/zip; charset=utf8")
    

@settings.route('/upload_models', methods=['POST'])
def upload_models():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    
    files = request.files.getlist("file[]")
    is_zip, msg = is_file_extensions_zip(files)
    if not is_zip:
        return jsonify({'error': msg })
    form_data = request.form.to_dict()
    creator = Configuration('{}/config.ini'.format(str(Path(__file__).parents[2])))
    path_selected_models = str(Path(__file__).parents[2]) + r'/models/selected/'
    path_archived_models = str(Path(__file__).parents[2]) + r'/models/archived/'
    if form_data['set_models'] and json.loads(form_data['set_models'])[0].get('name'):
        set_models = {el['name']: el['choose'] for el in json.loads(form_data['set_models'])}

        delete_set_models(form_data, set(session['config.ini']['MACHINE_LEARNING']['set_models'].keys()), set(set_models.keys()))
        if not os.path.exists(path_selected_models):
            create_folder(path_selected_models)
        if not os.path.exists(path_archived_models):
            create_folder(path_archived_models)

        if session['config.ini']['MACHINE_LEARNING']['selected_set_models'] != form_data.get('selected_models'):
            shutil.rmtree(path_selected_models)
            create_folder(path_selected_models)
            if len(files) != 0:
                creator.set_option(
                    'DEFECT_ATTRIBUTES',
                    'mark_up_attributes',
                    str({})
                )
                for file_ in files:
                    if os.path.splitext(file_.filename)[0] == form_data.get('selected_models'):
                        file_.save(os.path.join(path_archived_models, file_.filename))
                        zipfile.ZipFile(os.path.join(path_archived_models, file_.filename), 'r').extractall(path_selected_models)
                        if not os.path.exists(os.path.join(path_selected_models, 'predictions_parameters.ini')):
                            return jsonify({
                                'error': 'Selected set models does not contain "predictions_parameters.ini"',
                                })
                        else:
                            load_config_to_session(os.path.join(path_selected_models, 'predictions_parameters.ini'))
                            mark_up_attributes = {}
                            if session['predictions_parameters.ini']['predictions_parameters'].get('mark_up_attributes'):
                                mark_up_attributes = session['predictions_parameters.ini']['predictions_parameters']['mark_up_attributes']
                            creator.set_option(
                                'DEFECT_ATTRIBUTES',
                                'mark_up_attributes',
                                str(mark_up_attributes)
                            )
                            session['markup'] = 1
                    else:
                        file_.save(os.path.join(path_archived_models, file_.filename))
                            
                    session['config.ini']['MACHINE_LEARNING']['selected_set_models'] = form_data.get('selected_models')
                    
                    creator.set_option(
                        'MACHINE_LEARNING',
                        'selected_set_models',
                        "'"+str(session['config.ini']['MACHINE_LEARNING']['selected_set_models'])+"'"
                    )
            elif form_data.get('selected_models'):
                session['config.ini']['MACHINE_LEARNING']['selected_set_models'] = form_data.get('selected_models')
                    
                creator.set_option(
                    'MACHINE_LEARNING',
                    'selected_set_models',
                    str(session['config.ini']['MACHINE_LEARNING']['selected_set_models'])
                )
                zipfile.ZipFile(path_archived_models + form_data['selected_models']+'.zip', 'r').extractall(path_selected_models)
                if not os.path.exists(path_selected_models + 'predictions_parameters.ini'):
                    return jsonify({
                        'error': 'Selected set models does not contain "predictions_parameters.ini"',
                        })
        else:
            for file_ in files:            
                file_.save(os.path.join(path_archived_models, file_.filename))
        
        creator.set_option(
            'MACHINE_LEARNING',
            'set_models',
            str(set_models)
        )
        creator.set_option(
            'MACHINE_LEARNING',
            'selected_set_models',
            str(form_data.get('selected_models'))
        )
        load_config_to_session('config.ini')
    else: 
        if os.path.exists(str(Path(__file__).parents[2]) + '/models'):
            shutil.rmtree(str(Path(__file__).parents[2]) + '/models')
        creator.set_option(
            'MACHINE_LEARNING',
            'set_models',
            str({})
        )
        creator.set_option(
            'MACHINE_LEARNING',
            'selected_set_models',
            str(None)
        )
    if not form_data.get('selected_models') and not session['markup'] == 1:
        creator.set_option(
            'DEFECT_ATTRIBUTES',
            'mark_up_attributes',
            str({})
        )
            
    if os.path.exists(path_selected_models + 'predictions_parameters.ini'):
        load_config_to_session(path_selected_models + 'predictions_parameters.ini')
        creator.set_option(
            'DEFECT_ATTRIBUTES',
            'mark_up_attributes',
            str(session['predictions_parameters.ini']['predictions_parameters']['mark_up_attributes'])
        )
        session['markup'] = 1
    
    load_config_to_session('config.ini')
    predictions_parameters_verification = check_predictions_parameters_config()
    multiple_mode_status = predictions_parameters_verification['multiple_mode']
    signle_mode_status = predictions_parameters_verification['single_mode']

    return jsonify(dict(redirect=url_for('analysis.analysis_and_training'), 
        single_mod = signle_mode_status, multiple_mod = multiple_mode_status))


@settings.route('/set_config', methods=['POST', 'GET'])
def set_config():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    incoming_defect_attributes = get_settings_from_gui(request.form.to_dict(flat=False))
    try:
        verification_status, error_message = check_defect_attributes(incoming_defect_attributes)
        if verification_status:
            creator = Configuration('{}/config.ini'.format(os.curdir))
            for attribute in incoming_defect_attributes.keys():
                creator.set_option(
                    'DEFECT_ATTRIBUTES',
                    attribute,
                    str(incoming_defect_attributes[attribute])
                )
            load_config_to_session('config.ini')
            session['markup'] = 1 if ('1' if session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes'] else '0') == '1' else 0
            session['new_settings'] = True
            return jsonify({'msg': "ok"})
        else:
            return jsonify({'error': error_message,
                            'special_attributes':incoming_defect_attributes['special_attributes'],
                            'mark_up_attributes':incoming_defect_attributes['mark_up_attributes'],
                            'mandatory_attributes': incoming_defect_attributes['mandatory_attributes'],
                            'data_types': session['config.ini']['REQUIREMENTS']['allowed_data_types'],
                            'referring_to': incoming_defect_attributes['referring_to'],
                            'logging_level': 'INFO',
                            'config_data': incoming_defect_attributes})

    except KeyError as e:
        print(e)
        return jsonify({
            'error': 'Field couldn\'t be empty.\nPlease fill in all required fields.',
            'mandatory_attributes': incoming_defect_attributes['mandatory_attributes'],
            'data_types': session['config.ini']['REQUIREMENTS']['allowed_data_types'],
            'referring_to': incoming_defect_attributes['referring_to'],
            'logging_level': 'INFO'
            })
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Something went wrong.\nPlease try again later.',
            'mandatory_attributes': incoming_defect_attributes['mandatory_attributes'],
            'data_types': session['config.ini']['REQUIREMENTS']['allowed_data_types'],
            'referring_to': incoming_defect_attributes['referring_to'],
            'logging_level': 'INFO'
            })


@settings.route('/setting', methods=['POST', 'GET'])
def setting():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return redirect(url_for('home', expired='1'), code=302)
    
    # config.ini file_ verification
    defect_attributes_verification, err_msg_attr_verif = check_defect_attributes(session['config.ini']['DEFECT_ATTRIBUTES'])

    # predictions_parameters.ini file_ verification
    predictions_parameters_verification = check_predictions_parameters_config()
    multiple_mode_status = predictions_parameters_verification['multiple_mode']
    signle_mode_status = predictions_parameters_verification['single_mode']
    error_message = predictions_parameters_verification['err_message']
    if defect_attributes_verification:
        return render_template('setting.html', json=json.dumps({'error': error_message,
                                                                'mandatory_attributes': session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes'],
                                                                'data_types': session['config.ini']['REQUIREMENTS']['allowed_data_types'],
                                                                'referring_to': ['Resolution', 'Priority', 'Areas of testing'],
                                                                'logging_level': ['INFO', 'ERROR', 'DO NOT LOG'],
                                                                'config_data': session['config.ini']['DEFECT_ATTRIBUTES'],
                                                                'single_mod': signle_mode_status,
                                                                'multiple_mod': multiple_mode_status,
                                                                'set_models': session['config.ini']['MACHINE_LEARNING']['set_models']}))
        
    else:
        return render_template('setting.html', json=json.dumps({'error': err_msg_attr_verif,
                                                                'mandatory_attributes': session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes'],
                                                                'data_types': session['config.ini']['REQUIREMENTS']['allowed_data_types'],
                                                                'referring_to': ['Resolution', 'Priority', 'Areas of testing'],
                                                                'logging_level': ['INFO', 'ERROR', 'DO NOT LOG'],
                                                                'config_data': session['config.ini']['DEFECT_ATTRIBUTES'],
                                                                'single_mod': signle_mode_status,
                                                                'multiple_mod': multiple_mode_status,
                                                                'set_models': session['config.ini']['MACHINE_LEARNING']['set_models']}))
    
@settings.route('/reset_settings', methods=['GET', 'POST'])
def reset_settings():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('home', expired='0'), code=302)
    if check_session():
        return jsonify(dict(redirect=url_for('home', expired='1')))
    if request.method == 'POST':
        predictions_parameters_verification = check_predictions_parameters_config()
        multiple_mode_status = predictions_parameters_verification['multiple_mode']
        signle_mode_status = predictions_parameters_verification['single_mode']

        update_defect_attributes()

        load_config_to_session(str(
                    Path(__file__).parents[2]) +
                'config.ini')
        return render_template('setting.html', json=json.dumps({'error': '',
                                                            'mandatory_attributes': session['config.ini']['DEFECT_ATTRIBUTES']['mandatory_attributes'],
                                                            'special_attributes': session['config.ini']['DEFECT_ATTRIBUTES']['special_attributes'],
                                                            'mark_up_attributes': session['config.ini']['DEFECT_ATTRIBUTES']['mark_up_attributes'],
                                                            'data_types': session['config.ini']['REQUIREMENTS']['allowed_data_types'],
                                                            'referring_to': ['Resolution', 'Priority', 'Areas of testing'],
                                                            'logging_level': ['INFO', 'ERROR', 'DO NOT LOG'],
                                                            'config_data': session['config.ini']['DEFECT_ATTRIBUTES'],
                                                            'single_mod': signle_mode_status,
                                                            'multiple_mod': multiple_mode_status
                                                            }))
