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
                if config.has_option(section, key):
                    config.set(section, key, str(value))
                else:
                    print(f"Option '{key}' not found in section '{section}'")
        else:
            print(f"Section '{section}' not found")

    # Write the updated configuration back to the INI file
    with open(config_file_path, 'w') as configfile:
        config.write(configfile, False)


def update_json_file(config_file_path, config_params):
    # Read the existing JSON file
    with open(config_file_path, 'r') as f:
        data = json.load(f)

    # Update values inside the file
    def update_values(data, config_params):
        for k, v in config_params.items():
            if k in data:
                if isinstance(v, dict) and isinstance(data[k], dict):
                    update_values(data[k], v)
                else:
                    data[k] = v
            else:
                data[k] = v
    update_values(data, config_params)

    # Write the updated configuration back to the JSON file
    with open(config_file_path, 'w') as f:
        json.dump(data, f, indent=4)