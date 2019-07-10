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
import csv


class ClearData:
    # description field cleanup
    def clean_descr(self, data):
        try:
            # list of compiled regular expressions from the regularExpression.csv file
            self.remove_pat = [re.compile(el1) for el in csv.reader(open('regularExpression.csv'), delimiter=',', quotechar='"') for el1 in el if el1]
        except FileNotFoundError as e:
            raise Exception(str(e))
        clear = ClearData()
        return data.apply(clear.defaults_clean_for_top, args=(self.remove_pat,)).fillna(value='aftercleaning') # changes NaN fields to 'aftercleaning'
 
    def defaults_clean_for_top(self, text, remove_pat):
        if text is None:
            return None
        else:
            self.test_clean = text
            for self.el in remove_pat:
                self.test_clean = re.sub(self.el, ' ', self.test_clean)
            return self.test_clean

