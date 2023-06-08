import configparser
import json
import yaml

class ConfigManager():

    def __init__(self, config_type: str, config_file_path: str, config_params: dict):
        self.config_type = config_type
        self.config_file_path = config_file_path
        self.config_params = config_params


    def dict_to_ini(self):
        if self.config_type == "ini":
            config = configparser.ConfigParser()
            for section, settings in self.config_params.items():
                config.add_section(section)
                for key, value in settings.items():
                    config.set(section, key, str(value))
            return config


    def ini_to_dict(self):
        config_dict = {}
        for section in self.config_file_path.sections():
            config_dict[section] = {}
            for key, value in self.config_file_path.items(section):
                config_dict[section][key] = value
        return config_dict



    def dict_to_json(config_dict):
        return json.dumps(config_dict)

    def json_to_dict(config_json):
        return json.loads(config_json)

    def dict_to_yaml(config_dict):
        return yaml.dump(config_dict)

    def yaml_to_dict(config_yaml):
        return yaml.safe_load(config_yaml)