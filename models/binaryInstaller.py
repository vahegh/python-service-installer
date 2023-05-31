from models.basemodel import ServiceInstaller
from models.dbInstaller import DBInstaller
import os
import requests
import apt_inst
import pwd, grp
import subprocess
import shutil
from pystemd.systemd1 import Unit
from pystemd import dbusexc
import json
from passlib import pwd



class BinaryInstaller(ServiceInstaller):

    def __init__(self, title: str, version: str, pkg_name: str, archive_url: str, data_dir: str, service_file_data: str, config_file_path: str, database: None, config_params: dict):
        super().__init__(title, version, pkg_name)

        self.archive_url = archive_url.format(version, version)
        self.archive_file = f"{pkg_name}.tar.gz"
        self.service_file_data = service_file_data

        self.config_params = config_params

        self.base_dir = "/opt"
        self.service_dir = f"{self.base_dir}/{self.pkg_name}"
        self.data_dir = f"{self.service_dir}/{data_dir}"

        self.service_file_path = f"/etc/systemd/system/{self.pkg_name}.service"
        self.config_file_path = f"{self.service_dir}/{config_file_path}"

        self.user_name = self.pkg_name

        self.systemd = Unit(f"{self.pkg_name}.service")
        self.systemd.load()


        if database:
            self.database = database
            self.db_name = self.pkg_name
            self.db_user = self.pkg_name
            self.db_pass = pwd.genword(entropy=None, length=12)

            

    def check_installed(self) -> bool:
        return os.path.exists(self.service_dir) 
    

    def install_archive(self):

        if not os.path.isdir(self.service_dir):
            print(f"{self.service_dir} directory doesn't exist. Creating now.")
            os.mkdir(self.service_dir)

        if not os.path.isfile(self.archive_file):
            print("Downloading archive...")
            response = requests.get(self.archive_url)

            print(f"Done. Writing to {self.archive_file}")
            with open (self.archive_file, "wb") as f:
                f.write(response.content)

        print(f"Done. Extracting archive to {self.service_dir}")

        apt_inst.TarFile(self.archive_file).extractall(self.base_dir)

        # os.remove(self.archive_file)

        print("Done.")


    def create_user(self):
        try:
            pwd.getpwnam(self.user_name)
            grp.getgrnam(self.user_name)

        except Exception:
            print(f"Creating {self.user_name} user and group.")
            subprocess.run(['useradd', '--system', '--user-group', self.user_name])

        else:
            print(f"{self.user_name} user and group exist.")


    def configure_dirs(self):

        if not os.path.isdir(self.data_dir):
            print(f"{self.data_dir} directory doesn't exist. Creating now.")
            os.mkdir(self.data_dir)

        subprocess.run(['chown', '-R', f'{self.user_name}:{self.user_name}', self.service_dir])
        subprocess.run(['chmod', '-R', 'g+w', self.service_dir])


    def configure_systemd(self):
        with open (self.service_file_path, "w") as f:
            f.write(self.service_file_data)
        subprocess.run(['systemctl', 'enable', f'{self.pkg_name}.service'])

    def check_status(self):
        status = self.systemd.Unit.ActiveState
        return status.decode()


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
        
        variables = vars()
        variables.update(self.__dict__)
        

        with open(self.config_file_path, "r") as f:
            default_config_dict = json.load(f)


        def apply_configuration():
            for p in self.config_params:
                obj_names = p["config_key"].split("|")
                key = obj_names.pop()

                value = p["value"].format(**variables)
                obj = default_config_dict

                for name in obj_names:
                    obj = obj[name]
                obj[key] = value

        def save_configuration():
            with open(self.config_file_path, "w") as f:
                json.dump(default_config_dict, f, indent=4)

        apply_configuration()
        save_configuration()

    def remove_service(self):

        try:
            self.systemd.Unit.Stop(b'replace')
        except dbusexc.DBusNoSuchUnitError:
            pass

        subprocess.run(['systemctl', 'disable', f'{self.pkg_name}.service'])

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

        subprocess.run(['userdel', self.user_name])
        shutil.rmtree(self.service_dir, ignore_errors=True)
        shutil.rmtree(self.service_file_path, ignore_errors=True)
        print(f"Removed {self.title}.")