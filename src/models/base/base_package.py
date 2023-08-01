from dataclasses import dataclass
from pystemd.systemd1 import Unit, Manager
from pystemd.dbusexc import DBusNoSuchUnitError
from ...utils.consts import NGINX_BASE_DIR, NGINX_PARAMS_APT

@dataclass
class Package():
    title: str # User choice (service name)
    pkg_name: str
    version: str = None # User choice
    dependencies: list = None
    conf_type: str = None
    conf_file_path: str = None
    conf_params: dict = None
    domain: str = None # User input
    ssl_email: str = None # User input
    upstream_address: str = None
    data_dir: list = None
    database: str = None # User choice
    force_install: bool = None

    def __post__init__(self):
        if self.domain:
            self.nginx_file_path = f"{NGINX_BASE_DIR}/{self.pkg_name}.conf"
            self.dependencies.extend(NGINX_PARAMS_APT)

        self.unit_bytes = f"{self.pkg_name}.service".encode()
        self.systemd = Unit(self.unit_bytes.decode())
        self.systemd.load()

        self.db_port = None

    @property
    def status(self):
        if self.service_exists():
            status_bytes = self.systemd.Unit.ActiveState
            return status_bytes.decode()
        else:
            return("unavailable")

    def service_exists(self):
        with Manager() as manager:
            try:
                manager.Manager.GetUnit(self.unit_bytes)

            except DBusNoSuchUnitError:
                return False
            else:
                return True