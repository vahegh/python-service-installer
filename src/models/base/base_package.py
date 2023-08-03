from pydantic.dataclasses import dataclass
from pystemd.systemd1 import Unit, Manager
from pystemd.dbusexc import DBusNoSuchUnitError
from ...utils.consts import NGINX_BASE_DIR, NGINX_PARAMS_APT

manager = Manager(_autoload = True)

@dataclass
class Package():
    title: str
    pkg_name: str
    version: str = None
    dependencies: list = None
    conf_type: str = None
    conf_file_path: str = None
    conf_params: dict = None
    domain: str = None
    ssl_email: str = None
    upstream_address: str = None
    data_dir: list = None
    database: str = None
    force_install: bool = None

    def __post__init__(self):
        if self.domain:
            self.nginx_file_path = f"{NGINX_BASE_DIR}/{self.pkg_name}.conf"
            self.dependencies.extend(NGINX_PARAMS_APT)

        self.unit_str = f"{self.pkg_name}.service"
        self.unit_bytes = self.unit_str.encode()
        self.systemd = Unit(self.unit_str, _autoload = True)

        self.db_port = None

    @property
    def status(self):
        if self.service_exists():
            status_bytes = self.systemd.Unit.ActiveState
            return status_bytes.decode()
        else:
            return("unavailable")

    def service_exists(self):
        try:
            manager.Manager.GetUnit(self.unit_bytes)

        except DBusNoSuchUnitError:
            return False
        else:
            return True