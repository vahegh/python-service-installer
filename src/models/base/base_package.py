from dataclasses import dataclass

@dataclass
class Package():
    title: str
    pkg_name: str
    version: str = None
    dependencies: list = None
    conf_type: str = None
    conf_file_path: str = None
    conf_params: dict = None