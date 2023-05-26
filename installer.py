import apt
import apt_inst
import argparse
import requests
import os
from abc import ABC, abstractmethod

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--delete", action="store_true")
args = parser.parse_args()



class ServiceInstaller(ABC):

    def __init__(self, title, version, ):
        self.title = title
        self.version = version

    @abstractmethod
    def check_installed(self) -> bool:
        pass

    @abstractmethod
    def install_service(self) -> bool:
        pass

    # @abstractmethod
    # def configure_service(self) -> bool:
    #     pass




class PackageInstaller(ServiceInstaller):

    def __init__(self, title: str, version: str, pkg_name: str):

        super().__init__(title, version)
        self.pkg_name = pkg_name

        self.cache = apt.Cache()
        self.pkg = self.cache[self.pkg_name]
        self.available_versions = self.pkg.versions
        self.desired_version = next((x for x in self.available_versions if x.version == self.version), None)
        self.pkg_name = self.pkg_name.capitalize()


    def check_installed(self):

        return self.pkg.is_installed
    
    def set_version(self):

        if self.desired_version is not None:
            self.pkg.candidate = self.desired_version
            self.pre_install()
        else:
            pass    

    def pre_install(self):

        self.cache.update()
        self.cache.open()

    def install_service(self):

        print(f"Installing {self.pkg_name}")
        self.pkg.mark_install()
        self.cache.commit()
    
    def remove_service(self):

        print(f"Removing {self.pkg_name}")
        self.pkg.mark_delete()
        self.cache.commit()


    def post_install(self):

        self.cache.update()
        self.cache.close()


apt_installer = PackageInstaller(title="NGINX", version= "1.18.0-6ubuntu14", pkg_name='nginx')


apt_installer.pre_install()

if args.delete:
    if apt_installer.check_installed():
        apt_installer.remove_service()
    else:
        print(f"{apt_installer.pkg_name} not installed.")

else:
    if apt_installer.check_installed():
        print(f"{apt_installer.pkg_name} already installed")
    else:
        apt_installer.set_version()
        apt_installer.install_service()
 
apt_installer.post_install()


# apt_installer.archive_download(base_url)
# apt_installer.archive_install(file_name, "/opt")

main_url = "https://releases.mattermost.com/7.10.2/mattermost-7.10.2-linux-amd64.tar.gz"
base_url = "releases.mattermost.com"
target_dir = "/opt"

class BinaryInstaller(ServiceInstaller):

    def __init__(self, title: str, version: str, pkg_name: str, base_url: str, target_dir: str):
        super().__init__(title, version)
        self.base_url = base_url
        self.target_dir = target_dir
        self.pkg_name = pkg_name

    # def archive_download(self):
    #     response = requests.get(base_url)
    #     with open(file_name, "wb") as f:
    #         f.write(response.content)

    # def archive_install(self):

    #     if not os.path.isdir(target_dir):
    #         print(f"{target_dir} directory doesn't exist. Creating now.")
    #         os.mkdir(target_dir)

    #     apt_inst.TarFile(file_name).extractall(target_dir)

binary_installer = BinaryInstaller("Mattermost", "7.10.2", "mattermost.tar.gz", "releases.mattermost.com", "/opt")

