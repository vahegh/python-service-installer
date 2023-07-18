from abc import ABC, abstractmethod
from ...config_manager import update_json, update_ini
from ..apt.apt_package import AptPackage
from ..apt.apt_package import cache

class Installer(ABC):

    def __init__(self, package: AptPackage) -> None:
        self.package = package

    def __getattr__(self, attr):
        return getattr(self.package, attr)

    @abstractmethod
    def check_installed(self) -> bool:
        pass

    @abstractmethod
    def check_status(self):
        pass

    def install_dependencies(self):
        cache.update(raise_on_error=False)
        cache.open
        for dep in self.dependencies:
            dependency_pkg = AptPackage(**dep)
            if not dependency_pkg.pkg.is_installed:
                print(f"Installing dependency: {dependency_pkg.title}")
                dependency_pkg.pkg.mark_install()
            else:
                print(f"Dependency '{dependency_pkg.title}' already satisfied.")
        cache.commit()
        cache.close()

    def remove_dependencies(self):
        cache.update(raise_on_error=False)
        cache.open
        for dep in self.dependencies:
            dependency_pkg = AptPackage(**dep)
            if dependency_pkg.pkg.is_installed:
                print(f"Removing dependency: {dependency_pkg.title}")
                dependency_pkg.pkg.mark_delete()
            else:
                print(f"Dependency '{dependency_pkg.title}' not installed.")
        cache.commit()
        cache.close()

    @abstractmethod
    def install_service(self):
        pass

    @abstractmethod
    def remove_service(self):
        pass

    def configure_service(self):
        for section in self.conf_params:
            for key in self.conf_params[section]:
                self.conf_params[section][key] = self.conf_params[section][key].format(**vars(self.package))

        if self.conf_type == "json":
            update_json(self.conf_file_path, self.conf_params)
        if self.conf_type == "ini":
            update_ini(self.conf_file_path, self.conf_params)