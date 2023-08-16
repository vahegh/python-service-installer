from json import load
from argparse import ArgumentParser
from src.models.apt_models.apt_package import AptPackage
from src.models.binary.binary_package import BinaryPackage
from src.models.binary.binary_installer import BinaryInstaller
from src.models.apt_models.apt_installer import AptPackageInstaller
from src.models.docker.docker_installer import DockerInstaller
from src.utils.exceptions import InstallTypeError

parser = ArgumentParser()
parser.add_argument("-i", "--install", action="store_true", help="install service")
parser.add_argument("-r", "--remove", action="store_true", help="remove service")
parser.add_argument("-s", "--status", action="store_true", help="check service status")
parser.add_argument("-ci", "--is-installed", action="store_true",help="check whether service is installed")
parser.add_argument("-v", "--version", action="store_true", help="check service version")
parser.add_argument("-f", "--file", help="specify configuration file", required=True)
parser.add_argument("-sr", "--service-exists", action="store_true", help="check if systemd service exists")

args = parser.parse_args()

configfile = args.file
with open(configfile, "r") as f:
    config = load(f)

if type(config) == dict:
    install_type = config["install_type"]
elif type(config) == list:
    install_type = "docker"

def load_config(conf):
    install_settings = {**conf, **conf["user_parameters"]}
    del install_settings["user_parameters"]
    return install_settings

def service_action():
    if args.install:
        installer.install_service()

    elif args.remove:
        installer.remove_service()
    
    elif args.status:
        print(installer.status)
    
    elif args.is_installed:
        print(installer.is_installed)
    
    elif args.version:
        print(f"Version: {installer.pkg_version}")

    elif args.service_exists:
        print(installer.service_exists())


if install_type == "apt":
    install_settings = load_config(config)
    service = AptPackage(**install_settings)
    installer = AptPackageInstaller(service)
    service_action()

elif install_type =="binary":
    install_settings = load_config(config)
    service = BinaryPackage(**install_settings)
    installer = BinaryInstaller(service)
    service_action()

elif install_type == "docker":
    for i in config:
        install_settings = load_config(i)
        installer = DockerInstaller(**install_settings)
        service_action()

else:
    raise InstallTypeError(f"Unsupported install type: {install_type}")


# def main():
#     pass

# if __name__ == "__main__":
#     main()