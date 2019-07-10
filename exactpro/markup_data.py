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


import pandas


class Markup:
    # data - DataFrame   
    # list_pat - compiled regular expressions list
    # list_aot - areas of testing list
    # colname - field name which stores binarised data (pattern: fieldname + '_lab')
    # field - searching component
    def collabels(self, data, list_pat, list_aot, colname, field):
        data[list_aot+colname] = data[field].str.contains(list_pat.strip(), case=False, na=False, regex=True).astype(int)
        return data

    def other_lab(self, frame, columns):
        self.other = pandas.Series([])
        # use frame.index to get number of rows for frame
        for self.count in range(len(frame.index)):
            self.other[self.count] = 1
            for self.column in columns:
                if frame[self.column].iloc[self.count] == 1:
                    self.other[self.count] = 0
                    break
        return self.other

