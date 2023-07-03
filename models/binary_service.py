from os import path, mkdir
import requests
from apt_inst import TarFile
import pwd, grp
from dataclasses import dataclass
from pystemd.systemd1 import Unit
from pystemd import dbusexc
from passlib import pwd as pw
from plumbum.cmd import useradd, userdel, chown, chmod, systemctl, rm
from models.basemodel import Package, Installer
import utils.consts as consts


@dataclass
class BinaryPackage(Package):
    archive_url: str
    data_dir: str
    service_file_data: str
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
            self.db_pass = pw.genword(entropy=None, length=12)

        self.systemd = Unit(f"{self.pkg_name}.service")
        self.systemd.load()


class BinaryInstaller(Installer):

    def check_installed(self):
        return path.exists(self.service_dir) and path.exists(self.service_file_path)
    
    def check_status(self):
        status = self.systemd.Unit.ActiveState
        return status.decode()

    def install_archive(self):
        if not path.isdir(self.service_dir):
            print(f"Creating {self.service_dir}...")
            mkdir(self.service_dir)

        if not path.isfile(self.archive_file):
            print("Downloading archive...")
            response = requests.get(self.archive_url)

            print(f"Writing to {self.archive_file}...")
            with open (self.archive_file, "wb") as f:
                f.write(response.content)

        print(f"Extracting archive to {self.service_dir}...")
        TarFile(self.archive_file).extractall(consts.service_base_dir)
        # remove(self.archive_file)


    def create_user(self):
        try:
            pwd.getpwnam(self.user_name)
            grp.getgrnam(self.user_name)

        except Exception:
            print(f"Creating {self.user_name} user and group...")
            useradd('--system', '--user-group', self.user_name)

        else:
            print(f"{self.user_name} user and group exist.")


    def configure_dirs(self):
        if not path.isdir(self.data_dir):
            print(f"Creating {self.data_dir}...")
            mkdir(self.data_dir)

        chown('-R', f'{self.user_name}:{self.user_name}', self.service_dir)
        chmod('-R', 'g+w', self.service_dir)


    def configure_systemd(self):
        print("Configuring systemd service...")
        with open (self.service_file_path, "w") as f:
            f.write(self.service_file_data)
        systemctl('enable', f'{self.pkg_name}.service')


    def install_service(self):
        if self.check_installed():
            print(f"{self.title} is already installed.")
        
        else:
            self.install_archive()
            self.create_user()
            self.configure_dirs()
            self.configure_systemd()
            self.configure_service()
            self.systemd.Unit.Start(b'replace')


    def remove_service(self):
        try:
            self.systemd.Unit.Stop(b'replace')
        except dbusexc.DBusNoSuchUnitError:
            print(f"{self.title} unit doesn't exist, so not disabling it.")
        else:
            systemctl('disable', f'{self.pkg_name}.service', retcode = (0, 1))

        userdel(self.user_name, retcode = (0, 6))
        rm('-r', self.service_dir, retcode = (0, 1))
        rm('-r', self.service_file_path, retcode = (0, 1))
        print(f"Removed {self.title}.")