from os import environ as env
from plumbum.cmd import curl
from ..base.base_installer import Installer
from .apt_package import cache
from ..exceptions import VersionError

env["DEBIAN_FRONTEND"] = "noninteractive"

class AptPackageInstaller(Installer):
    """An installer object for an apt package.

    Accepts an AptPackage() object.

    Defines methods for:
      Checking whether the package is installed
      Checking its status using systemd
      Configuring repository
      Checking package version
      Setting package version
      Installing the dependencies for the package
      Removing the dependencies for the package
      Installing the package itself
      Removing the package"""

    def configure_repo(self):
        if self.source_repo and self.gpg_url:
            print(f"Configuring apt repository for {self.title}")
            source_list_path = f"/etc/apt/sources.list.d/{self.pkg_name}.list"
            gpg_file_path = f"/etc/apt/trusted.gpg.d/{self.pkg_name}.asc"

            with open(source_list_path, "w") as f:
                f.write(self.source_repo)
            curl["-sL", "-o", {gpg_file_path}, {self.gpg_url}]

    def install_service(self):
        if self.is_installed:
            print(f"{self.title} already installed")
            print(f"Status:", self.status)
        else:
            print(f"Installing service: {self.title}")
            if self.new_version:
                self.pkg_version = self.new_version
            else:
                raise VersionError(f"Version '{self.version}' not available for {self.title}.")
            self.configure_repo()
            if self.dependencies:
                self.install_dependencies()
            else:
                cache.update(raise_on_error=False)
                cache.open()
            self.pkg.mark_install()
            cache.commit()
            cache.close()
            self.configure_service()

    def remove_service(self):
        if not self.is_installed:
            print(f"{self.title} is not installed, so not removing it.")

        else:
            print(f"Removing service: {self.title}")
            self.remove_dependencies()
            self.pkg.mark_delete(purge=True)
            cache.commit()