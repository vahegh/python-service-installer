import json
import configparser

def update_ini_file(config_file_path, config_params):
    # Read the existing INI file
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(config_file_path)

    # Update the options in the INI file
    for section, settings in config_params.items():
        if config.has_section(section):
            for key, value in settings.items():
                config.set(section, key, str(value))
        else:
            print(f"Section '{section}' not found")

    # Write the updated configuration back to the INI file
    with open(config_file_path, 'w') as configfile:
        config.write(configfile, False)


def update_json_file(config_file_path, config_params):
    # Read the existing JSON file
    with open(config_file_path, 'r') as f:
        config_file = json.load(f)

    # Update values inside the file
    def update_values(config_file, config_params):
        for key, value in config_params.items():
            if key in config_file:
                if isinstance(value, dict) and isinstance(config_file[key], dict):
                    update_values(config_file[key], value)
                else:
                    config_file[key] = value
            else:
                config_file[key] = value
    update_values(config_file, config_params)

    # Write the updated configuration back to the JSON file
    with open(config_file_path, 'w') as f:
        json.dump(config_file, f, indent=4)