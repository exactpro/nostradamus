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
from werkzeug.utils import secure_filename
from exactpro.model import Model
from exactpro.config_parser import SettingProvider
from exactpro.model import Insert


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
            self.tfidf = StemmedTfidfVectorizer(norm='l2',
                                                sublinear_tf=True,
                                                min_df=1,
                                                stop_words=sw,
                                                analyzer='word',
                                                max_features=1000)

            
            self.multithreaded = Multithreaded()
            self.clear_data = ClearData()
            # description cleaning
            self.parall_data = self.multithreaded.parallelize(data['Description_tr'], self.clear_data.clean_descr)
            
            tfs = self.tfidf.fit_transform(self.parall_data)

            # train_bug = tfs.todense()  # use it for sparse matrix
            self.idf = self.tfidf.idf_

            # words coefficient
            self.voc_feat = dict(zip(self.tfidf.get_feature_names(), self.idf))
            self.voc_feat_s = OrderedDict((k, v) for k, v in sorted(self.voc_feat.items(), key=lambda x: x[1], reverse=True))
            return list(self.voc_feat_s.keys())[:100]   # returns the first 100 words from the calculated list
        except Exception as e:
            raise Exception(str(e))

    def top_terms(self, data, metric, field, sw=text.ENGLISH_STOP_WORDS):
        try:
            chi2 = feature_selection.chi2
            tfidf = StemmedTfidfVectorizer(norm='l2',
                                           sublinear_tf=True,
                                           min_df=1,
                                           stop_words=sw,
                                           analyzer='word',
                                           max_features=1000)
            # StemmedTfidfVectorizer(norm='l2', sublinear_tf=True, min_df=1, stop_words=SW, analyzer='word', max_features = 1000, ngram_range=(2, 3))  # stemming + bigram
            # TfidfVectorizer(tokenizer=LemmaTokenizer(), norm='l2',sublinear_tf=True, min_df=10, max_df=0.5,stop_words=SW, analyzer='word', ngram_range=(2, 3))  # lemmatization + bigram
            # TfidfVectorizer(tokenizer=LemmaTokenizer(), norm='l2', sublinear_tf=True, min_df=10, max_df=0.5, stop_words=SW, analyzer='word')  # lemmatization
            # StemmedTfidfVectorizer(norm='l2', sublinear_tf=True, min_df=1, stop_words=SW, analyzer='word', max_features = 1000)  # stemming with additional settings
            # StemmedTfidfVectorizer(norm='l2', stop_words=SW, analyzer='word')  # stemming
            self.bidata = pandas.get_dummies(data, prefix=[field], columns=[field]) # data binarisation
            
            self.multithreaded = Multithreaded()
            self.clear_data = ClearData()
            self.parall_data = self.multithreaded.parallelize(self.bidata['Description_tr'], self.clear_data.clean_descr)

            self.tfs = tfidf.fit_transform(self.parall_data)

            self.y = self.bidata[metric]
            self.selector = SelectKBest(score_func=chi2, k='all')  # select the most significant terms
            self.selector.fit_transform(self.tfs, self.y)
            self.X_new = dict(zip(tfidf.get_feature_names(), self.selector.scores_))
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
            self.setting_provader = SettingProvider('single_mod.ini')
            self.insert = Insert()
            self.dictionary = {}
            while self.count < frame.shape[0]:
                self.my_list = {}
                self.my_list['Summary'] = (frame['Summary'][self.count])
                self.my_list['Priority'] = (frame['Priority'][self.count])

                self.ttr = self.model.proc_text(frame['Description'][self.count],
                                                self.setting_provader.get_setting('single_mod.ini'.split('.')[0], 'ttr_col_class', False).split(','),
                                                'ttr',
                                                 str(Path(__file__).parents[2])+'/model/')

                self.my_list['ttr'] = (max(self.ttr, key=self.ttr.get))
                for el in resolution:
                    self.rez = self.model.proc_text(frame['Description'][self.count],
                                                    self.setting_provader.get_setting('single_mod.ini'.split('.')[0], el+'_col_class', False).split(','),
                                                    secure_filename(el),
                                                    str(Path(__file__).parents[2])+'/model/')

                    self.my_list[el] = (max(self.rez, key=self.rez.get))
                self.area_prob = {}
                for area in fields:
                    self.tmp = self.model.proc_text(frame['Description'][self.count],
                                                    self.setting_provader.get_setting('single_mod.ini'.split('.')[0], 'binary_col_class', False).split(','),
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
            self.setting_provader = SettingProvider('single_mod.ini')
            self.resolution_fin = {el: {el: [], 'not_'+el: []} for el in resolution}
            self.ttr_fin = {k: [] for k in self.setting_provader.get_setting('single_mod.ini'.split('.')[0], 'ttr_col_class', False).split(',')}
            self.area_fin = {field: [] for field in fields}

            while self.count < frame.shape[0]:

                    self.ttr = self.model.proc_text(frame['Description'][self.count],
                                                    self.setting_provader.get_setting('single_mod.ini'.split('.')[0], 'ttr_col_class', False).split(','),
                                                    'ttr',
                                                    str(Path(__file__).parents[2])+'/model/')
                    for key in self.ttr_fin:
                        self.ttr_fin[key].append(self.ttr[key])

                    for el in resolution:
                        self.rez = self.model.proc_text(frame['Description'][self.count],
                                                        ['not_'+el, el],
                                                        el,
                                                        str(Path(__file__).parents[2])+'/model/')
                        self.resolution_fin[el][el].append(self.rez[el])
                        self.resolution_fin[el]['not_'+el].append(self.rez['not_'+el])
                    for area in fields:
                        self.tmp = self.model.proc_text(frame['Description'][self.count],
                                                        self.setting_provader.get_setting('single_mod.ini'.split('.')[0], 'binary_col_class', False).split(','),
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


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: (SnowballStemmer("english").stem(w) for w in analyzer(doc))