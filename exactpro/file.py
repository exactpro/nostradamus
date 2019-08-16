import os
import pandas


class File:
    def save_file(self, data, file_name, murkup, store, fields):
        if murkup == 0:
            data.to_csv(os.path.join(store, file_name), 
                        columns=list(fields['mandatory_fields'].keys()) + [field for field in fields['special_fields'].keys() if field != 'ttr'], 
                        index=False)
        else:
            try:
                data.to_csv(os.path.join(store, file_name), 
                            columns=list(fields['mandatory_fields'].keys()) + [field for field in fields['special_fields'].keys() if field != 'ttr'] + list(fields['area_of_testing_fields'].keys()),  
                            index=False)
            except Exception as e:
                raise Exception(e)

    def save_multiple_file(self, frame, dict, file_name, store):
        self.new_frame = pandas.DataFrame.from_dict(dict, orient='index')
        self.rename_column_df = self.new_frame.rename(columns={0: 'Description',
                                                               1: 'Priority',
                                                               2: 'TTR',
                                                               3: 'Wont Fix',
                                                               4: 'Reject',
                                                               5: 'Area of testing'})
        self.drop_df = self.rename_column_df.drop('Description', 1)
        self.drop_df['Issue_key'] = self.drop_df.index.tolist()
        self.final_df = pandas.merge(frame, self.drop_df , how='inner', on='Issue_key')
        self.final_df.to_csv(os.path.join(store, file_name),
                             columns=['Issue_key', 'Project_name', 'Description', 'Priority',
                                      'TTR', 'Wont Fix','Reject', 'Area of testing'], 
                             index=False)

    def save_multiple_file1(self, dict, file_name, store):
        # converts list to str for area_of_testing
        for key in dict:
            for key1 in dict[key]:
                if key1 == 'area_of_testing':
                    if isinstance(dict[key][key1], list):
                        dict[key][key1] = ','.join(dict[key][key1])
        self.new_frame = pandas.DataFrame.from_dict(dict, orient='index')
        self.new_frame['Issue_key'] = self.new_frame.index.tolist()
        self.new_frame.to_csv(os.path.join(store, file_name), index=False)


class ReduceFrame:
    def mem_usage(self, pandas_obj):
        if isinstance(pandas_obj, pandas.DataFrame):
            self.usage_b = pandas_obj.memory_usage(deep=True).sum()
        else:
            # if it's not a DataFrame so we consider that as a Series
            self.usage_b = pandas_obj.memory_usage(deep=True)
        self.usage_mb = self.usage_b / 1024  # converts bytes to megabytes
        return "{} kb".format(self.usage_mb)

    def reduce(self, frame):
        self.frame_int = frame.select_dtypes(include=['int'])
        self.frame_converted_int = self.frame_int.apply(pandas.to_numeric, downcast='unsigned')
        self.frame_float = frame.select_dtypes(include=['float'])
        self.frame_converted_float = self.frame_float.apply(pandas.to_numeric, downcast='float')
        self.frame_obj = frame.select_dtypes(include=['object']).copy()
        self.frame_converted_obj = pandas.DataFrame()
        for col in self.frame_obj.columns:
            if len(self.frame_obj[col].unique()) / len(self.frame_obj[col]) < 0.5:
                self.frame_converted_obj.loc[:, col] = self.frame_obj[col].astype('category')
            else:
                self.frame_converted_obj.loc[:, col] = self.frame_obj[col]
        self.optimized_frame = frame.copy()
        self.optimized_frame[self.frame_converted_int.columns] = self.frame_converted_int
        self.optimized_frame[self.frame_converted_float.columns] = self.frame_converted_float
        self.optimized_frame[self.frame_converted_obj.columns] = self.frame_converted_obj
        return self.optimized_frame


# cleans up model/ folder
def remove_models():
    try:
        main_dir = list(os.getcwd().split('/'))[-1:]
        os.chdir('../model/')
        models_dest_dir = os.getcwd()
        models = [ file for file in os.listdir(models_dest_dir) if file.endswith('.sav') ]
        for model in models:
            os.remove(os.path.join(models_dest_dir, model))
        os.chdir('../' + main_dir[0])
    except Exception:
        print('Error: can\'t clean up model/ folder.')

if __name__ == "__main__":
    remove_models()
