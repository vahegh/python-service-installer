from dataclasses import dataclass
from ...utils.consts import NGINX_BASE_DIR, NGINX_PARAMS_APT, CERT_BASE_DIR

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
    data_dir: str = None
    database: str = None


    def __post__init__(self):
        if self.nginx_params:
            self.domain = self.nginx_params["DOMAIN"]
            self.email = self.nginx_params["EMAIL"]
            self.nginx_file_path = f"{NGINX_BASE_DIR}/{self.pkg_name}.conf"
            self.dependencies.extend(NGINX_PARAMS_APT)