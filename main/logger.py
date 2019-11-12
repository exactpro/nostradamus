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
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, matthews_corrcoef



class Logger:
    def __init__(self, filename):
        self.filename = filename

    def _get_logger(self, area_name):
        logger = logging.getLogger(area_name)
        logger.setLevel(logging.INFO)
        # clear handlers to exclude dublicated rows
        if logger.hasHandlers():
            logger.handlers = []
        log = logging.FileHandler(self.filename)
        log.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(log)
        return logger

    def _get_prediction(self, description, area_values, area_name, model_path):
        prediction = cross_val_predict(
            pickle.load(
                open(
                    model_path +
                    area_name +
                    '.sav',
                    'rb')),
            description,
            area_values,
            cv=10,
            n_jobs=4)
        return prediction

class BynaryTrainLogger(Logger):
    def __init__(self, file_name):
        self.filename = file_name

    def log(self, description, area_values, area_name, model_path):
        prediction = self._get_prediction(description, area_values, area_name, model_path)
        logger = self._get_logger(area_name)
        result = '{}'.format('\n' +
                          classification_report(area_values, prediction, target_names=['0', '1']) +
                          '\n' +
                          'accuracy_score ' +
                          str(accuracy_score(area_values, prediction)) +
                          '\n' +
                          'roc_auc_score ' +
                          str(roc_auc_score(area_values, prediction)) +
                          '\n' +
                          'matthews_corrcoef ' +
                          str(matthews_corrcoef(area_values, prediction)) +
                          '\n')
        logger.info(result)


class MultipleTrainLogger(Logger):
    def __init__(self, file_name):
        self.filename = file_name
    
    def log(self, descr, area_values, area_name, model_path):
        prediction = self._get_prediction(descr, area_values, area_name, model_path)
        logger = self._get_logger(area_name)
        result = '{}'.format(
            '\n' +
            classification_report(
                area_values,
                prediction,
                target_names=[
                    str(el) for el in area_values.unique().tolist()]))
        logger.info(result)


