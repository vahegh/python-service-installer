from dataclasses import dataclass
from pystemd.systemd1 import Unit
from ...utils.consts import NGINX_BASE_DIR, NGINX_PARAMS_APT

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

        self.systemd = Unit(f"{self.pkg_name}.service")
        self.systemd.load()
    
    @property
    def status(self):
        st = self.systemd.Unit.ActiveState
        return st.decode()