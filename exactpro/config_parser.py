import configparser
import os
from flask import session


class SettingProvider:
    def __init__(self, config_name):
        # checks whether the ini-file exists
        if not os.path.exists(config_name):
            raise FileNotFoundError('not find {}'.format(config_name))
        else:
            self.config_name = config_name
            self.config = configparser.ConfigParser()
            self.config.read(self.config_name)
    
    def get_parameters(self, section):
        return [parameter for parameter in self.config[section]]

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
                raise KeyError('not find section {} or settings {}'.format(section, ','.join(categories)))
            except SyntaxError:
                raise SyntaxError('syntax error in one of {}'.format(','.join(categories)))
        else:
            try:
                return {categories: eval(self.config[section][categories])} if evaluate else {categories: self.config[section][categories]}
            except KeyError:
                raise KeyError('not find section {} or settings {}'.format(section, categories))
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
            raise FileNotFoundError('can\'t find {}'.format(path))
        self.config = configparser.ConfigParser()
        self.config.read(path)
        return self.config


def load_defect_attributes():
    defect_attributes = {}
    config_reader = SettingProvider('defect_attributes.ini')
    session['defect_attributes'] = config_reader.get_fields(
                                                section='defect_attributes', 
                                                categories=['mandatory_fields', 'special_fields', 'area_of_testing_fields'], 
                                                evaluate=True
                                                )
    defect_attributes['special_fields'] = [{
                                            'gui_name': field_name,
                                            'xml_name': session['defect_attributes']['special_fields'][field_name]['name'],
                                            'type': session['defect_attributes']['special_fields'][field_name]['type']
                                            } for field_name in session['defect_attributes']['special_fields']
                                            ]

    defect_attributes['area_of_testing_fields_for_models'] = {field_name.strip()+'_lab':{
        'gui_name':field_name.strip(), 
        'name':session['defect_attributes']['area_of_testing_fields'][field_name]['name'].strip()}  
        for field_name in list(session['defect_attributes']['area_of_testing_fields'])}
    
    defect_attributes['area_of_testing_fields'] = [{
                                                    'gui_name': field_name.strip(),
                                                    'name': session['defect_attributes']['area_of_testing_fields'][field_name]['name'].strip()  
                                                    } for field_name in list(session['defect_attributes']['area_of_testing_fields'])
                                                    ]
                                                    
    session['ref_to'] = config_reader.get_fields(
                                                section='defect_attributes',
                                                categories='referring_to',
                                                evaluate=True
                                                )
    defect_attributes['referring_to'] = session['ref_to']['referring_to']
    # gets resolutions for single mode
    # these resolutions are also used for models creation
    session['resolution'] = config_reader.get_fields(
                                                    section='defect_attributes',
                                                    categories='resolution',
                                                    evaluate=True
                                                    )['resolution']
    defect_attributes['resolution'] = session['resolution']
    # gets fields for multiple mode
    session['multiple_mode_fields'] = config_reader.get_setting(
                                                            section='defect_attributes', 
                                                            setting='multiple_mode_fields', 
                                                            evaluate=True
                                                            )
    defect_attributes['multiple_mode_fields'] = ','.join(session['multiple_mode_fields'])
    

    return defect_attributes


def unpack_dictionary_val_to_list(dictionary):
    unpacked_list = [el for el in dictionary.values() if not isinstance(el, list)]
    for el in [el for el in dictionary.values() if isinstance(el, list)]:
        unpacked_list += el
    return unpacked_list


def get_models_names():
    config_reader = SettingProvider('predictions_parameters.ini')
    areas_of_testing = config_reader.get_fields(
                                            section='predictions_parameters',
                                            categories='areas_of_testing',
                                            evaluate=False)['areas_of_testing'].split(',')
    config_reader = SettingProvider('defect_attributes.ini')
    resolution = unpack_dictionary_val_to_list(config_reader.get_fields(
                                                                    section='defect_attributes',
                                                                    categories='resolution',
                                                                    evaluate=True)['resolution'])
    models = [model for container in [areas_of_testing, resolution] for model in container]

    return models