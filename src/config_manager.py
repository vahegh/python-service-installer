import json
import configparser
import yaml

def update_ini(conf_file_path, conf_params):
    # Read the existing INI file
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(conf_file_path)

    # Update values in the file
    for section, settings in conf_params.items():
        if config.has_section(section):
            for key, value in settings.items():
                config.set(section, key, str(value))
        else:
            print(f"Section '{section}' not found")

    # Write the updated configuration back to the INI file
    with open(conf_file_path, 'w') as f:
        config.write(f, False)


def update_json(conf_file_path, conf_params):
    # Read the existing JSON file
    with open(conf_file_path, 'r') as f:
        config_file = json.load(f)

    # Update values in the file
    def update_values(config_file, conf_params):
        for key, value in conf_params.items():
            if key in config_file:
                if isinstance(value, dict) and isinstance(config_file[key], dict):
                    update_values(config_file[key], value)
                else:
                    config_file[key] = value
            else:
                config_file[key] = value
    update_values(config_file, conf_params)

    # Write the updated configuration back to the JSON file
    with open(conf_file_path, 'w') as f:
        json.dump(config_file, f, indent=4)


def update_yaml(conf_file_path, conf_params):
    with open(conf_file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    data.update(conf_params)
    
    with open(conf_file_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)