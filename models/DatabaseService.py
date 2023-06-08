from models.package_manager_service import AptPackageInstaller, AptPackage
import subprocess
from dataclasses import dataclass


@dataclass
class DBPackage(AptPackage):
    db_type: str
    db_name: str
    db_user: str
    db_pass: str

    def __post_init__(self):

        if self.db_type == "mysql" or self.db_type == "mariadb":
            self.db_command = ["mysql", "-e"]

            self.create_user = f"CREATE USER '{self.db_user}'@'localhost' IDENTIFIED BY '{self.db_pass}';"
            self.create_db = f"CREATE DATABASE {self.db_name};"
            self.grant_privileges =f"GRANT ALL PRIVILEGES ON {self.db_name}.* TO '{self.db_user}'@'localhost';"
            self.flush_privileges = "FLUSH PRIVILEGES;"

            self.delete_db = f"DROP DATABASE IF EXISTS {self.db_name};"
            self.revoke_privileges = None
            self.delete_user = f"DROP USER IF EXISTS '{self.db_user}'@'localhost';"

        elif self.db_type == "postgresql":
            self.db_command = ["sudo", "-u", "postgres", "psql", "-c"]

            self.create_user = f"CREATE USER {self.db_user} WITH PASSWORD '{self.db_pass}';"
            self.create_db = f"CREATE DATABASE {self.db_name} OWNER {self.db_user};"
            self.grant_privileges = f"GRANT ALL PRIVILEGES ON DATABASE {self.db_name} TO {self.db_user};"
            self.flush_privileges = f"GRANT USAGE, CREATE ON SCHEMA PUBLIC TO {self.db_user}"

            self.delete_db = f"DROP DATABASE IF EXISTS {self.db_name};"
            self.revoke_privileges = f"REVOKE USAGE, CREATE ON SCHEMA PUBLIC FROM {self.db_user}"
            self.delete_user = f"DROP USER IF EXISTS {self.db_user};"

        else:
            raise ValueError("Database engine must be one of: mysql, postgresql, mariadb")



class DBInstaller(AptPackageInstaller):
    def __init__(self, package: DBPackage):
        self.package = package    
   
    def __getattr__(self, attr):
        return getattr(self.package, attr)

    def configure_service(self):
        for q in self.queries:
            if q is not None:
                command = self.db_command + [q]
                process = subprocess.run(command)
                process.check_returncode()

    def install_service(self):
        super().install_service()

        self.queries = []
        self.queries.extend([self.create_user, self.create_db, self.grant_privileges, self.flush_privileges])
        self.configure_service()

        print(
            f"""Configured database.
        Database: {self.db_name}
        User: {self.db_user}
        Password: {self.db_pass}"""
        )

    def remove_service(self):
        self.queries = []
        self.queries.extend([self.delete_db, self.revoke_privileges, self.delete_user])

        self.configure_service()

        print(f"Removed database {self.db_name} and user {self.db_user}")



    def configure_database(self, db_type, db_name, db_user, db_pass):
        if db_type == "mysql" or db_type == "mariadb":
            db_command = ["mysql", "-e"]

            create_user = f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}';"
            create_db = f"CREATE DATABASE {db_name};"
            grant_privileges =f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';"
            flush_privileges = "FLUSH PRIVILEGES;"

        elif db_type == "postgresql":
            db_command = ["sudo", "-u", "postgres", "psql", "-c"]

            create_user = f"CREATE USER {db_user} WITH PASSWORD '{db_pass}';"
            create_db = f"CREATE DATABASE {db_name} OWNER {db_user};"
            grant_privileges = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
            flush_privileges = f"GRANT USAGE, CREATE ON SCHEMA PUBLIC TO {db_user}"

        else:
            raise ValueError("Database engine must be one of: mysql, postgresql, mariadb")

        pass


    def remove_database(self, db_type, db_name, db_user):

        if db_type == "mysql" or db_type == "mariadb":
            delete_db = f"DROP DATABASE IF EXISTS {db_name};"
            revoke_privileges = None
            delete_user = f"DROP USER IF EXISTS '{db_user}'@'localhost';"
        elif db_type == "postgresql":
            delete_db = f"DROP DATABASE IF EXISTS {db_name};"
            revoke_privileges = f"REVOKE USAGE, CREATE ON SCHEMA PUBLIC FROM {db_user}"
            delete_user = f"DROP USER IF EXISTS {db_user};"