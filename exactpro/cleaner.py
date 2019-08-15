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
        return data.apply(clear.defaults_clean_for_top, args=(self.remove_pat,)).fillna(value='aftercleaning') # NaN --> 'aftercleaning'
 
    def defaults_clean_for_top(self, text, remove_pat):
        if text is None:
            return None
        else:
            self.test_clean = text
            for self.el in remove_pat:
                self.test_clean = re.sub(self.el, ' ', self.test_clean)
            return self.test_clean