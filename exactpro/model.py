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
from exactpro.file import remove_models
from exactpro.my_multithread import Multithreaded
from exactpro.cleaner import ClearData
from exactpro.config_parser import SettingProvider
from exactpro.data_checker import Checker, verify_classes_amount, verify_samples_amount
from exactpro.xml_parser import clean_description
from exactpro.config_parser import unpack_dictionary_val_to_list


class Model:
    def proc_text(self, text, col_class, name_model, model_path):
        self.test_pro = text
        try:
            self.proba = {}
            sys.path.append("..")
            self.load_model_test = pickle.load(open(model_path+name_model+'.sav', 'rb'))
            self.proba_ = list(numpy.array(numpy.around(self.load_model_test.predict_proba([self.test_pro])[0], 3), dtype=float).flatten())
            self.proba_dic = dict(zip(col_class, self.proba_))
            return self.proba_dic
        except Exception as e:
            print(e)
            raise


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


def is_zero(val):
        if val < 0:
            return 0
        else:
            return val


def training_imbalance_kf(X_, Y_, TFIDF_, IMB_, FS_, pers_, CLF_, name_, model_path):
        transform = feature_selection.SelectPercentile(FS_)
        clf_model = Pipeline([('tfidf', TFIDF_), ('imba', IMB_), ('fs', transform), ('clf', CLF_)])
        kf = KFold(n_splits=10)
        kf.get_n_splits(X_)
        #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X_,Y_,train_size=.8, stratify=Y_)
        for train_index, test_index in kf.split(X_):
            X_train, X_test = X_[train_index], X_[test_index]
            y_train, y_test = Y_[train_index], Y_[test_index]
        clf_model.set_params(fs__percentile=pers_).fit(X_train, y_train)
        pickle.dump(clf_model, open(model_path+name_+'.sav', 'wb'))
        #y_pred = clf_model.predict(X_test)
        #print(classification_report(y_test, y_pred))


def train_model(model_path, dataframe_path, areas_of_testing, resolution, sw=text.ENGLISH_STOP_WORDS, log=0):
    try:
        filter = Filter()
        configuration = ConfigCreator()
        smt = SMOTE(ratio='minority', random_state=0, kind='borderline1', n_jobs=4)
        svm_imb = SVC(gamma=2, C=1, probability=True, class_weight='balanced')
        anova = feature_selection.f_classif
        chi2 = feature_selection.chi2
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        dataframe = pandas.read_pickle(dataframe_path)
        binary_logger = BynaryTrainLogger()
        multiple_logger = MultipleTrainLogger()
        bins = 4
        ldis = [i for i in range(1, bins+1)]

        # filtering out classes with quite low percent of categorical value
        # areas of testing
        areas_of_testing_filtered = [area for area in areas_of_testing if dataframe[area][dataframe[area] == 1].size/dataframe[area].size > 0.005]
        verify_classes_amount(areas_of_testing_filtered)
        for area in areas_of_testing_filtered:
            verify_samples_amount(dataframe, area)
        # priority classes
        priority_classes_filtered = [_class for _class in dataframe['Priority'].unique().tolist() if dataframe['Priority'][dataframe['Priority'] == _class].size/dataframe['Priority'].size > 0.005]
        priority_dataframe = dataframe[dataframe['Priority'].isin(priority_classes_filtered)]
        if dataframe.shape[0] > priority_dataframe.shape[0]:
            priority_dataframe = filter.reindex_data(priority_dataframe)
        priority_dataframe['Priority_ord'] = priority_dataframe['Priority'].astype("category")
        priority_dataframe['Priority_ord_codes'] = pandas.Categorical(priority_dataframe['Priority_ord']).codes
        verify_classes_amount(priority_classes_filtered)
        verify_samples_amount(priority_dataframe, 'Priority_ord_codes')
        # ttr classes
        dataframe['temp_ttr_class'] = pandas.qcut(dataframe['ttr_tr'], bins, labels=ldis, duplicates='drop')
        ttr_classes = [_class for _class in dataframe['temp_ttr_class'].unique().tolist() if dataframe['temp_ttr_class'][dataframe['temp_ttr_class'] == _class].size/dataframe['temp_ttr_class'].size > 0.005]
        ttr_dataframe = dataframe[dataframe['temp_ttr_class'].isin(ttr_classes)]
        if dataframe.shape[0] > ttr_dataframe.shape[0]:
            ttr_dataframe = filter.reindex_data(ttr_dataframe)
        ttr_col_class_tmp = pandas.qcut(ttr_dataframe['ttr_tr'], 4, duplicates='drop').unique()
        verify_classes_amount(ttr_classes)
        verify_samples_amount(ttr_dataframe, 'temp_ttr_class')
        # resolution classes
        resolution_binarized = pandas.get_dummies(dataframe, prefix=list(resolution.keys()), columns=list(resolution.keys()))
        unfiltered_resolutions = unpack_dictionary_val_to_list(resolution)
        filtered_resolutions = [resol for resol in unfiltered_resolutions
                                if resolution_binarized['Resolution_'+resol][resolution_binarized['Resolution_'+resol] == 1].size/resolution_binarized['Resolution_'+resol].size > 0.005]
        verify_classes_amount(filtered_resolutions)
        for resol in filtered_resolutions:
            verify_samples_amount(resolution_binarized, 'Resolution_'+resol)

        # model/ folder cleanup
        remove_models()
        # config file creation
        configuration.create_config('predictions_parameters.ini', section_name='predictions_parameters.ini'.split('.')[0])

        # areas of testing models training
        for area in areas_of_testing_filtered:
            training_imbalance_kf(dataframe['Description_tr'], dataframe[area], session['tfidf'], smt, chi2, 50, svm_imb, secure_filename(area), model_path)
            if log == 1:
                binary_logger.log('{}.log'.format(session.sid), dataframe['Description_tr'], dataframe[area], area, model_path)
        # priority models training
        training_imbalance_kf(priority_dataframe['Description_tr'], 
                              priority_dataframe['Priority_ord_codes'], 
                              session['tfidf'], smt, chi2, 50, svm_imb, 'priority', model_path)
        if log == 1:
            multiple_logger.log('{}.log'.format(session.sid), priority_dataframe['Description_tr'], priority_dataframe['Priority_ord_codes'], 'priority', model_path)
        # ttr models training
        training_imbalance_kf(ttr_dataframe['Description_tr'], ttr_dataframe['temp_ttr_class'], session['tfidf'], smt, chi2, 50, svm_imb, 'ttr', model_path)
        if log == 1:
            multiple_logger.log('{}.log'.format(session.sid), ttr_dataframe['Description_tr'], ttr_dataframe['temp_ttr_class'], 'ttr', model_path)
        # resolution models training
        for resol in filtered_resolutions:
            training_imbalance_kf(resolution_binarized['Description_tr'], resolution_binarized['Resolution_'+resol], session['tfidf'], smt, chi2, 50, svm_imb, secure_filename(resol), model_path)
            configuration.update_setting('predictions_parameters.ini', 'predictions_parameters.ini'.split('.')[0], resol+'_classes', ','.join(['not '+resol, resol]))
        if log == 1:
            binary_logger.log('{}.log'.format(session.sid), resolution_binarized['Description_tr'], resolution_binarized['Resolution_'+resol], secure_filename(resol), model_path)
        
        # updated predictions parameters writing
        configuration.update_setting('predictions_parameters.ini', 
                                     'predictions_parameters.ini'.split('.')[0], 
                                     'binary_classes', ','.join(['0', '1']))
        configuration.update_setting('predictions_parameters.ini', 
                                     'predictions_parameters.ini'.split('.')[0], 
                                     'areas_of_testing', ','.join(areas_of_testing_filtered))
        configuration.update_setting('predictions_parameters.ini',
                                     'predictions_parameters.ini'.split('.')[0], 
                                     'priority_classes', ','.join(priority_dataframe['Priority'].unique().tolist()))
        configuration.update_setting('predictions_parameters.ini',
                                     'predictions_parameters.ini'.split('.')[0], 
                                     'ttr_classes',
                                     ','.join(
                                         [str(is_zero(ttr_col_class_tmp[range(3)[0]].left))+'-'+str(is_zero(ttr_col_class_tmp[range(3)[0]].right))]+
                                         [str(is_zero(ttr_col_class_tmp[el].left+1.0))+'-'+str(is_zero(ttr_col_class_tmp[el].right)) for el in range(1,3)]+
                                         ['>'+str(is_zero(ttr_col_class_tmp[range(3)[-1]].right))]))
        for resol in filtered_resolutions:
            configuration.update_setting('predictions_parameters.ini', 
                                         'predictions_parameters.ini'.split('.')[0], 
                                         resol+'_classes', ','.join(['not '+resol, resol]))
        dataframe.to_pickle(dataframe_path)
    except FileNotFoundError:
        raise


def calculate_top_terms(data, field, func, SW):
        # bidata = pandas.get_dummies(data, prefix=field+'_', columns=field)
        multithreaded = Multithreaded()
        clear_data = ClearData()
        parall_data = multithreaded.parallelize(data['Description_tr'], clear_data.clean_descr)
        tfs = session['tfidf'].fit_transform(parall_data)
        y = data[field]
        selector = SelectKBest(score_func=func, k='all')
        selector.fit_transform(tfs, y)
        X_new = dict(zip(session['tfidf'].get_feature_names(), selector.scores_))
        temp_dict = sorted(X_new.items(), key=lambda x: x[1], reverse=True)
        rez = []
        mean = []
        for el in temp_dict[:]:
            if el[1] > 1:
                rez.append(el)
                mean.append(el[1])
        import numpy
        return [el[0] for el in rez if el[1] > numpy.mean(mean)]

def create_top_terms_file(frame, resolution):
        checker = Checker()
        chi2 = feature_selection.chi2
        SW = text.ENGLISH_STOP_WORDS
        config_reader = SettingProvider('predictions_parameters.ini')
        resol_all = []
        for el in checker.get_resolutions(resolution):
            resol_all += config_reader.get_setting(section='predictions_parameters', setting="{el}_classes".format(el=el), evaluate=False).split(',')
        resol = [el for el in resol_all if 'not' not in el]
        prio = config_reader.get_setting(section='predictions_parameters',
                                         setting='priority_classes', evaluate=False).split(',')

        areas = config_reader.get_setting(section='predictions_parameters',
                                          setting='areas_of_testing', evaluate=False).split(',')
        all_terms = prio + resol + areas
        all_mass = []
        bin_data = pandas.get_dummies(frame, prefix=list(resolution.keys())+['Priority'], columns=list(resolution.keys())+['Priority'])
        top_term = {}
        for el in all_terms:
            if el != "Other_lab":
                if el in prio:
                    top_term[el] = calculate_top_terms(bin_data, 'Priority_'+el, chi2, SW)
                if el in resol:
                    key = None 
                    for key1 in resolution:
                        if isinstance(resolution[key1], list):
                            if el in resolution[key1]:
                                key = key1
                        else:
                            if el == resolution[key1]:
                                key = key1
                    top_term[el] = calculate_top_terms(bin_data, key+'_'+el, chi2, SW)
                if el in areas:
                    top_term[el] = calculate_top_terms(bin_data, el, chi2, SW)
        top_term = pandas.DataFrame(dict([(k, pandas.Series(v)) for k, v in top_term.items()]))
        top_term.to_csv('top_terms.csv', index=False)

