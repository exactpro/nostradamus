from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction import text
from collections import OrderedDict
from exactpro.cleaner import ClearData
from exactpro.my_multithread import Multithreaded
from sklearn import feature_selection
from sklearn.feature_selection import SelectKBest
import pandas
from pathlib import Path
from exactpro.model import Model
from exactpro.config_parser import SettingProvider
from exactpro.model import Insert
from exactpro.xml_parser import clean_description
from werkzeug.utils import secure_filename
from flask import session


# calculation of:
# THE TOP OF THE MOST FREQUENTLY USED TERMS
# THE TOP OF THE MOST SIGNIFICANT TERMS
# STAT INFO
class StatInfo:
    # STAT INFO info calculation
    def get_statInfo(self, data, orig_data):
        try:
            # data type convertion for correct stat processing
            comments_ser = data['Comments'].apply(float)
            attachments_ser = data['Attachments'].apply(float)
            return {'total': str(orig_data['Issue_key'].count()),
                    'filtered': str(data['Issue_key'].count()),
                    'commentStat': {'max': str(comments_ser.max()),  
                                    'min': str(comments_ser.min()),
                                    'mean': str(round(comments_ser.mean(), 3)),
                                    'std': str(round(comments_ser.std(), 3))
                                    },
                    'attachmentStat': {
                        'max': str(attachments_ser.max()),
                        'min': str(attachments_ser.min()),
                        'mean': str(round(attachments_ser.mean(), 3)),
                        'std': str(round(attachments_ser.std(), 3))
                        },
                    'ttrStat': {
                        'max': str(data['ttr'].max()),
                        'min': str(data['ttr'].min()),
                        'mean': str(round(data['ttr'].mean(), 3)),
                        'std': str(round(data['ttr'].std(), 3))
                        }
                    }
        except KeyError:
            raise

    # THE TOP OF THE MOST FREQUENTLY USED TERMS info calculation
    def friquency_stat(self, data, sw=text.ENGLISH_STOP_WORDS):
        try:
            self.multithreaded = Multithreaded()
            self.clear_data = ClearData()
            # description cleaning
            self.parall_data = self.multithreaded.parallelize(data['Description_tr'], self.clear_data.clean_descr)
            
            tfs = session['tfidf'].fit_transform(self.parall_data)

            # train_bug = tfs.todense()  # use it for sparse matrix
            self.idf = session['tfidf'].idf_

            # words coefficient
            self.voc_feat = dict(zip(session['tfidf'].get_feature_names(), self.idf))
            self.voc_feat_s = OrderedDict((k, v) for k, v in sorted(self.voc_feat.items(), key=lambda x: x[1], reverse=True))
            
            return list(self.voc_feat_s.keys())[:100]   # returns the first 100 words from the calculated list
        except Exception as e:
            raise Exception(str(e))

    def top_terms(self, data, metric, field, sw=text.ENGLISH_STOP_WORDS):
        try:
            chi2 = feature_selection.chi2
            self.bidata = pandas.get_dummies(data, prefix=[field], columns=[field]) # data binarisation
            
            self.multithreaded = Multithreaded()
            self.clear_data = ClearData()
            self.parall_data = self.multithreaded.parallelize(self.bidata['Description_tr'], self.clear_data.clean_descr)

            self.tfs = session['tfidf'].fit_transform(self.parall_data)

            self.y = self.bidata[metric]
            self.selector = SelectKBest(score_func=chi2, k='all')  # select the most significant terms
            self.selector.fit_transform(self.tfs, self.y)
            self.X_new = dict(zip(session['tfidf'].get_feature_names(), self.selector.scores_))
            self.temp_dict = OrderedDict((k, v) for k, v in sorted(self.X_new.items(), key=lambda x: x[1], reverse=True))
            return list(self.temp_dict.keys())[:20]
        except Exception as e:
            raise Exception(str(e))

    def get_topPriority(self, frame, field, sw):
        if field.split()[0] == 'Priority':
            return StatInfo.top_terms(self,
                                      frame,
                                      'Priority_' + ' '.join(e for e in field.split()[1:]),
                                      'Priority',
                                      sw)
        if field.split()[0] == 'Resolution':
            return StatInfo.top_terms(self,
                                      frame,
                                      'Resolution_' + ' '.join(e for e in field.split()[1:]),
                                      'Resolution',
                                      sw)

    # saving of finished calculations for significance top
    # reason: building the top of terms is too resource-consuming task
    def save_significanceTop(self, data, reference_to, significance_top, sw=text.ENGLISH_STOP_WORDS):
        if reference_to in significance_top.keys():
            return significance_top[reference_to]
        else:
            significance_top[reference_to] = StatInfo.get_topPriority(self, data, reference_to, sw)
            return significance_top[reference_to]

    def max_data(self, frame, fields, resolution):
        try:
            self.count = 0
            self.model = Model()
            self.setting_provader = SettingProvider('predictions_parameters.ini')
            self.insert = Insert()
            self.dictionary = {}
            while self.count < frame.shape[0]:
                self.my_list = {}
                self.my_list['Summary'] = (frame['Summary'][self.count])
                self.my_list['Priority'] = (frame['Priority'][self.count])
                text_descr = clean_description(frame['Description'][self.count])
                self.ttr = self.model.proc_text(text_descr,
                                                self.setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                  'ttr_classes', False).split(','),
                                                'ttr',
                                                str(Path(__file__).parents[2])+'/model/')

                self.my_list['ttr'] = (max(self.ttr, key=self.ttr.get))
                for el in resolution:
                    self.rez = self.model.proc_text(text_descr,
                                                    self.setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                      el+'_classes', False).split(','),
                                                    secure_filename(el),
                                                    str(Path(__file__).parents[2])+'/model/')

                    self.my_list[el] = (max(self.rez, key=self.rez.get))
                self.area_prob = {}
                for area in fields:
                    self.tmp = self.model.proc_text(text_descr,
                                                    self.setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                      'binary_classes', False).split(','),
                                                    secure_filename(area),
                                                    str(Path(__file__).parents[2])+'/model/')
                    self.area_prob.update({area: float(self.tmp['1'])})

                self.my_list['area_of_testing'] = [k for k, v in self.area_prob.items() if v > 0.5] if [k for k, v in self.area_prob.items() if v > 0.5] else 'no idea'
                self.dictionary[frame['Issue_key'][self.count]] = self.my_list
                self.count = self.count + 1
            return self.dictionary
        except FileNotFoundError:
            raise
        except Exception:
            raise

    def mean_std_data(self, frame, fields, resolution):
        try:
            self.count = 0
            self.model = Model()
            self.setting_provader = SettingProvider('predictions_parameters.ini')
            self.resolution_fin = {el: {el: [], 'not_'+el: []} for el in resolution}
            self.ttr_fin = {k: [] for k in self.setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                             'ttr_classes', False).split(',')}
            self.area_fin = {field: [] for field in fields}

            while self.count < frame.shape[0]:

                    text_descr = clean_description(frame['Description'][self.count])

                    self.ttr = self.model.proc_text(text_descr,
                                                    self.setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                      'ttr_classes', False).split(','),
                                                    'ttr',
                                                    str(Path(__file__).parents[2])+'/model/')
                    for key in self.ttr_fin:
                        self.ttr_fin[key].append(self.ttr[key])

                    for el in resolution:
                        self.rez = self.model.proc_text(text_descr,
                                                        ['not_'+el, el],
                                                        el,
                                                        str(Path(__file__).parents[2])+'/model/')
                        self.resolution_fin[el][el].append(self.rez[el])
                        self.resolution_fin[el]['not_'+el].append(self.rez['not_'+el])
                    for area in fields:
                        self.tmp = self.model.proc_text(text_descr,
                                                        self.setting_provader.get_setting('predictions_parameters.ini'.split('.')[0],
                                                                                          'binary_classes', False).split(','),
                                                        area,
                                                        str(Path(__file__).parents[2])+'/model/')
                        self.area_fin[area].append(float(self.tmp['1']))

                    self.count = self.count + 1
            StatInfo.print_mean_std(self, self.resolution_fin)
            StatInfo.print_mean_std(self, self.ttr_fin)
            StatInfo.print_mean_std(self, self.area_fin)
        except FileNotFoundError:
            raise
        except Exception:
            raise

    def print_mean_std(self, obj):
        import numpy
        for el in obj:
            if isinstance(obj[el], list):
                print(el+'\nmean: '+str(numpy.mean(obj[el]))+'\n'+'std: '+str(numpy.std(obj[el])))
            elif isinstance(obj[el], dict):
                StatInfo.print_mean_std(self, obj[el])
            else:
                print(el+'\nfor {} only one value'.format(el))

