from os import path, mkdir
import requests
from apt_inst import TarFile
import pwd, grp
from dataclasses import dataclass
from pystemd.systemd1 import Unit
from pystemd import dbusexc
from passlib import pwd
from plumbum.cmd import useradd, userdel, chown, chmod, systemctl, rm
from models.basemodel import Package, Installer
from models.config_manager import update_json_file, update_ini_file
from models.dbInstaller import DBInstaller
import utils.consts as consts


@dataclass
class BinaryPackage(Package):
    archive_url: str
    data_dir: str
    service_file_data: str
    config_file_type: str
    config_file_path: str
    database: str


    def __post_init__(self):
        self.service_dir = f"{consts.service_base_dir}/{self.pkg_name}"
        self.data_dir = f"{self.service_dir}/{self.data_dir}"
        self.service_file_path = f"{consts.systemd_base_dir}/{self.pkg_name}.service"
        self.config_file_path = f"{self.service_dir}/{self.config_file_path}"
        self.archive_file = f"{self.pkg_name}.tar.gz"
        self.archive_url = self.archive_url.format(self.version, self.version)
        self.user_name = self.pkg_name

        if self.database:
            self.db_name = self.pkg_name
            self.db_user = self.pkg_name
            self.db_pass = pwd.genword(entropy=None, length=12)

        self.systemd = Unit(f"{self.pkg_name}.service")
        self.systemd.load()



class BinaryInstaller(Installer):

    def __init__(self, package: BinaryPackage):
        self.package = package
            
    def __getattr__(self, attr):
        return getattr(self.package, attr)

    def check_installed(self):
        return path.exists(self.service_dir) 
    
    def check_status(self):
        status = self.systemd.Unit.ActiveState
        return status.decode()

    def install_archive(self):
        if not path.isdir(self.service_dir):
            print(f"{self.service_dir} directory doesn't exist. Creating now.")
            mkdir(self.service_dir)

        if not path.isfile(self.archive_file):
            print("Downloading archive...")
            response = requests.get(self.archive_url)

            print(f"Done. Writing to {self.archive_file}")
            with open (self.archive_file, "wb") as f:
                f.write(response.content)

        print(f"Done. Extracting archive to {self.service_dir}")

        TarFile(self.archive_file).extractall(self.base_dir)

        # os.remove(self.archive_file)

        print("Done.")


    def create_user(self):
        try:
            pwd.getpwnam(self.user_name)
            grp.getgrnam(self.user_name)

        except Exception:
            print(f"Creating {self.user_name} user and group.")
            useradd['--system', '--user-group', self.user_name]

        else:
            print(f"{self.user_name} user and group exist.")


    def configure_dirs(self):
        if not path.isdir(self.data_dir):
            print(f"{self.data_dir} directory doesn't exist. Creating now.")
            mkdir(self.data_dir)

        chown['-R', f'{self.user_name}:{self.user_name}', self.service_dir]
        chmod['-R', 'g+w', self.service_dir]


    def configure_systemd(self):
        with open (self.service_file_path, "w") as f:
            f.write(self.service_file_data)
        systemctl['enable', f'{self.pkg_name}.service']


    def configure_deps_db(self):
        if self.database:
            database_service = DBInstaller(
                self.database,
                None,
                self.database,
                self.database,
                self.db_name,
                self.db_user,
                self.db_pass
            )
            database_service.install_service()


    def install_service(self):
        if self.check_installed():
            print(f"{self.pkg_name} is already installed.")
        
        else:
            self.configure_deps_db()
            self.install_archive()
            self.create_user()
            self.configure_dirs()
            self.configure_systemd()
            self.configure_service()

            self.systemd.Unit.Start(b'replace')
 

    def configure_service(self):
        if self.config_file_type == "json":
            update_json_file(self.config_file_path, self.config_params)
        if self.config_file_type == "ini":
            update_ini_file(self.config_file_path, self.config_params)


    def remove_service(self):

        try:
            self.systemd.Unit.Stop(b'replace')
        except dbusexc.DBusNoSuchUnitError:
            pass

        systemctl['disable', f'{self.pkg_name}.service']

        if self.database:
            database_service = DBInstaller(
                self.database,
                None,
                self.database,
                self.database,
                self.db_name,
                self.db_user,
                None
            )
            database_service.remove_service()

        userdel[self.user_name]
        rm['-r', self.service_dir]
        rm['-r', self.service_file_path]
        print(f"Removed {self.title}.")