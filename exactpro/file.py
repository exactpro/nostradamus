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


import os
import pandas
import shutil


class File:
    def save_file(self, data, file_name, murkup, store, fields):
        if murkup == 0:
            data.to_csv(os.path.join(store, file_name), columns=list(fields['mandatory_fields'].keys()) + [field for field in fields['special_fields'].keys() if field != 'ttr'], index=False)
        else:
            try:
                data.to_csv(os.path.join(store, file_name), columns=list(fields['mandatory_fields'].keys()) + list(fields['special_fields'].keys()) + list(fields['areas_fields'].keys()), index=False)
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
                             columns=['Issue_key', 'Project_name', 'Description', 'Priority', 'TTR', 'Wont Fix',
                                      'Reject', 'Area of testing'], index=False)

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
            # we assume if not a df it's a series
            self.usage_b = pandas_obj.memory_usage(deep=True)
        self.usage_mb = self.usage_b / 1024  # convert bytes to megabytes
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


# creates a backup of single_mod.ini and all existing models
def backup_models():
    config_bckp_folder = '/backup/configs/'
    model_bckp_folder = '/backup/model/'
    acc_rights = 0o777
    main_path = os.getcwd()
    file_copier = shutil.copyfile
    try:
        if not os.path.exists(main_path + '/backup/'):
            os.makedirs(name=main_path+config_bckp_folder, mode=acc_rights) # backup folder creation for config files
            os.makedirs(name=main_path+model_bckp_folder, mode=acc_rights) # backup folder creation for models
        file_copier('single_mod.ini', main_path + '/backup/configs/single_mod.ini')
        os.chdir('../model/')
        curr_dir = os.getcwd()
        models = os.listdir(curr_dir)
        for model in models:
            file_copier(model, main_path + model_bckp_folder + model)
        os.chdir('../nostradamus/')

    except OSError as e:  
        print("Creation of the directory %s failed" + str(e))
    except Exception:
        print('Error occured while file copying process')


# removes backup folder
def remove_backup():
    bckp_path = os.getcwd() + '/backup'
    shutil.rmtree(path=bckp_path)


# rolls back changes in single_mod.ini and models
def roll_back_models():
    config_bckp_folder = '/backup/configs/'
    model_bckp_folder = '/backup/model/'
    main_path = os.getcwd()
    file_copier = shutil.copyfile
    try:
        file_copier(main_path + config_bckp_folder + 'single_mod.ini', main_path + '/single_mod.ini') # getting back source config file
        
        os.chdir('../model/')
        models_dest_dir = os.getcwd()
        shutil.rmtree(path=models_dest_dir)
        shutil.copytree(main_path + model_bckp_folder, models_dest_dir) # get back source models
        os.chdir('../nostradamus/')
    except OSError as e:  
        print("Creation of the directory %s failed" + str(e))
    except Exception:
        print('Error occured while file copying process')

