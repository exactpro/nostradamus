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


from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction import text
from sklearn.svm import SVC
import os
import pandas
from imblearn.pipeline import Pipeline
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold
from nltk.stem.snowball import SnowballStemmer
import re
import numpy
import csv
import psycopg2
import logging
import traceback
import sys
from werkzeug.utils import secure_filename
import time
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, matthews_corrcoef, precision_recall_fscore_support
from sklearn import feature_selection
from sklearn.feature_selection import SelectKBest
from flask import session
from collections import OrderedDict
import csv
from itertools import zip_longest
from exactpro.config_parser import ConfigCreator
from exactpro.logger import BynaryTrainLogger, MultipleTrainLogger
from exactpro.filter import Filter
from exactpro.my_multithread import Multithreaded
from exactpro.cleaner import ClearData
from exactpro.config_parser import SettingProvider
from exactpro.data_checker import Checker


class Model:
    def training_model(self, model_path, data_path, colums, resolution, sw=text.ENGLISH_STOP_WORDS, log=0):
        try:
            self.creater = ConfigCreator()
            smt = SMOTE(ratio='minority', random_state=0, kind='borderline1', n_jobs=4)
            svm_imb = SVC(gamma=2, C=1, probability=True, class_weight='balanced')
            tfidf_imb = StemmedTfidfVectorizer(norm='l2', sublinear_tf=True, stop_words=sw, analyzer='word', max_df=0.5, max_features=500)
            anova = feature_selection.f_classif
            chi2 = feature_selection.chi2
            if not os.path.exists(model_path):
                os.makedirs(model_path)
            self.data = pandas.read_pickle(data_path)
            binary_logger = BynaryTrainLogger()
            multiple_logger = MultipleTrainLogger()
            filter = Filter()
            self.creater.create_config('single_mod.ini', section_name='single_mod.ini'.split('.')[0])

            # models training 
            self.creater.update_setting('single_mod.ini', 'single_mod.ini'.split('.')[0], 'binary_col_class', ','.join(['0', '1']))

            # areas
            # to exclude columns with quite low percent of 1
            clear_columns = [column for column in colums if self.data[column][self.data[column] == 1].size/self.data[column].size > 0.005]
            self.creater.update_setting('single_mod.ini', 'single_mod.ini'.split('.')[0], 'columns', ','.join(clear_columns))
            for col in clear_columns:
                self.data['Description_tr'] = self.data['Description_tr']
                Model.training_imbalance_kf(self, self.data['Description_tr'], self.data[col], tfidf_imb, smt, chi2, 50, svm_imb, secure_filename(col), model_path)
                if log == 1:
                    binary_logger.log('{}.log'.format(session.sid), self.data['Description_tr'], self.data[col], col, model_path)

            # priority
            # to exclude rows with quite low percent of any categorical value
            self.valid_set = [el for el in self.data['Priority'].unique().tolist() if self.data['Priority'][self.data['Priority'] == el].size/self.data['Priority'].size > 0.005]
            self.data_after_filter = self.data[self.data['Priority'].isin(self.valid_set)]
            if self.data.shape[0] > self.data_after_filter.shape[0]:
                self.data_after_filter = filter.reindex_data(self.data_after_filter)
            self.data_after_filter['Priority_ord'] = self.data_after_filter['Priority'].astype("category")
            self.data_after_filter['Priority_ord_codes'] = pandas.Categorical(self.data_after_filter['Priority_ord']).codes
            # train
            Model.training_imbalance_kf(self, self.data_after_filter['Description_tr'], self.data_after_filter['Priority_ord_codes'], tfidf_imb, smt, chi2, 50, svm_imb, 'priority', model_path)
            self.creater.update_setting('single_mod.ini', 'single_mod.ini'.split('.')[0], 'prior_col_class',
                                        ','.join(self.data_after_filter['Priority'].unique().tolist()))
            # log
            if log == 1:
                # print('priority')
                # start = time.clock()
                multiple_logger.log('{}.log'.format(session.sid), self.data_after_filter['Description_tr'], self.data_after_filter['Priority_ord_codes'], 'priority', model_path)
                # print(time.clock()-start)

            bins = 4
            self.ldis = [i for i in range(1, bins+1)]

            # ttr
            # to exclude rows with quite low percent of any categorical value
            self.data['temp_ttr_class'] = pandas.qcut(self.data['ttr_tr'], bins, labels=self.ldis, duplicates='drop')
            self.valid_set = [el for el in self.data['temp_ttr_class'].unique().tolist() if self.data['temp_ttr_class'][self.data['temp_ttr_class'] == el].size/self.data['temp_ttr_class'].size > 0.005]
            self.data_after_filter = self.data[self.data['temp_ttr_class'].isin(self.valid_set)]
            if self.data.shape[0] > self.data_after_filter.shape[0]:
                self.data_after_filter = filter.reindex_data(self.data_after_filter)
            # train
            Model.training_imbalance_kf(self, self.data_after_filter['Description_tr'], self.data_after_filter['temp_ttr_class'], tfidf_imb, smt, chi2, 50, svm_imb, 'ttr', model_path)
            self.ttr_col_classTemp = pandas.qcut(self.data_after_filter['ttr_tr'], 4, duplicates='drop').unique()
            self.creater.update_setting('single_mod.ini', 'single_mod.ini'.split('.')[0], 'ttr_col_class',
                                        ','.join([str(Model.ifZero(self, self.ttr_col_classTemp[el].left))+'-'+str(Model.ifZero(self, self.ttr_col_classTemp[el].right)) for
                                                  el in range(3)] + ['>'+str(Model.ifZero(self, self.ttr_col_classTemp[range(3)[-1]].right))]))
            # log
            if log == 1:
                multiple_logger.log('{}.log'.format(session.sid), self.data_after_filter['Description_tr'], self.data_after_filter['temp_ttr_class'], 'ttr', model_path)

            # resolution
            # resolution may have values wich can't be correctly processed by the system like: "Won't Fix"
            # therefore we have to convert them to model name via secure_filename() function
            self.bin_data = pandas.get_dummies(self.data, prefix=list(resolution.keys()), columns=list(resolution.keys()))
            # to exclude columns with quite low percent of 1
            clear_columns = {}
            for key in resolution:
                if isinstance(resolution[key], list):
                    resolutions = []
                    for rez in resolution[key]:
                        if self.bin_data[key+'_'+rez][self.bin_data[key+'_'+rez] == 1].size/self.bin_data[key+'_'+rez].size > 0.005:
                            resolutions.append(rez)
                    if len(resolutions) == 1:
                        clear_columns[key] = resolutions[0]
                    if len(resolutions) > 1:
                        clear_columns[key] = resolutions
                else:
                    if self.bin_data[key+'_'+resolution[key]][self.bin_data[key+'_'+resolution[key]] == 1].size/self.bin_data[key+'_'+resolution[key]].size > 0.005:
                        clear_columns[key] = resolution[key]

            for key in clear_columns:
                if isinstance(clear_columns[key], list):
                    for res in clear_columns[key]:
                        Model.training_imbalance_kf(self, self.bin_data['Description_tr'], self.bin_data[key+'_'+res], tfidf_imb, smt, chi2, 50, svm_imb, secure_filename(res), model_path)
                        self.creater.update_setting('single_mod.ini', 'single_mod.ini'.split('.')[0], res+'_col_class', ','.join(['not '+res, res]))
                        if log == 1:
                            binary_logger.log('{}.log'.format(session.sid), self.bin_data['Description_tr'], self.bin_data[key+'_'+res], secure_filename(res), model_path)
                else:
                    Model.training_imbalance_kf(self, self.bin_data['Description_tr'], self.bin_data[key+'_'+clear_columns[key]], tfidf_imb, smt, chi2, 50, svm_imb, secure_filename(clear_columns[key]), model_path)
                    self.creater.update_setting('single_mod.ini', 'single_mod.ini'.split('.')[0], clear_columns[key]+'_col_class', ','.join(['not '+clear_columns[key], clear_columns[key]]))
                    if log == 1:
                        binary_logger.log('{}.log'.format(session.sid), self.bin_data['Description_tr'], self.bin_data[key+'_'+clear_columns[key]], secure_filename(clear_columns[key]), model_path)

            self.data.to_pickle(data_path)
        except FileNotFoundError:
            raise

    def training_imbalance_kf(self, X_, Y_, TFIDF_, IMB_, FS_, pers_, CLF_, name_, model_path):
        self.transform = feature_selection.SelectPercentile(FS_)
        self.clf_model = Pipeline([('tfidf', TFIDF_), ('imba', IMB_), ('fs', self.transform), ('clf', CLF_)])
        kf = KFold(n_splits=10)
        kf.get_n_splits(X_)
        #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X_,Y_,train_size=.8, stratify=Y_)
        for train_index, test_index in kf.split(X_):
            self.X_train, self.X_test = X_[train_index], X_[test_index]
            self.y_train, self.y_test = Y_[train_index], Y_[test_index]
        self.clf_model.set_params(fs__percentile=pers_).fit(self.X_train, self.y_train)
        pickle.dump(self.clf_model, open(model_path+name_+'.sav', 'wb'))
        #y_pred = clf_model.predict(X_test)
        #print(classification_report(y_test, y_pred))

    def ifZero(self, val):
        if val < 0:
            return 0
        else:
            return val

    def proc_text(self, text, col_class, name_model, model_path):
        self.test_pro = text
        try:
            with open('regularExpression.csv') as csv_data:
                for i in [re.compile(el1) for el in csv.reader(csv_data, delimiter=',', quotechar='"') for el1 in el if el1]:
                    self.test_pro = re.sub(i, ' ', self.test_pro)
            self.proba = {}
            sys.path.append("..")
            self.load_model_test = pickle.load(open(model_path+name_model+'.sav', 'rb'))
            self.proba_ = list(numpy.array(numpy.around(self.load_model_test.predict_proba([self.test_pro])[0], 3), dtype=float).flatten())
            self.proba_dic = dict(zip(col_class, self.proba_))
            return self.proba_dic
        except Exception:
            raise

    def create_top_terms_file(self, frame, resolution):
        checker = Checker()

        chi2 = feature_selection.chi2
        SW = text.ENGLISH_STOP_WORDS

        config_reader = SettingProvider('single_mod.ini')

        resol_all = []
        for el in checker.get_resolutions(resolution):
            resol_all += config_reader.get_setting(section='single_mod', setting="{el}_col_class".format(el=el), evaluate=False).split(',')

        resol = [el for el in resol_all if 'not' not in el]

        prio = config_reader.get_setting(section='single_mod',
                                         setting='prior_col_class', evaluate=False).split(',')

        areas = config_reader.get_setting(section='single_mod',
                                          setting='columns', evaluate=False).split(',')
        
        all_terms = prio + resol + areas
        all_mass = []
        bin_data = pandas.get_dummies(frame, prefix=list(resolution.keys())+['Priority'], columns=list(resolution.keys())+['Priority'])
        with open('top_terms.csv', 'w', newline='\n') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(all_terms)
            for el in all_terms:
                if el in prio:
                    prior = self.top_terms(bin_data, 'Priority_'+el, chi2, SW)
                    all_mass.append(prior)

                if el in resol:
                    key = None 
                    for key1 in resolution:
                        if isinstance(resolution[key1], list):
                            if el in resolution[key1]:
                                key = key1
                        else:
                            if el == resolution[key1]:
                                key = key1
                    resol = self.top_terms(bin_data, key+'_'+el, chi2, SW)
                    all_mass.append(resol)
                
                if el in areas:
                    area = self.top_terms(bin_data, el, chi2, SW)
                    all_mass.append(area)

            rows = zip_longest(*all_mass)
            for row in rows:
                csvwriter.writerow(row)

    def top_terms(self, data, field, func, SW):
        tfidf = StemmedTfidfVectorizer(norm='l2', sublinear_tf=True, min_df=1, stop_words=SW, analyzer='word',
                                       max_features=1000)
        # bidata = pandas.get_dummies(data, prefix=field+'_', columns=field)
        multithreaded = Multithreaded()
        clear_data = ClearData()
        parall_data = multithreaded.parallelize(data['Description_tr'], clear_data.clean_descr)
        tfs = tfidf.fit_transform(parall_data)
        y = data[field]
        selector = SelectKBest(score_func=func, k='all')
        selector.fit_transform(tfs, y)
        X_new = dict(zip(tfidf.get_feature_names(), selector.scores_))
        temp_dict = sorted(X_new.items(), key=lambda x: x[1], reverse=True)
        rez = []
        mean = []
        for el in temp_dict[:]:
            if el[1] > 1:
                rez.append(el)
                mean.append(el[1])
        import numpy
        return [el[0] for el in rez if el[1] > numpy.mean(mean)]


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: (SnowballStemmer("english").stem(w) for w in analyzer(doc))


class Insert:
    def insert_to_predictions(self, store, insert):
        self.conn = None
        self.cur = None
        self.logger = logging.getLogger("ul_submit.insert_to_predictions")
        try:
            self.conn = psycopg2.connect(**store)
            self.cur = self.conn.cursor()
            self.cur.execute(insert)
            self.conn.commit()
        except (psycopg2.DatabaseError, KeyboardInterrupt):
            self.logger.info(traceback.format_exc().splitlines()[traceback.format_exc().splitlines().__len__()-1])
            raise
        finally:
            if self.cur is not None:
                 self.cur.close()
            if self.conn is not None:
                 self.conn.close()


class ResearchInfo:
    def checking(self, load_model, X_, Y_, target_names):
        self.pred_ = cross_val_predict(load_model, X_, Y_, cv=10, n_jobs=4)
        # print(classification_report(Y_, self.pred_, target_names=target_names).split())
        # print(accuracy_score(Y_, self.pred_))
        # print(roc_auc_score(Y_, self.pred_))
        # print(matthews_corrcoef(Y_, self.pred_))
        return str(' '.join(classification_report(Y_, self.pred_, target_names=target_names).split())) + \
               ' accuracy_score ' + str(accuracy_score(Y_, self.pred_)) + \
               ' roc_auc_score '+str(roc_auc_score(Y_, self.pred_)) + \
               ' matthews_corrcoef '+str(matthews_corrcoef(Y_, self.pred_))


    def checking_multi(self, load_model, X_, Y_, target_names):
        self.pred_ = cross_val_predict(load_model,X_, Y_, cv=10, n_jobs=4)
        print(precision_recall_fscore_support(Y_, self.pred_, labels=target_names, average='weighted'))

