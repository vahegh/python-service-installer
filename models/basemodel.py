from abc import ABC, abstractmethod
from dataclasses import dataclass
# from packageInstaller import PackageInstaller
# import requests
# import os
# import apt_inst
# import pwd
# import grp
# import subprocess
# from pystemd.systemd1 import Unit

@dataclass
class Package():
    title: str
    pkg_name: str
    version: str


class Installer(ABC):

    @abstractmethod
    def check_installed(self) -> bool:
        pass

    @abstractmethod
    def check_status(self):
        pass

    @abstractmethod
    def install_service(self):
        pass

    @abstractmethod
    def remove_service(self):
        pass

    # @abstractmethod
    # def configure_service(self) -> bool:
    #     pass