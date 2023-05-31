import json
from models.binaryInstaller import BinaryInstaller


with open("config.json", "r") as f:
    config = json.load(f)

# print(config)
install_type = config["install_type"]

settings = config["install_settings"]

params = config["params"]

# print(settings)
for p in params:
    print(p["config_key"])
    print(p["value"])



# apt_installer = BinaryInstaller(**config)