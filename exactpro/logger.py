'''
/*******************************************************************************
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
******************************************************************************/
'''


import logging
import pickle
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, matthews_corrcoef


class BynaryTrainLogger:
    def log(self, filename, descr, area, area_name, model_path):
        logger = logging.getLogger(area_name)
        logger.setLevel(logging.INFO)
        # clear handlers to exclude dublicated rows
        if logger.hasHandlers():
            logger.handlers = []
        log = logging.FileHandler(filename)
        log.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(log)
        pred_ = cross_val_predict(pickle.load(open(model_path+area_name+'.sav', 'rb')), descr, area, cv=10, n_jobs=4)

        rez = '{}'.format('\n'+classification_report(area, pred_, target_names=['0', '1']) + '\n' +
                                'accuracy_score ' + str(accuracy_score(area, pred_)) + '\n' +
                                'roc_auc_score '+str(roc_auc_score(area, pred_)) + '\n' +
                                'matthews_corrcoef '+str(matthews_corrcoef(area, pred_))+'\n')
        logger.info(rez)


class MultipleTrainLogger:
    def log(self, filename, descr, area, area_name, model_path):
        logger = logging.getLogger(area_name)
        logger.setLevel(logging.INFO)
        # clear handlers to exclude dublicated rows 
        if logger.hasHandlers():
            logger.handlers = []
        log = logging.FileHandler(filename)
        log.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(log)
        pred_ = cross_val_predict(pickle.load(open(model_path+area_name+'.sav', 'rb')), descr, area, cv=10, n_jobs=4)
        rez = '{}'.format('\n'+classification_report(area, pred_, target_names=[str(el) for el in area.unique().tolist()]))
        logger.info(rez)