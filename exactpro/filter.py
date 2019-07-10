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


import re
import os
import shutil
import pandas
from decimal import Decimal
from exactpro.data_checker import Checker


# DataFrame filtration (GUI section: ATTRIBUTES LIST FILTRATION)
class Filter:
    # key - field name from GUI
    # value - field value from GUI
    # data - DataFrame
    # fields - fields from config file (manadatory/special fields)
    # store - path where DataFrames will be stored (using pickle)
    def filtration(self, key, value, data, fields, store):
        # categorical fields processing
        if key in [el for group in fields for el in fields[group] if
                   fields[group][el]['type'] == 'categorical']:
            # link to the new filtered DataFrame
            self.newData = data[data[key].isin(value.split(',')) == True]
            if data.shape[0] > self.newData.shape[0]: 
                Filter.reindex_data(self, self.newData).to_pickle(store) # reindex DataFrame (shape[0] is DataFrame's elements count)
            else:
                self.newData.to_pickle(store)
        # bool fields processing
        if key in [el for group in fields for el in fields[group] if
                   fields[group][el]['type'] == 'bool']:
            self.newData = data[data[key].apply(bool) == value]
            if data.shape[0] > self.newData.shape[0]:
                Filter.reindex_data(self, self.newData).to_pickle(store)
            else:
                self.newData.to_pickle(store)
        # text fields processing (full matching search)
        if key in [el for group in fields for el in fields[group] if
                   fields[group][el]['type'] == 'text']:
            self.newData = data[data[key+'_tr'].str.lower() == value.lower()]
            if data.shape[0] > self.newData.shape[0]:
                Filter.reindex_data(self, self.newData).to_pickle(store)
            else:
                self.newData.to_pickle(store)
        # text1 fields processing (substring search)
        if key in [el for group in fields for el in fields[group] if
                   fields[group][el]['type'] == 'text1']:
            self.newData = data[data[key+'_tr'].str.replace(r'\n', ' ').str.replace(' ', '').
                               str.contains(value.replace(r'\n', ' ').replace(' ', ''),
                                            case=False, na=False, regex=False) == True] 
            if data.shape[0] > self.newData.shape[0]:
                Filter.reindex_data(self, self.newData).to_pickle(store)
            else:
                self.newData.to_pickle(store)
        # text2 fields processing (search of subsets inside substring)
        if key in [el for group in fields for el in fields[group] if
                   fields[group][el]['type'] == 'text2']:
            self.newData = data
            self.newData[key+'_tr'] = self.newData[key+'_tr'].astype(str)
            for pattern in value.split(','):
                self.newData = Filter.my_contains(self, self.newData, key+'_tr', pattern.lower().strip())
            if data.shape[0] > self.newData.shape[0]:
                Filter.reindex_data(self, self.newData).to_pickle(store)
            else:
                self.newData.to_pickle(store)
        # number fields processing
        if key[:-1] in [el for group in fields for el in fields[group] if
                        fields[group][el]['type'] == 'number']:
            data[key[:-1]+'_tr'] = data[key[:-1]].apply(Decimal)
            if '0' in key:
                self.newData = data[data[key[:-1]+'_tr'] >= value]
            if '1' in key:
                self.newData = data[data[key[:-1]+'_tr'] <= value]
            if data.shape[0] > self.newData.shape[0]:
                Filter.reindex_data(self, self.newData).to_pickle(store)
            else:
                self.newData.to_pickle(store)
        # date fields processing
        if key[:-1] in [el for group in fields for el in fields[group] if
                        fields[group][el]['type'] == 'date']:
            if key[:-1] == 'Resolved':
                if '0' in key:
                    self.newData = data[data[key[:-1]+'_td_tr'] >= value]
                if '1' in key:
                    self.newData = data[data[key[:-1]+'_td_tr'] <= value]
            else:
                if '0' in key:
                    self.newData = data[data[key[:-1] + '_tr'] >= value]
                if '1' in key:
                    self.newData = data[data[key[:-1] + '_tr'] <= value]
            if data.shape[0] > self.newData.shape[0]:
                Filter.reindex_data(self, self.newData).to_pickle(store)
            else:
                self.newData.to_pickle(store)

    def my_contains(self, df, field, pattern):
        self.find = Filter()
        self.newDf = df[df[field].str.replace(r'\n', ' ').apply(self.find.find, args=(pattern,)) == True]
        return self.newDf[self.newDf[field].str.contains(pattern, case=False, na=False, regex=False) == True]

    def find(self, value, pattern):
        self.pattern = re.compile(r'\b' + re.sub(r'[%;"\\.^:\/$​–•\|!#<~&@>*\-+=◾\'\?╙“”‘’]*', '', pattern) + r'\b')
        if re.findall(self.pattern, re.sub(r'[%;"\\.^:\/$​–•\|!#<~&@>*\-+=◾\'\?╙“”‘’]*', '', value)):
            return True
        else:
            return False

    def drop_filter(self, store):
        checker = Checker()
        os.remove(os.path.abspath(os.curdir)+'/'+store['newData'])
        shutil.copy(os.path.abspath(os.curdir)+'/'+store['origFrame'], os.path.abspath(os.curdir)+'/'+store['newData'])

    def reindex_data(self, data):
        if 'index' in list(data):
            newData_reindex = data.reset_index(drop=True)
        else:
            newData_reindex = data.reset_index()
        newData_reindex.drop(columns=['index'])
        return newData_reindex

