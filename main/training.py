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

from main.file_processor import is_file_exist, remove_models
from main.exceptions import ModelNotFound, ModelsNotFound
from main.validation import is_zero
from main.data_converter import unpack_dictionary_val_to_list
from main.data_analysis import reindex_dataframe, check_bugs_count
from main.logger import log_train, log

import pandas
from werkzeug.utils import secure_filename
from os.path import exists
from os import makedirs
import os
from pathlib import Path
from sklearn import feature_selection
from sklearn.feature_selection import SelectKBest
from imblearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.feature_extraction import text
from pickle import dump
from pandas import read_pickle, Categorical, qcut, get_dummies
from flask import session
from pathlib import Path
from zipfile import ZipFile


def get_models_names():
    """ Generates a list of model names.

        Returns:
            models(list): List of model names.
    """
    areas_of_testing = session['predictions_parameters.ini']['predictions_parameters']['areas_of_testing_classes']
    resolution = unpack_dictionary_val_to_list(session['config.ini']['DEFECT_ATTRIBUTES']['resolution'])
    models = [model for container in [areas_of_testing, resolution]
            for model in container]
    return models


def are_models_exist(models):
    """ Checks whether the handled models are exist.

        Parameters:
            models(list): List of models' names.

    """
    not_found_models = []
    for model in models:
        model = secure_filename(model)
        if not is_file_exist(
                str(Path(__file__).parents[1]) + '/models/selected/' + model + '.sav'):
            not_found_models.append(model + '.sav')
    if len(not_found_models) > 0:
        raise ModelsNotFound(
            'Oops! Can\'t find the following model(s): {}. Please check whether the models exist'
            ' and correctness of models names'
            ' in predictions_parameters.ini'.format(
                ', '.join(not_found_models)))

def check_resolutions(df, resolutions):
    """ Checks whether the all specified resolutions are presented in handled DataFrame.

        Parameters:
            df (DataFrame): defect reports' file parsed to pandas DataFrame;
            resolutions(list): list of resolutions names.

        Returns:
            Dictionary representing checking status and error message.

    """

    missed_resolutions = []
    for resol in resolutions:
        if 'Resolution_' + resol not in df.columns:
            missed_resolutions.append(resol)
    if missed_resolutions:
        return {
            'status': False,
            'msg': 'Oops! These Resolution elements are missed: {}. Models can\'t be trained.'.format(
                ', '.join(missed_resolutions))}
    return {'status': True, 'msg': ''}


def check_classes_count(classes: list, required_count=2):
    """ Checks whether the classes count fits to required count.

        Parameters:
            classes(list): classes' list;
            required_count(int): required count of classes.

    """
    if len(classes) < required_count:
        raise ValueError(
            'Oops! Too little data to analyze. Model can\'t be trained.')


@log_train
def training_imbalance(
        descr_series,
        classes_codes,
        TFIDF_,
        IMB_,
        FS_,
        req_percentage,
        CLF_,
        model_path):
    """ Trains models using handled setting and saves them as .sav objects.

        Parameters:
            descr_series(Series): description series;
            classes_codes(Series): series with classes' codes;
            TFIDF_: vectorizer;
            IMB_: SMOTE method;
            FS_: ranking terms method;
            req_percentage(int): percentage to be taken from the ranked list;
            CLF_: classifier;
            model_path(str): the path to the model.

    """
    transformer = feature_selection.SelectPercentile(FS_)
    clf_model = Pipeline([('tfidf', TFIDF_), ('imba', IMB_),
                          ('fs', transformer), ('clf', CLF_)])
    clf_model.set_params(
        fs__percentile=req_percentage).fit(
        descr_series,
        classes_codes)
    dump(clf_model, open(model_path + '.sav', 'wb'))


def is_class_more_than(percentage, in_series, _class):
    """ Checks whether the _class members amount represents required percentage in handled series.

        Parameters:
            percentage(float): required percentage;
            in_series(Series): DataFrame series;
            _class: searching value.

        Returns:
            Boolean value.

    """
    return in_series[in_series == _class].size / in_series.size >= percentage


def stringify_ttr_intervals(intervals):
    """ Stringifies list of ttr intervals.

        Parameters:
            intervals(list): intervals.

        Returns:
            Stringified list of intervals.

    """
    return str([str(intervals[0].left if intervals[0].left > 0 else 0) +
                '-' +
                str(intervals[0].right)] +
               [str(intervals[el].left +
                    1.0) +
                '-' +
                str(intervals[el].right) for el in range(1, 3)] +
               ['>' +
                str(intervals[2].right)])


def prepare_df(
        df, areas_of_testing, resolution):
    """ Filters and encodes series data from handled DataFrame.

        Parameters:
            df(DataFrame): defect reports' file parsed to pandas DataFrame;
            areas_of_testing(list): areas of testing;
            resolution(dict): resolution.

        Returns:
            filtered_classes(dict): valid classes;
            dataframes(dict): encoded data.

    """
    filtered_classes = {}
    dataframes = {}

    filtered_classes['areas_of_testing_classes'] = [
        area for area in areas_of_testing if is_class_more_than(percentage = 0.01, in_series = df[areas_of_testing[area]['series_name']], _class = 1)]

    filtered_classes['priority_classes'] = sorted(
        [
            el for el in df['Priority'].unique().tolist() if is_class_more_than(
                percentage = 0.01, in_series = df['Priority'], _class = el)])

    dataframes['priority_df'] = df[df['Priority'].isin(
        filtered_classes['priority_classes'])]

    dataframes['priority_df'] = reindex_dataframe(
        dataframes['priority_df'])
    dataframes['priority_df']['Priority_codes'] = Categorical(
        dataframes['priority_df']['Priority'], ordered=True).codes

    filtered_classes['ttr_classes'] = qcut(
        df['ttr'].astype(int),
        4,
        duplicates='drop')

    df['coded_ttr_intervals'] = filtered_classes['ttr_classes'].cat.rename_categories(
        range(
            0,
            4))
    filtered_classes['ttr_classes'] = list(
        filtered_classes['ttr_classes'].unique().categories)

    valid_ttr_code_classes = [el for el in df['coded_ttr_intervals'].unique(
    ).tolist() if is_class_more_than(percentage = 0.01, in_series = df['coded_ttr_intervals'], _class = el)]

    dataframes['ttr_df'] = df[df['coded_ttr_intervals'].isin(
        valid_ttr_code_classes) & (df['Resolution'] != 'Unresolved') & (df['Resolved'].isna() != True)]
    
    dataframes['ttr_df'] = reindex_dataframe(
        dataframes['ttr_df'])

    dataframes['resolution_df'] = df[(df['Resolution'] != 'Unresolved') & (df['Resolved'].isna() != True)]
    dataframes['resolution_df'] = get_dummies(
        dataframes['resolution_df'], prefix=list(
            resolution.keys()), columns=list(
            resolution.keys()))
    dataframes['resolution_df'] = reindex_dataframe(
        dataframes['resolution_df'])

    unfiltered_resolutions = unpack_dictionary_val_to_list(resolution)

    filtered_classes['resolutions_classes'] = []
    
    valid_resolutions = check_resolutions(dataframes['resolution_df'], unfiltered_resolutions)

    if valid_resolutions['status']:
        for resol in unfiltered_resolutions:
            if is_class_more_than(percentage = 0.01, in_series = dataframes['resolution_df']['Resolution_' + resol], _class = 1):
                filtered_classes['resolutions_classes'].append(resol)
    else:
        raise ValueError(valid_resolutions['msg'])

    filtered_classes['binary_classes'] = [0, 1]
    filtered_classes['ttr_classes'] = stringify_ttr_intervals(
        filtered_classes['ttr_classes'])

    return filtered_classes, dataframes


def write_classes(filtered_classes):
    """ Writes handled classes to prediction_parameters.ini.

        Parameters:
            filtered_classes(dict): classes.
    """
    from main.config_processor import Configuration
    config = Configuration(
        str(Path(__file__).parents[1]) + '/models/selected/' + 'predictions_parameters.ini')
    # config file creation
    config.create_config('predictions_parameters')

    for _class in filtered_classes:
        if _class == 'resolutions_classes':
            for resolution in filtered_classes[_class]:
                config.set_option(
                    'predictions_parameters', resolution + '_classes', str(['not ' + resolution, resolution]))
        else:
            config.set_option(
                'predictions_parameters', _class, str(
                    filtered_classes[_class]))


@log
def get_k_neighbors(series):
    classes = series.unique().tolist()
    min_count = len(series[lambda x: x == classes[0]])
    count_samples = []
    for _class in classes:
        count_sample = len(series[lambda x: x == _class])
        count_samples.append(count_sample)
        if count_sample < min_count:
            min_count = count_sample
    k_neighbors = int(min_count / 2)
    if len(set(count_samples)) == 1:
        return 2
    if k_neighbors <= 1:
        raise ValueError(
            'Oops! Too small number of class representatives for {}'.format(series.name))
    return k_neighbors


def train_model(
        model_path,
        dataframe_path,
        areas_of_testing,
        resolution):
    if not exists(model_path):
        makedirs(model_path)
    df = read_pickle(dataframe_path)

    if not check_bugs_count(df, 100):
        raise ValueError(
            'Oops! Too little data to analyze. Model can\'t be trained.')

    filtered_classes, dataframes = prepare_df(
        df, areas_of_testing, resolution)

    for _class in filtered_classes:
        check_classes_count(filtered_classes[_class])

    # model/ folder cleanup
    remove_models()

    # updated predictions parameters writing
    write_classes(filtered_classes)

    from main.config_processor import load_config_to_session
    load_config_to_session(str(Path(__file__).parents[1]) + '/models/selected/' + 'predictions_parameters.ini')

    smt = SMOTE(
        ratio='minority',
        random_state=0,
        kind='borderline1',
        n_jobs=4)
    svm_imb = SVC(gamma=2, C=1, probability=True, class_weight='balanced')
    chi2 = feature_selection.chi2
    # areas of testing models training
    for area in filtered_classes['areas_of_testing_classes']:
        smt.k_neighbors = get_k_neighbors(df[areas_of_testing[area]['series_name']])
        training_imbalance(
            df['Description_tr'],
            df[areas_of_testing[area]['series_name']],
            session['tfidf'],
            smt,
            chi2,
            50,
            svm_imb,
            model_path + secure_filename(area))
    # priority models training
    smt.k_neighbors = get_k_neighbors(dataframes['priority_df']['Priority_codes'])
    training_imbalance(
        dataframes['priority_df']['Description_tr'],
        dataframes['priority_df']['Priority_codes'],
        session['tfidf'],
        smt,
        chi2,
        50,
        svm_imb,
        model_path + secure_filename('priority'))
    # ttr models training
    smt.k_neighbors = get_k_neighbors(dataframes['ttr_df']['coded_ttr_intervals'])
    training_imbalance(
        dataframes['ttr_df']['Description_tr'],
        dataframes['ttr_df']['coded_ttr_intervals'],
        session['tfidf'],
        smt,
        chi2,
        50,
        svm_imb,
        model_path + secure_filename('ttr'))

    # resolution models training
    for resol in filtered_classes['resolutions_classes']:
        smt.k_neighbors = get_k_neighbors(dataframes['resolution_df']['Resolution_' + resol])
        training_imbalance(dataframes['resolution_df']['Description_tr'],
                              dataframes['resolution_df']['Resolution_' + resol],
                              session['tfidf'],
                              smt,
                              chi2,
                              50,
                              svm_imb,
                              model_path + secure_filename(resol))

