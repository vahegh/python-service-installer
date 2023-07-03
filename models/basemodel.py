from abc import ABC, abstractmethod
from dataclasses import dataclass
from models.config_manager import update_json_file, update_ini_file

@dataclass
class Package():
    title: str
    pkg_name: str
    version: str
    dependencies: list
    config_file_type: str
    config_file_path: str
    config_params: dict


class Installer(ABC):

    def __init__(self, package) -> None:
        self.package = package

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

    def configure_service(self):
        if self.config_file_type == "json":
            update_json_file(self.config_file_path, self.config_params)
        if self.config_file_type == "ini":
            update_ini_file(self.config_file_path, self.config_params)