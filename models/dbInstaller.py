from models.packageInstaller import AptPackage, AptPackageInstaller
import subprocess


class DBInstaller(AptPackageInstaller):
    def __init__(self, title: str, version: str, pkg_name: str, db_engine: str, db_name: str, db_user: str, db_pass):
        super().__init__(title, version, pkg_name)

        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        if db_engine == "mysql" or db_engine == "mariadb":

            self.db_command = ['mysql', '-e']

            self.create_user = f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{self.db_pass}';"
            self.create_db = f"CREATE DATABASE {db_name};"
            self.grant_privileges = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';"
            self.flush_privileges = "FLUSH PRIVILEGES;"

            self.delete_user = f"DROP USER IF EXISTS '{db_user}'@'localhost';"
            self.delete_db = f"DROP DATABASE IF EXISTS {db_name};"

        elif db_engine == "postgresql":

            self.db_command = ['sudo', '-u', 'postgres', 'psql', '-c']

            self.create_user = f"CREATE USER {db_user} WITH PASSWORD '{self.db_pass}';"
            self.create_db = f"CREATE DATABASE {db_name} OWNER {db_user};"
            self.grant_privileges = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
            self.flush_privileges = f"GRANT USAGE, CREATE ON SCHEMA PUBLIC TO {db_user}"

            self.delete_user = f"DROP USER IF EXISTS {db_user};"
            self.delete_db = f"DROP DATABASE IF EXISTS {db_name};"


        else:
            raise ValueError("Database engine must be one of: mysql, postgresql, mariadb")


    def configure_db(self):
        
        for q in self.queries:
            if q is not None:
                command = self.db_command + [q]
                process = subprocess.run(command)
                process.check_returncode()


    def install_service(self):
        # super().install_service()

        self.queries = []
        self.queries.extend([self.create_user, self.create_db, self.grant_privileges, self.flush_privileges])

        self.configure_db()

        print(f"""Configured database.
        Database: {self.db_name}
        User: {self.db_user}
        Password: {self.db_pass}""")


    def remove_service(self):

        self.queries = []
        self.queries.extend([self.delete_db, self.delete_user])

        self.configure_db()

        print(f"Removed database {self.db_name} and user {self.db_user}")



# installer = DBInstaller(title="PostgreSQL", version="", pkg_name="postgresql-14", db_engine="postgresql", db_name="testing1", db_user="testing", db_pass="test1234")

# if __name__ == "__main__":

#     installer.remove_service()
#     installer.configure_db()