import json
default_conf_json = "test/default_config.json"
new_conf_json = "test/config.json"


with open (new_conf_json, "r") as f:
    new_conf_dict = json.load(f)

config_params = new_conf_dict["params"]

db_user = "gexamik"
db_pass = "test"
db_name = "test_db"
database = "postgres"


with open(default_conf_json, "r") as f:
    default_conf_dict = json.load(f)

def apply_configuration():


    for p in config_params:

        obj_names = p["config_key"].split("|")
        key = obj_names.pop()

        value = p["value"].format(**vars())

        obj = default_conf_dict

        for name in obj_names:
            obj = obj[name]
        obj[key] = value
            

def save_configuration():
    with open(default_conf_json, "w") as f:
        json.dump(default_conf_dict, f, indent=4)


def configure():
    apply_configuration()
    save_configuration()


configure()