from os import environ as env
from dataclasses import dataclass
import apt
from pystemd.systemd1 import Unit
from plumbum.cmd import curl
from models.basemodel import Installer, Package

env["DEBIAN_FRONTEND"] = "noninteractive"
cache = apt.Cache()

@dataclass
class AptPackage(Package):
    source_repo: str
    gpg_url: str

    def __post_init__(self):
        self.pkg = cache[self.pkg_name]
        self.service = Unit(f"{self.pkg_name}.service")
        self.service.load()


class AptPackageInstaller(Installer):
    """An installer object for an apt package.

    Accepts an AptPackage() object.

    Defines methods for:
    1. Checking whether the package is installed
    2. Checking its status using systemd
    3. Installing the dependencies for the package
    4. Removing the dependencies for the package
    5. Installing the package itself
    6. Removing the package"""

    def check_installed(self):
        return self.pkg.is_installed

    def check_status(self):
        status = self.service.Unit.ActiveState
        return status.decode()
    
    def configure_repo(self):
        if self.source_repo and self.gpg_url:
            print(f"Configuring apt repository for {self.title}")
            source_list_path = f"/etc/apt/sources.list.d/{self.pkg_name}.list"
            gpg_file_path = f"/etc/apt/trusted.gpg.d/{self.pkg_name}.asc"

            with open(source_list_path, "w") as f:
                f.write(self.source_repo)
            curl["-sL", "-o", {gpg_file_path}, {self.gpg_url}]

    def set_version(self):
        if self.version:
            desired_version = next((x for x in self.pkg.versions if x.version == self.version), None)
            if desired_version:
                print(f"Setting version '{self.version}' for {self.title}")
                self.pkg.candidate = desired_version
            else:
                print(f"Version '{self.version}' not available for {self.title}, defaulting to latest.")

    def install_dependencies(self):
        for d in self.dependencies:
            dependency_config = d["install_settings"]
            dependency_pkg = AptPackage(**dependency_config)
            if not dependency_pkg.pkg.is_installed:
                print(f"Installing dependency: {dependency_pkg.title}")
                dependency_pkg.pkg.mark_install()
            else:
                print(f"Dependency '{dependency_pkg.title}' already satisfied.")

    def remove_dependencies(self):
        for d in self.dependencies:
            dependency_config = d["install_settings"]
            dependency_pkg = AptPackage(**dependency_config)
            if dependency_pkg.pkg.is_installed:
                print(f"Removing dependency: {dependency_pkg.title}")
                dependency_pkg.pkg.mark_delete()
            else:
                print(f"Dependency '{dependency_pkg.title}' not installed.")

    def install_service(self):
        if self.check_installed():
            print(f"{self.title} already installed")
            print(f"Status: {self.check_status()}")
        else:
            print(f"Installing service: {self.title}")
            self.set_version()
            self.configure_repo()
            cache.update(raise_on_error=False)
            cache.open()
            self.install_dependencies()
            self.pkg.mark_install()
            cache.commit()
            self.configure_service()

    def remove_service(self):
        if not self.check_installed():
            print(f"{self.title} is not installed, so not removing it.")

        else:
            print(f"Removing service: {self.title}")
            self.remove_dependencies()
            self.pkg.mark_delete(purge=True)
            cache.commit()