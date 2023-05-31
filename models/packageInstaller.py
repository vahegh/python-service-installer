from models.basemodel import ServiceInstaller
import apt
from os import environ as env


class PackageInstaller(ServiceInstaller):

    env["DEBIAN_FRONTEND"] = "noninteractive"
    
    def __init__(self, title: str, version: str, pkg_name: str):
        super().__init__(title, version, pkg_name)
        
        
        self.cache = apt.Cache()
        self.pkg = self.cache[self.pkg_name]
        self.available_versions = self.pkg.versions
        self.desired_version = next((x for x in self.available_versions if x.version == self.version), None)


    def check_installed(self):
        return self.pkg.is_installed
    

    def set_version(self):
        if self.desired_version is not None:
            self.pkg.candidate = self.desired_version
            self.open_cache()
        else: 
            print(f"Version '{self.version}' not available for {self.title}, defaulting to latest.")


    def open_cache(self):
        self.cache.update()
        self.cache.open()


    def close_cache(self):
        self.cache.update()
        self.cache.close()


    def install_service(self):
        if self.check_installed():
            print(f"{self.title} already installed")
        else:
            print(f"Installing {self.title}")
            self.set_version()
            self.open_cache()
            self.pkg.mark_install()
            self.cache.commit()
            self.close_cache()



    def remove_service(self):
        if not self.check_installed():
            print(f"{self.title} is not installed, so not removing it.")

        else:
            print(f"Removing {self.title}")
            self.open_cache()
            self.pkg.mark_delete(purge=True)
            self.cache.commit()
            self.close_cache()