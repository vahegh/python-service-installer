from ..base.base_package import Package
from dataclasses import dataclass
import apt

cache = apt.Cache()

@dataclass
class AptPackage(Package):
    source_repo: str = None
    gpg_url: str = None

    def __post_init__(self):
        super().__post__init__()
        self.pkg = cache[self.pkg_name]
        self.new_version = next((x for x in self.pkg.versions if self.version in x.version), None)
    
    @property
    def is_installed(self):
        return self.pkg.is_installed
    
    @property
    def pkg_version(self):
        return self.pkg.installed.version
    
    @pkg_version.setter
    def pkg_version(self):
        print(f"Setting version '{self.version}' for {self.title}")
        self.pkg.candidate = self.new_version