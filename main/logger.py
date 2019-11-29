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


import logging
import pickle
import os
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, matthews_corrcoef
import functools
from datetime import datetime
from flask import session
from main.file_processor import is_file_exist
from logging import handlers


def __get_prediction(description, field_values, model_path):
    """ Generate cross-validated estimates for each input data point.

        Parameters:
            description (Series): descriptions series;
            field_values (Series): series of codes for each class;
            model_path: path to model.

        Returns:
            prediction(ndarray): cross-validated estimates.

    """
    prediction = cross_val_predict(
        pickle.load(
            open(
                model_path +
                '.sav',
                'rb')),
        description,
        field_values,
        cv=10,
        n_jobs=4)
    return prediction


def get_level(logger, level):
    """ Setting up logging level.

        Parameters:
            logger (Loger): logger object;
            level (str): logging level.

        Returns:
            logging level object.

    """
    if level == 'DEBUG':
        return logging.DEBUG
    elif level == 'INFO':
        return logging.INFO
    elif level == 'WARNING':
        return logging.WARNING
    elif level == 'ERROR':
        return logging.ERROR
    elif logging == 'CRITICAL':
        return logging.CRITICAL


def load_base_loggers_config(func):
    """ Setting up logger options.

        Parameters:
            func (Function): a function to log.

        Returns:
            logger (Loger): logger object.

    """
    logger = logging.getLogger('{func}'.format(func=func.__name__))
    logger.setLevel(
        get_level(
            logger,
            session['config.ini']['DEFECT_ATTRIBUTES']['logging_level'][0]))
    if not len(logger.handlers):
        date = datetime.date(datetime.today())
        if not is_file_exist('logs/' + str(date) + '/'):
            os.makedirs('logs/' + str(date) + '/')
        file_handler = handlers.RotatingFileHandler(
            filename='logs/' + str(date) + '/' + str(
                session['session_id']) + '.log',
            maxBytes=50 * 1024 * 1024,
            backupCount=10)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def log(func):
    """ Functions' logging decorator.

        Parameters:
            func (Function): a function to log.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        logger = load_base_loggers_config(func)
        start = datetime.now()
        func_result = func(*args, **kwargs)
        logger.info(
            'function: {module}.{name}, arguments:{name}({args},{kwargs}) \
            \ntotal execution date: {date}\
            \nfunctions_result: {func_result}\n'.format(
                start_time=start,
                module=func.__module__,
                name=func.__name__,
                args=args,
                kwargs=kwargs,
                date=datetime.now() - start,
                func_result=func_result))
        return func_result
    return wrapped


def log_train(func):
    """ Training logging decorator.

        Parameters:
            func (Function): a function to log.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        descr, areas, model_path = args[0], args[1], args[len(args) - 1]
        logger = load_base_loggers_config(func)
        target_names = [str(x) for x in range(len(areas.unique().tolist()))]
        start = datetime.now()
        func(*args)
        prediction = __get_prediction(descr, areas, model_path)
        if areas.name.split('_')[-1] == 'lab':
            result = '\ntotal execution date: {date} \nareas_name: {areas_name} \n{reports}'.format(
                date=datetime.now() - start,
                areas_name=areas.name,
                reports=classification_report(
                    areas,
                    prediction,
                    target_names=target_names) + '\n' + 'accuracy_score ' + str(
                    accuracy_score(
                        areas,
                        prediction)) + '\n' + 'roc_auc_score ' + str(
                    roc_auc_score(
                        areas,
                        prediction)) + '\n' + 'matthews_corrcoef ' + str(
                            matthews_corrcoef(
                                areas,
                                prediction)) + '\n')
        else:
            result = '{}'.format(
                '\n areas_name: ' + areas.name + '\n' +
                classification_report(
                    areas,
                    prediction,
                    target_names=[
                        str(el) for el in areas.unique().tolist()]))
        logger.info(result)
    return wrapped

