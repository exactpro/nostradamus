import numpy
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas
import datetime
import calendar


class RelativeFrequencyChart:
    # returns coordinates for each chart column
    def get_coordinates(self, data, bins): #   bins - chart columns count
        self.btt = numpy.array(list(data))
        self.y, self.x, self.bars = plt.hist(self.btt, weights=numpy.zeros_like(self.btt) + 1. / self.btt.size, bins=bins)
        return self.x, self.y


class FrequencyDensityChart:
    def get_coordinates_histogram(self, data, bins):
        self.btt = numpy.array(list(data))
        self.y, self.x, self.bars = plt.hist(self.btt, bins=bins, density=True)
        return self.x, self.y

    def get_coordinates_line(self, data):
        try:
            self.btt = numpy.array(list(data))
            self.density = stats.kde.gaussian_kde(list(data))
            self.x_den = numpy.linspace(0, data.max(), data.count())
            self.density = self.density(self.x_den)
            return self.x_den, self.density
        except numpy.linalg.linalg.LinAlgError:
            return [-1], [-1]


class DynamicChart:
    def get_coordinates(self, frame, step_size):
        self.plot = {}  # chart coordinates
        self.dynamic_bugs = []
        self.x = []
        self.y = []
        self.plot['period'] = step_size
        if step_size == 'W-SUN':
            self.periods = DynamicChart.get_periods(self, frame, step_size) # separates DataFrame to the specified periods
            if len(self.periods) == 0:
                return 'error'
            self.cumulative = 0 # cumulative total of defect submission for specific period
            for self.period in self.periods:
                # checks whether the first day of period is Monday (if not then we change first day to Monday)
                if pandas.to_datetime(self.period[0]) < pandas.to_datetime(frame['Created_tr']).min():
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >=
                                          pandas.to_datetime(frame['Created_tr']).min()) &
                                          (pandas.to_datetime(frame['Created_tr']) <= pandas.to_datetime(self.period[1]))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                    self.x.append(str(datetime.datetime.date(pandas.to_datetime(frame['Created_tr'], format='%Y-%m-%d').min())))
                    self.y.append(self.cumulative)
                else:
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(self.period[0]))
                                          & (pandas.to_datetime(frame['Created_tr']) <= pandas.to_datetime(self.period[1]))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                    self.x.append(str((self.period[0])))
                    self.y.append(self.cumulative)
            
            # check whether the date from new DataFrame is greater than date which is specified in settings 
            if pandas.to_datetime(frame['Created_tr']).max() > pandas.to_datetime(self.periods[-1][1]):
                # processing of days which are out of full period set
                self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) > pandas.to_datetime(self.periods[-1][1]))
                                      & (pandas.to_datetime(frame['Created_tr']) <=
                                      pandas.to_datetime(frame['Created_tr']).max())]
                self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                self.x.append(str(datetime.datetime.date(pandas.to_datetime(self.periods[-1][1], format='%Y-%m-%d')) + datetime.timedelta(days=1)))
                self.y.append(self.cumulative)
            self.dynamic_bugs.append(self.x)
            self.dynamic_bugs.append(self.y)
            self.plot['dynamic bugs'] = self.dynamic_bugs
            self.cumulative = 0
            return self.plot
        if step_size in ['7D', '10D', '3M', '6M', 'A-DEC']:
            self.count0 = 0
            self.count1 = 1
            self.periods = DynamicChart.get_periods(self, frame, step_size) # DataFrame separation by the specified periods
            if len(self.periods) == 0:
                return 'error'
            self.cumulative = 0
            self.countPeriodsList = len(self.periods) # calculated periods count
            self.count = 1
            if self.countPeriodsList == 1:
                if step_size == '7D':
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >=
                                          pandas.to_datetime(frame['Created_tr']).min())
                                          & (pandas.to_datetime(frame['Created_tr'])
                                          < pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())
                                                             +datetime.timedelta(days=7)))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key'].count())
                    self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr'], format='%Y-%m-%d').min()), step_size)))
                    self.y.append(self.cumulative)
                    if pandas.to_datetime(frame['Created_tr']).max() > pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())+datetime.timedelta(days=7)):
                        self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >=
                                              pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())+
                                              datetime.timedelta(days=7))) & (pandas.to_datetime(frame['Created_tr'])
                                                                                             <= pandas.to_datetime(frame['Created_tr']).max())]
                        self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                        self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())+datetime.timedelta(days=7), step_size)))
                        self.y.append(self.cumulative)
                    self.cumulative = 0
                if step_size == '10D':
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(frame['Created_tr']).min()) & (pandas.to_datetime(frame['Created_tr']) < pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())+datetime.timedelta(days=10)))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                    self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr'], format='%Y-%m-%d').min()), step_size)))
                    self.y.append(self.cumulative)
                    if pandas.to_datetime(frame['Created_tr']).max() > pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())+datetime.timedelta(days=10)):
                        self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())+datetime.timedelta(days=10))) & (pandas.to_datetime(frame['Created_tr']) <= pandas.to_datetime(frame['Created_tr']).max())]
                        self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                        self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min())+datetime.timedelta(days=10), step_size)))
                        self.y.append(self.cumulative)
                    self.cumulative = 0
                if step_size == '3M':
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(frame['Created_tr']).min())
                                          & (pandas.to_datetime(frame['Created_tr']) <
                                          pandas.to_datetime(DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 3)))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key'].count())
                    self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr'], format='%Y-%m-%d').min()), step_size)))
                    self.y.append(self.cumulative)
                    if pandas.to_datetime(frame['Created_tr']).max() > pandas.to_datetime(DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 3)):
                        self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 3))) & (pandas.to_datetime(frame['Created_tr']) <= pandas.to_datetime(frame['Created_tr']).max())]
                        self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                        self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 3), step_size)))
                        self.y.append(self.cumulative)
                    self.cumulative = 0
                if step_size == '6M':
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(frame['Created_tr']).min())
                                          & (pandas.to_datetime(frame['Created_tr']) <
                                          pandas.to_datetime(DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 6)))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                    self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr'], format='%Y-%m-%d').min()), step_size)))
                    self.y.append(self.cumulative)
                    if pandas.to_datetime(frame['Created_tr']).max() > pandas.to_datetime(DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 6)):
                        self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 6))) & (pandas.to_datetime(frame['Created_tr']) <= pandas.to_datetime(frame['Created_tr']).max())]
                        self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                        self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, DynamicChart.add_months(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr']).min()), 6), step_size)))
                        self.y.append(self.cumulative)
                    self.cumulative = 0
                if step_size == 'A-DEC':
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(frame['Created_tr']).min())
                                          & (pandas.to_datetime(frame['Created_tr']) < pandas.to_datetime(str(int(self.periods[0])+1)))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                    self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(frame['Created_tr'], format='%Y-%m-%d').min()), step_size)))
                    self.y.append(self.cumulative)
                    if(pandas.to_datetime(frame['Created_tr']).max() > pandas.to_datetime(str(int(self.periods[0])+1))):
                        self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(str(int(self.periods[0])+1)))
                                         & (pandas.to_datetime(frame['Created_tr']) <= pandas.to_datetime(frame['Created_tr']).max())]
                        self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                        self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(str(int(self.periods[0])+1))), step_size)))
                        self.y.append(self.cumulative)
                    self.cumulative = 0
            else:
                while self.count < self.countPeriodsList:
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(self.periods[self.count0])) &
                                          (pandas.to_datetime(frame['Created_tr']) < pandas.to_datetime(self.periods[self.count1]))]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                    self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(self.periods[self.count0], format='%Y-%m-%d')), step_size)))
                    self.y.append(self.cumulative)
                    self.count0 = self.count0 + 1
                    self.count1 = self.count1 + 1
                    self.count = self.count + 1
                if pandas.to_datetime(frame['Created_tr']).max() >= pandas.to_datetime(self.periods[-1]):
                    self.newFrame = frame[(pandas.to_datetime(frame['Created_tr']) >= pandas.to_datetime(self.periods[-1])) &
                                     (pandas.to_datetime(frame['Created_tr']) <= pandas.to_datetime(frame['Created_tr']).max())]
                    self.cumulative = self.cumulative + int(self.newFrame['Issue_key_tr'].count())
                    self.x.append(str(DynamicChart.get_date_for_dynamic_my(self, datetime.datetime.date(pandas.to_datetime(self.periods[-1], format='%Y-%m-%d')), step_size)))
                    self.y.append(self.cumulative)
                self.cumulative = 0
            self.dynamic_bugs.append(self.x)
            self.dynamic_bugs.append(self.y)
            self.plot['dynamic bugs'] = self.dynamic_bugs
            return self.plot

    # DataFrame separation (by periods)
    def get_periods(self, frame, period):
        self.periods = []
        self.periodsFrame = pandas.period_range(start=pandas.to_datetime(frame['Created_tr']).min(), end=pandas.to_datetime(frame['Created_tr']).max(), freq=period)
        if period == 'W-SUN':
            for period in self.periodsFrame:
                self.periods.append(str(period).split('/'))
        if period in ['7D', '10D', '3M', '6M', 'A-DEC']:
            for period in self.periodsFrame:
                self.periods.append(str(period))
        return self.periods

    def get_date_for_dynamic_my(self, date, step_size):
        if date == None:
            return ''
        if step_size == '10D':
            self.day = date.day.__str__()
            self.month = date.month.__str__()
            if date.day.__str__().__len__() == 1:
                self.day = '0' + self.day
            if date.month.__str__().__len__() == 1:
                self.month = '0' + self.month
            self.date = self.day + '-' + self.month + '-' + date.year.__str__()
            return self.date
        if step_size in ['3M', '6M']:
            self.month = date.month.__str__()
            if date.month.__str__().__len__() == 1:
                self.month = '0' + self.month
            self.date = date.year.__str__() + '-' + self.month
            return self.date
        if step_size == 'A-DEC':
            return date.year.__str__()

    def add_months(self, source_date, months):
        self.month = source_date.month - 1 + months
        self.year = source_date.year + self.month // 12
        self.month = self.month % 12 + 1
        self.day = min(source_date.day, calendar.monthrange(self.year, self.month)[1])
        return self.year.__str__() + '-' + self.month.__str__()


class PlotChart:
    def prepare_data(self, data, x='ttr', y='Relative Frequency', scale='', step_size='', period='W-SUN'):
        self.rez_dict = {}
        self.val_dict = {}
        if y == 'Relative Frequency':
            # rel_freq0 - X axis, rel_freq1 - Y axis
            self.rel_freq0, self.rel_freq1 = RelativeFrequencyChart.get_coordinates(self,data[x].dropna().apply(int), 10)
            self.rez_dict['Relative Frequency'] = [list(self.rel_freq0), list(self.rel_freq1)+[float(0)]]

            self.rez_dict['scale'] = scale
            self.rez_dict['stepSize'] = step_size
            self.val_dict['x'] = x
            self.val_dict['y'] = y
            self.rez_dict['fieldsVal'] = self.val_dict
            return self.rez_dict
        if y == 'Frequency density':
            self.hist0, self.hist1 = FrequencyDensityChart.get_coordinates_histogram(self, data[x].dropna().apply(int), 'fd')
            self.line0, self.line1 = FrequencyDensityChart.get_coordinates_line(self, data[x].dropna().apply(int))
            self.rez_dict['Frequency density'] = {'histogram': [list(self.hist0), list(self.hist1)+[float(0)]],
                                                  'line': [list(self.line0), list(self.line1)]}
            self.rez_dict['scale'] = scale
            self.rez_dict['stepSize'] = step_size
            self.val_dict['x'] = x
            self.val_dict['y'] = y
            self.rez_dict['fieldsVal'] = self.val_dict
            return self.rez_dict
        if y == 'Dynamic':
            return DynamicChart.get_coordinates(self, data, period)

    def combine_charts(self, chart1, chart2):
        chart1['dynamic bugs'] = chart2
        return chart1

    def parse_period(self, period):
        if period == '1 week':
            return 'W-SUN'
        if period == '10 days':
            return '10D'
        if period == '3 months':
            return '3M'
        if period == '6 months':
            return '6M'
        if period == '1 year':
            return 'A-DEC'

    def check_scale_step(self, scale, step_size, x, stat_info):
        if scale == '' and step_size == '':
            return True
        elif scale != '' and step_size == '':
            try:
                return PlotChart.validate_step_scale(self, float(scale), x, stat_info)
            except ValueError:
                raise
        elif step_size != '' and scale == '':
            try:
                return PlotChart.validate_step_scale(self, float(step_size), x, stat_info)
            except ValueError:
                raise
        elif scale != '' and step_size != '':
            try:
                return PlotChart.validate_step_scale(self, float(scale), x, stat_info) and \
                       PlotChart.validate_step_scale(self, float(step_size), x, stat_info)
            except ValueError:
                raise
        else:
            return False

    def validate_step_scale(self, param, x, statInfo):
        if x == 'ttr' and param >= 0 and param <= float(statInfo['ttrStat']['max']):
            return True
        if x == 'Comments' and param >= 0 and param <= float(statInfo['commentStat']['max']):
            return True
        if x == 'Attachments' and param >= 0 and param <= float(statInfo['attachmentStat']['max']):
            return True
        return False


class MultupleChart:
    def data_for_multiple_plot(self, _dict, charts):
        self.rez = {key: {} for key in _dict[list(_dict.keys())[0]].keys() if key in charts}
        for el in _dict:
            for el1 in _dict[el]:
                if el1 in charts:
                    if isinstance(_dict[el][el1], list):
                        for el2 in _dict[el][el1]:
                            if el2 not in self.rez[el1].keys():
                                self.rez[el1][el2] = 1
                            else:
                                self.rez[el1][el2] += 1
                    else:
                        if _dict[el][el1] not in self.rez[el1].keys():
                            self.rez[el1][_dict[el][el1]] = 1
                        else:
                            self.rez[el1][_dict[el][el1]] += 1
        for el in self.rez:
            for el1 in self.rez[el]:
                self.rez[el][el1] = round((self.rez[el][el1]*100)/len(_dict), 3)
        return self.rez