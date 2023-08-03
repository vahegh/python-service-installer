from os import path
from passlib import pwd as pw
from ..base.base_package import Package, dataclass
from ...utils.consts import SERVICE_BASE_DIR, SYSTEMD_BASE_DIR

@dataclass
class BinaryPackage(Package):
    archive_url: str = None
    service_file_data: str = None

    def __post_init__(self):
        super().__post__init__()

        if self.service_file_data:
            self.service_dir = f"{SERVICE_BASE_DIR}/{self.pkg_name}"
            self.systemd_file_path = f"{SYSTEMD_BASE_DIR}/{self.pkg_name}.service"

        if self.conf_file_path and self.conf_params:
            self.conf_file_path = f"{self.service_dir}/{self.conf_file_path}"

        self.archive_file = f"{self.pkg_name}.tar.gz"
        self.archive_url = self.archive_url.format(**vars(self))
        self.user_name = self.pkg_name

        if self.database:
            self.db_name = self.pkg_name
            self.db_user = self.pkg_name
            self.db_pass = pw.genword(entropy=None, length=12)
        
    @property
    def is_installed(self):
        return path.exists(self.service_dir)