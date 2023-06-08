from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Package():
    title: str
    pkg_name: str
    version: str
    dependencies: list
    config_params: list


class Installer(ABC):

    def __getattr__(self, attr):
        return getattr(self.package, attr)

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