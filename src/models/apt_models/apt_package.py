from ..base.base_package import Package
from dataclasses import dataclass
from pystemd.systemd1 import Unit
import apt

cache = apt.Cache()

@dataclass
class AptPackage(Package):
    source_repo: str = None
    gpg_url: str = None

    def __post_init__(self):
        super().__post__init__()
        self.pkg = cache[self.pkg_name]