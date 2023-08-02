from os import path, mkdir
import tarfile
import requests
import pwd
from pystemd.dbusexc import DBusNoSuchUnitError
from plumbum.cmd import useradd, userdel, chown, chmod, rm, mv
from ..base.base_installer import Installer
from ..base.base_package import manager
from ...utils.consts import SERVICE_BASE_DIR
from ...helpers.database_manager import configure_db, remove_db

class BinaryInstaller(Installer):

    def download_archive(self):
        print("Downloading archive...")
        response = requests.get(self.archive_url)
        print(f"Writing to {self.archive_file}...")
        with open (self.archive_file, "wb") as f:
            f.write(response.content)

    def install_archive(self):
        print(f"Extracting archive to {self.service_dir}...")
        tar_file = tarfile.open(self.archive_file)
        dir_name = tar_file.getmembers()[0].name
        if not dir_name == self.pkg_name:
            archive_file_dir = f"{SERVICE_BASE_DIR}/{dir_name}"
            tar_file.extractall(SERVICE_BASE_DIR)
            mv(archive_file_dir, self.service_dir)
        else:
            tar_file.extractall(SERVICE_BASE_DIR)
        # remove(self.archive_file)

    def create_user(self):
        try:
            pwd.getpwnam(self.user_name)
        except Exception:
            print(f"Creating {self.user_name} user and group...")
            useradd('--system', '--user-group', self.user_name)
        else:
            print(f"{self.user_name} user and group exist. Skipping...")

    def configure_data_dirs(self):
        print("Configuring directories...")
        for dir in self.data_dir:
            data_dir = f"{self.service_dir}/{dir}"
            if not path.isdir(data_dir):
                print(f"Creating {data_dir}...")
                mkdir(data_dir)

        chown('-R', f'{self.user_name}:{self.user_name}', self.service_dir)
        chmod('-R', 'g+w', self.service_dir)

    def configure_systemd(self):
        print("Configuring systemd service...")
        with open (self.systemd_file_path, "w") as f:
            f.write(self.service_file_data)
        self.service_action("Load")

    def install_service(self):
        if self.is_installed:
            print(f"{self.title} is already installed.")

        else:
            if not path.isfile(self.archive_file):
                self.download_archive()
            self.install_archive()
            self.create_user()
            if self.data_dir:
                self.configure_data_dirs()
            if self.database:
                self.add_db_dependency()
            if self.dependencies:
                self.install_dependencies()
            if self.database:
                configure_db(self.database, self.db_user, self.db_pass, self.db_name)
            if self.domain:
                self.configure_webserver()
            if self.systemd_file_path:
                self.configure_systemd()
            if self.conf_params:
                self.configure_service()
            self.service_action("Start")
            self.service_action("Enable")

            print(f"Installed {self.title}.")
            print("Status:", self.status)

    def remove_service(self):
        if not self.is_installed:
            print(f"{self.title} is not installed, so not removing it.")

        else:
            self.service_action("Stop")
            self.service_action("Disable")
            
            print(f"Removing user {self.user_name}...")
            userdel(self.user_name, retcode = (0, 6))
            
            print(f"Purging {self.service_dir}...")
            rm('-r', self.service_dir, retcode = (0, 1))

            rm(self.systemd_file_path, retcode = (0, 1))
            self.service_action("Reload")

            if self.database:
                remove_db(self.database, self.db_user, self.db_name)

            self.remove_dependencies()
            self.remove_webserver()

            print(f"Removed {self.title}.")