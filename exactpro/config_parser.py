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


import configparser
import os


class SettingProvider:
    def __init__(self, config_name):
        # checks whether the ini-file exists
        if not os.path.exists(config_name):
            raise FileNotFoundError('not find {}'.format(config_name))
        else:
            self.config_name = config_name
            self.config = configparser.ConfigParser()
            self.config.read(self.config_name)
    
    # returns config parameter value
    def get_setting(self, section, setting, evaluate=False):
        try:
            return eval(self.config[section][setting]) if evaluate else self.config[section][setting]
        except KeyError:
            raise KeyError('Error in {}: section {} doesn\'t exist or element {} has incorrect parameters.'.format(self.config_name, section, setting))
        except SyntaxError:
            raise SyntaxError('syntax error in {}'.format(setting))
    
    def get_fields(self, section, categories, evaluate=False):
        if isinstance(categories, list):
            try:
                return {category: eval(self.config[section][category]) for category in categories} if evaluate else {category: self.config[section][category] for category in categories}
            except KeyError:
                raise KeyError('Can\'t find section {} or settings {}'.format(section, ','.join(categories)))
            except SyntaxError:
                raise SyntaxError('syntax error in one of {}'.format(','.join(categories)))
        else:
            try:
                return {categories: eval(self.config[section][categories])} if evaluate else {categories: self.config[section][categories]}
            except KeyError:
                raise KeyError('Can\'t find section {} or settings {}'.format(section, categories))
            except SyntaxError:
                raise SyntaxError('syntax error in one of {}'.format(categories))


class ConfigCreator:
    def create_config(self, path, section_name='default_section_name'):
        self.config = configparser.ConfigParser()
        self.config.add_section(section_name)
        with open(path, "w") as config_file:
            self.config.write(config_file)

    def update_setting(self, path, section_name, setting, value):
        self.config = ConfigCreator.get_config(self, path)
        self.config.set(section_name, setting, value)
        with open(path, "w") as config_file:
            self.config.write(config_file)

    def get_config(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError('not find {}'.format(path))
        self.config = configparser.ConfigParser()
        self.config.read(path)
        return self.config
