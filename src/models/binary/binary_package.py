from dataclasses import dataclass
from passlib import pwd as pw
from pystemd.systemd1 import Unit
from ..base.base_package import Package
from ...utils.consts import SERVICE_BASE_DIR, SYSTEMD_BASE_DIR

@dataclass
class BinaryPackage(Package):
    archive_url: str = None
    service_file_data: str = None

    def __post_init__(self):
        super().__post__init__()
        self.service_dir = f"{SERVICE_BASE_DIR}/{self.pkg_name}"
        self.data_dir = f"{self.service_dir}/{self.data_dir}"
        self.systemd_file_path = f"{SYSTEMD_BASE_DIR}/{self.pkg_name}.service"
        self.conf_file_path = f"{self.service_dir}/{self.conf_file_path}"
        self.archive_file = f"{self.pkg_name}.tar.gz"
        self.archive_url = self.archive_url.format(**vars(self))
        self.user_name = self.pkg_name

        if self.database:
            self.db_name = self.pkg_name
            self.db_user = self.pkg_name
            self.db_pass = pw.genword(entropy=None, length=12)
            self.db_port = "5432"

        self.systemd = Unit(f"{self.pkg_name}.service")
        self.systemd.load()