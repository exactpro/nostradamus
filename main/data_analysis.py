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


import swifter
import pandas
import datetime
import numpy
import re
import os
import shutil
import sys
import pickle
import swifter
from decimal import Decimal
from sklearn.feature_extraction import text
from collections import OrderedDict
from sklearn import feature_selection
from sklearn.feature_selection import SelectKBest
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import session


from main.cleaner import clean_description
from main.data_converter import convert_date, math_round
from multiprocessing import cpu_count, Pool, Process


def apply_datatype(series, series_name, attribute_type):
    """ Converts series to specific datatype.

    Parameters:
        series (Series)
        series_name (str)
        attribute_type (str): defect attribute type.

    Returns:
        converted series.

    """
    if not len(series.dropna().unique().tolist()) == 0:
        try:
            if attribute_type in ['String', 'Substring', 'Substring_array', 'Categorical']:
                if series.dtype != 'object':
                    series = series.swifter.progress_bar(
                        enable=False, desc=None).apply(str)
                series = series.fillna(
                    value='None')
            if attribute_type == 'Date':
                series = pandas.to_datetime(series, dayfirst=True)
            if attribute_type == 'Numeric':
                series = series.swifter.progress_bar(
                    enable=False, desc=None).apply(Decimal)
        except Exception:
            series = numpy.nan
            series = numpy.nan
    return series


def transform_series(df, defect_attributes):
    """ Transforms series to make theirs' data ready for analysis.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame;
        defect_attributes (dict): defect attributes configurations;.

    Returns:
        DataFrame with transformed series appended.

    """
    df['Resolved'] = df['Resolved'].fillna(
        value='').astype(str).swifter.progress_bar(
    enable=False, desc=None).apply(
        convert_date)
    df['Created'] = df['Created'].fillna(
        value='').astype(str).swifter.progress_bar(
    enable=False, desc=None).apply(
        convert_date)
    for group in ['special_attributes', 'mandatory_attributes']:
        for attribute in defect_attributes[group]:
            df[attribute] = apply_datatype(
                df[attribute], attribute, defect_attributes[group][attribute]['type'])     
    pool = Pool()
    df['Description_tr'] = pool.map(clean_description, df['Description'])
    pool.close()
    pool.join()

    df['Resolved_tr'] = df['Resolved'].fillna(
        value=datetime.date.today())
    df['ttr'] = (df['Resolved_tr'] - df['Created']).dt.days
    defect_attributes['special_attributes']['ttr'] = {
        'name': 'Time to Resolve (TTR)', 'type': 'Numeric'}
    df[defect_attributes['markup_series']] = df[defect_attributes['markup_series']].str.lower()
    return df


def get_fields(field_type, defect_attributes):
    """ Returns a list of strings.

        Parameters:
            field_type (str): Field type.

        Returns:
            list of strings.   

    """
    return [field for group in ['special_attributes', 'mandatory_attributes']
            for field in defect_attributes[group] if defect_attributes[group][field]['type'] == field_type]


def filter_dataframe(
        field_name,
        field_value,
        dataframe,
        defect_attributes):
    """ Filters dataframe.

        Parameters:
            field_name (str): Name of the field by which we filter.
            field_value (str): Value of the field by which we filter.
            dataframe (DataFrame): Data that we filter.
            defect_attributes (dict): Defect attributes.
        
        Returns:
            Filtered DataFrame.

    """
    filtered_df = pandas.DataFrame()
    if field_name in session['config.ini']['DEFECT_ATTRIBUTES']['areas_of_testing']:
        field_value = 1 if field_value == 'Yes' else 0
        filtered_df = dataframe[dataframe[field_name+'_lab'].swifter.apply(bool) == field_value]
    if field_name in get_fields('Categorical', defect_attributes):
        filtered_df = dataframe[dataframe[field_name].swifter.apply(apply_categorical_filter, args=(field_value,))]
    if field_name in get_fields('Boolean', defect_attributes):
        field_value = 1 if field_value == 'Yes' else 0
        filtered_df = dataframe[dataframe[field_name].swifter.apply(bool) == field_value]
    if field_name in get_fields('String', defect_attributes):
        filtered_df = dataframe[dataframe[field_name] == field_value]
    if field_name in get_fields('Substring', defect_attributes):
        filtered_df = dataframe[dataframe[field_name].
                                  str.contains(field_value,
                                               case=False, na=False, regex=False)]
    if field_name in get_fields('Substring_array', defect_attributes):
        filtered_df = dataframe
        for pattern in field_value.split(','):
            filtered_df = apply_substring_array_filter(
                filtered_df, field_name, pattern.strip())
    if field_name[:-1] in get_fields('Numeric', defect_attributes):
        if field_name[-1] == '0':
            filtered_df = dataframe[dataframe[field_name[:- \
                1]] >= Decimal(field_value)]
        elif field_name[-1] == '1':
            filtered_df = dataframe[dataframe[field_name[:- \
                1]] <= Decimal(field_value)]
    if field_name[:-1] in get_fields('Date', defect_attributes):
        if field_name[-1] == '0':
            filtered_df = dataframe[dataframe[field_name[:-
                                                           1]] >= datetime.datetime.strptime(field_value,'%d-%m-%Y')]
        if field_name[-1] == '1':
            filtered_df = dataframe[dataframe[field_name[:-
                                                           1]] <= datetime.datetime.strptime(field_value,'%d-%m-%Y')]
    return reindex_dataframe(filtered_df)


def apply_substring_array_filter(df, series, pattern):
    """ Filters dataframe.

        Parameters:
            df(DataFrame): defect reports' file parsed to pandas DataFrame;
            series(str): series name;
            pattern(str): the value you're looking for.

        Returns:
            filtered_df(DataFrame): filtered dataframe.
    """
    filtered_df = df[df[series].swifter.progress_bar(
        enable=False, desc=None).apply(compare_words, args=(pattern,))]
    return filtered_df[filtered_df[series].str.contains(
        pattern, case=False, na=False, regex=False)]


def apply_categorical_filter(df_element, field_value):
    return bool(set(df_element.split(',')).intersection(set(field_value.split(','))))


def compare_words(value, pattern):
    """ Checks whether the elements are equal.

        Parameters:
            value(str): dataframe element;
            pattern(str): the value you're looking for.

        Returns:
            Boolean value.
    """
    regexp = re.compile(r'\b' + pattern + r'\b', re.IGNORECASE)
    return bool(re.findall(regexp, str(value)))


def rollback_filter(df_paths):
    """ Rolls back dataframe to original state.

        Parameters:
            df_paths(dict): paths to dataframes' files.

    """
    os.remove(df_paths['filtered_df'])
    shutil.copy(
        df_paths['source_df'],
        os.path.abspath(df_paths['filtered_df']))


def reindex_dataframe(dataframe):
    """ Reindexes dataframe and drops index column.

        Parameters:
            dataframe(DataFrame): defect reports' file parsed to pandas DataFrame.

        Returns:
            reindexed_data(DataFrame): Transformed dataframe.
    """
    return dataframe.reset_index(drop = 'index' in list(dataframe)).drop(['index'], axis='columns')


def get_predictions_table(
        df,
        index,
        areas_of_testing,
        resolutions,
        prediction_parameters):
    """ Generates predictions for each defect from handled DataFrame.

        Parameters:
            df (DataFrame): defect reports' file parsed to pandas DataFrame;
            areas_of_testing (list): areas of testing;
            resolutions (list) : resolutions' values.
            prediction_parameters (dict): prediction_paraameters.

        Returns:
            predictions(dict): predictions for each defect.

    """
    defect_predictions = {}
    defect_predictions['Summary'] = df['Summary'][index]
    defect_predictions['Priority'] = df['Priority'][index]
    ttr_probabilities = get_probabilities(
        df['Description_tr'][index], prediction_parameters['ttr_classes'], str(
            Path(__file__).parents[1]) + '/models/selected/' + 'ttr')

    defect_predictions['ttr'] = max(
        ttr_probabilities,
        key=ttr_probabilities.get)
    for resolution in resolutions:
        resolution_probabilities = get_probabilities(df['Description_tr'][index], prediction_parameters[resolution.lower(
        ) + '_classes'], str(Path(__file__).parents[1]) + '/models/selected/' + secure_filename(resolution))

        defect_predictions[resolution] = (
            max(resolution_probabilities, key=resolution_probabilities.get))
    areas_probabilities = {}
    for area in areas_of_testing:
        area_probabilities = get_probabilities(
            df['Description_tr'][index], prediction_parameters['binary_classes'], str(
                Path(__file__).parents[1]) + '/models/selected/' + secure_filename(area))
        areas_probabilities.update({area: float(area_probabilities[1])})

    defect_predictions['area_of_testing'] = [
        area for area,
        probability in areas_probabilities.items() if probability > 0.5] if [
        area for area,
        probability in areas_probabilities.items() if probability > 0.5] else 'no idea'
    return (df['Key'][index], defect_predictions)


def get_probabilities(text, model_classes, model_path):
    """ Calculates probabilities of text belonging to each models' class.

        Parameters:
            text (str): text for analysis;
            model_classes(list): models' classes;
            model_path(str): the path to the model file.

        Returns:
            probabilities(dict):  probabilities of finding a word in a particular class.

    """
    model = pickle.load(open(model_path + '.sav', 'rb'))
    probabilities = numpy.array(
        numpy.around(
            model.predict_proba(
                [text])[0],
            3),
        dtype=float).flatten()
    probabilities = dict(zip(model_classes, probabilities))
    return probabilities


def run_in_parallel(flask, redis_expire):
        flask_proc = Process(target=flask) # thread 1: Flask processes
        flask_proc.start()
        expire_proc = Process(target=redis_expire, args=(flask_proc,)) # thread 2: session status activities
        expire_proc.start()
        proc = [flask_proc, expire_proc]
        for pr in proc:
            pr.join()


def calculate_top_terms(df, metric):
    """ Calculates top terms which are based on significance weights.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame;
        metric (str): field which is used for calculation.

    Returns:
        list of the calculated terms.

    """
    chi2 = feature_selection.chi2
    tfs = session['tfidf'].fit_transform(df['Description_tr'])
    y = df[metric]
    selector = SelectKBest(score_func=chi2, k='all')
    selector.fit_transform(tfs, y)
    terms = dict(zip(session['tfidf'].get_feature_names(), selector.scores_))
    terms = {k: v for (k, v) in terms.items() if v > 1}
    return [
        k for (
            k,
            v) in terms.items() if v > numpy.mean(
            list(
                terms.values()))]


from main.data_converter import unpack_dictionary_val_to_list
def create_top_terms_file(df, resolutions, priorities, areas_of_testing):
    """ Saves top terms' calculations results to csv file.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame;
        resolutions (dict): resolutions;
        priorities (list): priorities derived after models' training;
        areas_of_testing (list): areas of testing derived after models' training.

    """
    binarized_df = pandas.get_dummies(
        df,
        prefix=list(
            resolutions.keys()) +
        ['Priority'],
        columns=list(
            resolutions.keys()) +
        ['Priority'])
    top_terms = {}

    for priority in priorities:
        top_terms[priority] = calculate_top_terms(
            binarized_df, 'Priority_' + priority)
    for resolution in resolutions:
        for val in list(resolutions[resolution]):
            if 'not' not in val:
                top_terms[val] = calculate_top_terms(
                    binarized_df, resolution + '_' + val)
    for area in areas_of_testing:
        if area != 'Other':
            top_terms[area] = calculate_top_terms(binarized_df, area + '_lab')
    top_terms = pandas.DataFrame(
        dict([(k, pandas.Series(v)) for k, v in top_terms.items()]))
    top_terms.to_csv(
        str(Path(__file__).parents[1]) + '/models/selected/' + 'top_terms.csv', index=False)


import swifter
def mark_up_series(
        df,
        series,
        area_of_testing,
        patterns):
    """ Appends binarized series to df.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame;
        series (str): df series name;
        area_of_testing (str):
        patterns (str): searching elements.

    Returns:
        The whole df with binarized series.

    """
    df[area_of_testing] = df[series].swifter.progress_bar(
        enable=False, desc=None).apply(
        binarize_value, args=(
            patterns,))
    return df


def binarize_value(df_element, patterns):
    """ Binarizes searching value.

    Parameters:
        df_element (str): searching source;
        patterns (str): searching elements.

    Returns:
        Binarized value.

    """
    for pattern in patterns.split("|"):
        if pattern.strip() in str(df_element).split(","):
            return 1
    return 0
        

def mark_up_other_data(df, marked_up_series):
    """ Marks up series which represents data that isn't related to marked up fields.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame;
        marked_up_series (list): names of marked up series.

    Returns:
        The whole dataframe with new series appended.

    """
    df['Other_lab'] = '0'
    # replaces field value to 1 when summ of the fields from marked_up_series
    # is 0
    df['Other_lab'] = df['Other_lab'].replace(
        ['0'], '1').where(
        df[marked_up_series].sum(
            axis=1) == 0, 0).apply(int)
    return df


def check_bugs_count(dataframe, required_count: int):
    return len(dataframe.index) >= required_count


def calculate_significant_terms(df, metric, sw=text.ENGLISH_STOP_WORDS.difference(('see', 'system', 'call'))):
    """ Calculates top terms which are based on significance weights.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame;
        metric (str): field which is used for calculation.

    Returns:
        list of the first 20 calculated terms.

    """
    if not metric or metric == 'null':
        return ['Oops! Too little data to calculate.']
    chi2 = feature_selection.chi2
    term = metric.replace(
        'Areas of testing ',
        '') + '_lab' if 'Areas of testing' in metric else metric.split()[0] + "_" + ' '.join(
        metric.split()[
            1:])
    if term.split('_')[0] in ('Resolution', 'Priority'):
        df = pandas.get_dummies(
            df, prefix=[
                term.split('_')[0]], columns=[
                term.split('_')[0]])  # data binarisation

    description = df['Description_tr']
    tfs = session['tfidf'].fit_transform(description)

    y = df[term]
    # select the most significant terms
    selector = SelectKBest(score_func=chi2, k='all')
    selector.fit_transform(tfs, y)
    calculated_terms = dict(zip(session['tfidf'].get_feature_names(), selector.scores_))
    calculated_terms = OrderedDict((k, v) for k, v in sorted(
        calculated_terms.items(), key=lambda x: x[1], reverse=True))
    return list(calculated_terms.keys())[:20]


def get_records_count(filtered_df, source_df):
    return {'total': str(source_df['Key'].count()),
            'filtered': str(filtered_df['Key'].count())}


def get_statistical_info(df):
    """ Statistical info calculation.

    Parameters:
        df (DataFrame): defect reports' file parsed to pandas DataFrame.

    Returns:
        dict object filled in calculated statistics.

    """
    comments = df['Comments'].swifter.progress_bar(
        enable=False, desc=None).apply(int)
    attachments = df['Attachments'].swifter.progress_bar(
        enable=False, desc=None).apply(int)
    return {'comments_stat': {
        'min': str(comments.min()),
        'max': str(comments.max()),
        'mean': str(int(math_round(comments.mean()))),
        'std': str(int(math_round(numpy.nan_to_num(comments.std()))))
    },
        'attachments_stat': {
        'min': str(attachments.min()),
        'max': str(attachments.max()),
        'mean': str(int(math_round(attachments.mean()))),
        'std': str(int(math_round(numpy.nan_to_num(attachments.std()))))
    },
        'ttr_stat': {
        'min': str(df['ttr'].min()),
        'max': str(df['ttr'].max()),
        'mean': str(int(math_round(df['ttr'].mean()))),
        'std': str(int(math_round(numpy.nan_to_num(df['ttr'].std()))))
    }
    }


def get_frequently_terms(descr_series):
    """ Calculates most frequently used terms.

    Parameters:
        descr_series (Series): defects' descriptions.

    Returns:
        list of the first 100 calculated terms.

    """
    try:
        session['tfidf'].fit_transform(descr_series)
    except ValueError:
        return ['Oops! Too little data to calculate.']
    idf = session['tfidf'].idf_

    frequently_terms = dict(zip(session['tfidf'].get_feature_names(), idf))
    frequently_terms = OrderedDict((k, v) for k, v in sorted(
        frequently_terms.items(), key=lambda x: x[1], reverse=True))
    return list(frequently_terms.keys())[:100]

