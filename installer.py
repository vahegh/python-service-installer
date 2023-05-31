import json
from models.binaryInstaller import BinaryInstaller
from models.packageInstaller import PackageInstaller


with open("config.json", "r") as f:
    config = json.load(f)

install_type = config["install_type"]

settings = config["install_settings"]

params = config["params"]

if install_type == "binary":
    service = BinaryInstaller(**settings, config_params=params)
    try:
        service.install_service()

    except Exception as e:
        service.remove_service()
        raise e
    # service.remove_service()

# apt_installer = BinaryInstaller(**config)