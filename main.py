from json import load, dumps
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
parser.add_argument("-f", "--file", help="specify configuration file")
parser.add_argument("-sr", "--service-exists", action="store_true", help="check if systemd service exists")

args = parser.parse_args()

configfile = args.file

with open(configfile, "r") as f:
    config = load(f)

install_settings = {**config, **config["user_parameters"]}
del install_settings["user_parameters"]

install_type = install_settings["install_type"]

if install_type == "apt":
    service = AptPackage(**install_settings)
    installer = AptPackageInstaller(service)

elif install_type =="binary":
    service = BinaryPackage(**install_settings)
    installer = BinaryInstaller(service)

elif install_type == "docker":
    installer = DockerInstaller(**install_settings)

else:
    raise InstallTypeError(f"Unsupported install type: {install_type}")


def main():
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


if __name__ == "__main__":
    main()