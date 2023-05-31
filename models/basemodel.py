from abc import ABC, abstractmethod
# from packageInstaller import PackageInstaller
# import requests
# import os
# import apt_inst
# import pwd
# import grp
# import subprocess
# from pystemd.systemd1 import Unit


class ServiceInstaller(ABC):

    def __init__(self, title, version, pkg_name):
        self.title = title
        self.version = version
        self.pkg_name = pkg_name

    # @abstractmethod
    # def check_installed(self) -> bool:
    #     pass

    # @abstractmethod
    # def check_status(self):
    #     pass

    # @abstractmethod
    # def install_service(self):
    #     pass

    # @abstractmethod
    # def remove_service(self):
    #     pass

    # @abstractmethod
    # def configure_service(self) -> bool:
    #     pass

