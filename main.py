from json import load
from argparse import ArgumentParser
from src.models.apt.apt_package import AptPackage
from src.models.binary.binary_package import BinaryPackage
from src.models.binary.binary_service import BinaryInstaller
from src.models.apt.package_manager_service import AptPackageInstaller

parser = ArgumentParser()
parser.add_argument("-i", "--install", action="store_true", help="install service")
parser.add_argument("-r", "--remove", action="store_true", help="remove service")
parser.add_argument("-cs", "--check-status", action="store_true", help="check service status")
parser.add_argument("-ci", "--check-installed", action="store_true",help="check whether service is installed")
parser.add_argument("-f", "--file", help="specify configuration file")

args = parser.parse_args()
configfile = args.file if args.file else "test/samples/mattermost.json"

with open(configfile, "r") as f:
    config = load(f)

install_type = config["install_type"]
install_settings = config["install_settings"]

if install_type == "packagemanager":
    service = AptPackage(**install_settings)
    installer = AptPackageInstaller(service)

elif install_type =="binary":
    service = BinaryPackage(**install_settings)
    installer = BinaryInstaller(service)


def main():
    if args.install:
        installer.install_service()

    elif args.remove:
        installer.remove_service()
    
    elif args.check_status:
        print(f"Status: {installer.check_status()}")
    
    elif args.check_installed:
        print(f"Installed: {installer.check_installed()}")

    else:
        installer.install_service()


if __name__ == "__main__":
    main()