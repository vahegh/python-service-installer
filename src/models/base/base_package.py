from dataclasses import dataclass
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
    nginx_params: dict = None
    data_dir: list = None
    database: str = None
    force_install: bool = None


    def __post__init__(self):
        if self.nginx_params:
            self.domain = self.nginx_params["DOMAIN"]
            self.email = self.nginx_params["EMAIL"]
            self.nginx_file_path = f"{NGINX_BASE_DIR}/{self.pkg_name}.conf"