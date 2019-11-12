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

import numpy
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas
import datetime
import calendar
from main.validation import is_float
from main.data_converter import stringify_date


def get_relative_density_chart_coordinates(series, bins):
    """Calculates relative density chart coordinates.

    Parameters:
        series (Series): x_axis parameter value;
        bins (int): charts columns count.

    Returns:
        coordinates.
    """
    values = numpy.array(list(series))
    y, x, bars = plt.hist(values, weights=numpy.zeros_like(values) + 1. / values.size, bins=bins)
    return x, y


def get_frequency_density_chart_histogram_coordinates(series, bins):
    """Calculates histogram frequency density chart coordinates.

    Parameters:
        series (Series): x_axis parameter value;
        bins (int): chart's columns count.

    Returns:
        coordinates.
    """
    values = numpy.array(list(series))
    y, x, bars = plt.hist(values, bins=bins, density=True)
    return x, y


def get_frequency_density_chart_coordinates(series):
    """Calculates line frequency density chart coordinates.

    Parameters:
        series (Series): x_axis parameter value.

    Returns:
        coordinates.
    """
    try:
        density = stats.kde.gaussian_kde(list(series))
        x_den = numpy.linspace(0, series.max(), series.count())
        density = density(x_den)
        return x_den, density
    except numpy.linalg.linalg.LinAlgError:
        return [-1], [-1]



def get_coordinates_defect_submission(df, step_size):
    """ Calculates the coordinates for Cumulative chart of defect submission.

        Parameters:
            df (DataFrame): defect reports' file parsed to pandas DataFrame;
            step_size (str): step size value.

        Returns:
            plot(dict): chart coordinates

    """
    plot = {}
    coordinates = []
    x = []
    y = []
    periods = get_periods(df, step_size)

    current_index = 0
    next_index = 1
    bugs_count = 0

    while next_index < len(periods):
        bugs_count = bugs_count + int(df[(df['Created'] >= periods[current_index]) & (
            df['Created'] < periods[next_index])]['Key'].count())
        x.append(str(stringify_date(datetime.datetime.date(
            periods[current_index]), step_size)))
        y.append(bugs_count)
        current_index = current_index + 1
        next_index = next_index + 1
    if df['Created'].max() >= periods[-1]:
        bugs_count = bugs_count + int(df[(df['Created'] >= periods[-1]) &
                                         (df['Created'] <= df['Created'].max())]['Key'].count())
        x.append(
            str(stringify_date(datetime.datetime.date(periods[-1]), step_size)))
        y.append(bugs_count)
    coordinates.append(x)
    coordinates.append(y)
    plot['defect_submission_chart'] = coordinates
    return plot


def get_periods(dataframe, period):
    """Calculates periods for Defect Submission chart.

    Parameters:
        dataframe (DataFrame): file's data;
        period (str): a string representation of the period.

    Returns:
        periods(list): list of periods.
    """

    periods = []
    periods_frame = pandas.period_range(start=dataframe['Created'].min(), end=dataframe['Created'].max(), freq=period)
    for period in periods_frame:
        periods.append(pandas.to_datetime(str(period).split('/')[0], format='%Y-%m-%d'))
    return periods


def calculate_coordinates(dataframe, x='ttr', y='Relative Frequency', scale_size='', step_size='', period='W-SUN'):
    """Calculates charts' coordinates.

    Parameters:
        dataframe (DataFrame): file's data;
        x (str): x_axis parameter value;
        y (str): y_axis parameter value;
        scale_size (str): scale size value;
        step_size (str): step size value;
        period (str): string representation of the period.

    Returns:
        charts(dict): dictionary with the chart's coordinates.
    """
    charts = {}
    charts[y] = {}
    charts[y]['scale'] = scale_size
    charts[y]['stepSize'] = step_size
    charts[y]['fieldsVal'] = {'y': y, 'x': x}
    if y == 'Relative Frequency':
        x_axis, y_axis = get_relative_density_chart_coordinates(dataframe[x].dropna().apply(int), 10)
        charts[y]['coordinates'] = [list(x_axis), list(y_axis)+[float(0)]]
        return charts
    if y == 'Frequency density':
        x_hist, y_hist = get_frequency_density_chart_histogram_coordinates(dataframe[x].dropna().apply(int), 'fd')
        x_line, y_line = get_frequency_density_chart_coordinates(dataframe[x].dropna().apply(int))
        charts[y]['coordinates'] = {'histogram': [list(x_hist), list(y_hist)+[float(0)]],
                                    'line': [list(x_line), list(y_line)]}
        return charts
    if y == 'Dynamic':
        return get_coordinates_defect_submission(dataframe, period)


def add_disrtibution_charts(charts, dynamic_chart):
    charts['defect_submission_chart'] = dynamic_chart
    return charts


def check_scale_and_step(x_max, step_size, x, stat_info):
    """Checks whether the scale's and step's sizes are empty and correct.

    Parameters:
        x_max (str): maximum scale value;
        step_size (str): step size value;
        x (str): x_axis parameter value;
        stat_info (dict): dictionary with statistical information.

    Returns:
        Boolean value.
    """

    if x_max == '' and step_size == '':
        return True
    elif x_max != '' and step_size == '':
        return validate_scale_or_step(float(x_max), x, stat_info)
    elif step_size != '' and x_max == '':
        return validate_scale_or_step(float(step_size), x, stat_info)
    elif x_max != '' and is_float(x_max) and step_size != '' and is_float(step_size):
        return validate_scale_or_step(float(x_max), x, stat_info) and \
                validate_scale_or_step(float(step_size), x, stat_info)
    else:
        return False


def validate_scale_or_step(x_max, x, stat_info):
    """Checks whether the scale's and step's sizes are in the valid interval.

    Parameters:
        x_max (str): maximum scale value;
        x (str): x_axis parameter value;
        stat_info (dict): dictionary with statistical information.

    Returns:
        Boolean value.
    """

    if x_max >= 0:
        if x == 'ttr':
            return x_max <= float(stat_info['ttr_stat']['max'])
        if x == 'Comments':
            return x_max <= float(stat_info['comments_stat']['max'])
        if x == 'Attachments':
            return x_max <= float(stat_info['attachments_stat']['max'])
    else:
        return False
