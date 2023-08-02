from abc import ABC, abstractmethod
from ...helpers.config_manager import update_json, update_ini, update_yaml
from ..apt_models.apt_package import AptPackage
from ..apt_models.apt_package import cache
from ..base.base_package import manager, DBusNoSuchUnitError
from ...helpers.nginx_manager import configure_nginx, configure_ssl, remove_webserver_conf
from ...utils.consts import MYSQL_PARAMS_APT, POSTGRESQL_PARAMS_APT
from ...utils.exceptions import DbTypeError, ServiceActionError

class Installer(ABC):

    def __init__(self, package) -> None:
        self.package = package

    def __getattr__(self, attr):
        return getattr(self.package, attr)

    def install_dependencies(self):
        cache.update(raise_on_error=False)
        cache.open
        for dep in self.dependencies:
            dependency_pkg = AptPackage(**dep)
            if not dependency_pkg.pkg.is_installed:
                print(f"Installing dependency: {dependency_pkg.title}")
                dependency_pkg.pkg.mark_install()
            else:
                print(f"Dependency '{dependency_pkg.title}' already satisfied.")
        cache.commit()
        cache.close()

    def remove_dependencies(self):
        cache.update(raise_on_error=False)
        cache.open
        for dep in self.dependencies:
            dependency_pkg = AptPackage(**dep)
            if dependency_pkg.pkg.is_installed:
                print(f"Removing dependency: {dependency_pkg.title}")
                dependency_pkg.pkg.mark_delete(purge=True)
            else:
                print(f"Dependency '{dependency_pkg.title}' not installed.")
        cache.commit()
        cache.close()

    @abstractmethod
    def install_service(self):
        pass

    @abstractmethod
    def remove_service(self):
        pass

    def service_action(self, action):
        try:
            if action == "Start":
                print(f"Starting {self.unit_str}...")
                self.systemd.Unit.Start(b'replace')
            elif action == "Restart":
                print(f"Restarting {self.unit_str}...")
                self.systemd.Unit.Restart(b'replace') 
            elif action == "Stop":
                print(f"Stopping {self.unit_str}...")
                self.systemd.Unit.Stop(b'replace')
            elif action == "Enable":
                print(f"Enabling {self.unit_str}...")
                manager.Manager.EnableUnitFiles([self.unit_bytes], True, True)   
            elif action == "Disable":     
                print(f"Disabling {self.unit_str}...")
                manager.Manager.DisableUnitFiles([self.unit_bytes], True)
            elif action == "Load":
                print(f"Loading {self.unit_str}...")
                manager.Manager.LoadUnit(self.unit_bytes)
                manager.load()
            elif action == "Reload":
                manager.Manager.Reload()
                manager.load()

            else:
                raise ServiceActionError(f"Unsupported action '{action}'")

        except DBusNoSuchUnitError:
            print(f"Failed to {action} {self.unit_str}")

    def add_db_dependency(self):
        if self.database in ["mysql", "mariadb", "maria"]:
            self.dependencies.append(MYSQL_PARAMS_APT)
            self.package.db_port = 3306

        elif self.database in ["postgresql", "postgres", "psql"]:
            self.dependencies.append(POSTGRESQL_PARAMS_APT)
            self.package.db_port = 5432
        
        else:
            raise DbTypeError(f"Unsupported database '{self.database}'")

    def configure_service(self):
        for section in self.conf_params:
            for key in self.conf_params[section]:
                self.conf_params[section][key] = self.conf_params[section][key].format(**vars(self.package))
        if self.conf_type == "json":
            update_json(self.conf_file_path, self.conf_params)
        elif self.conf_type == "ini":
            update_ini(self.conf_file_path, self.conf_params)
        elif self.conf_type == "yaml":
            update_yaml(self.conf_file_path, self.conf_params)

    def configure_webserver(self):
        if self.domain:
            configure_nginx(self.nginx_file_path, self.domain, self.upstream_address)
            configure_ssl(self.domain, self.ssl_email)

    def remove_webserver(self):
        if self.domain:
            remove_webserver_conf(self.nginx_file_path)