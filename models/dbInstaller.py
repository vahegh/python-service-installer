from packageInstaller import PackageInstaller
import subprocess
from passlib import pwd


class DBInstaller(PackageInstaller):
    def __init__(self, title: str, version: str, pkg_name: str, db_engine: str, db_name: str, db_user: str, db_pass: None):
        super().__init__(title, version, pkg_name)

        self.db_name = db_name
        self.db_user = db_user
        if db_pass:
            self.db_pass = db_pass
        else:
            self.db_pass = pwd.genword(None, 12)


        if db_engine == "mysql" or db_engine == "mariadb":

            self.db_command = ['mysql', '-e']

            create_user = f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}';"
            create_db = f"CREATE DATABASE {db_name};"
            grant_privileges = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';"
            flush_privileges = "FLUSH PRIVILEGES;"

        elif db_engine == "postgresql":

            self.db_command = ['sudo', '-u', 'postgres', 'psql', '-c']

            create_user = f"CREATE USER {db_user} WITH PASSWORD '{db_pass}';"
            create_db = f"CREATE DATABASE {db_name};"
            grant_privileges = f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
            flush_privileges = None

        else:
            raise ValueError("Database engine must be one of: mysql, postgresql, mariadb")
        

        self.queries = []
        self.queries.extend([create_user, create_db, grant_privileges, flush_privileges])


    def configure_db(self):
        
        for q in self.queries:
            if q is not None:
                command = self.db_command + [q]
                process = subprocess.run(command)
                process.check_returncode()
        print(f"""Configured database.
        Database: {self.db_name}
        User: {self.db_user}
        Password: {self.db_pass}""")


# installer = DBInstaller(title="PostgreSQL", version="", pkg_name="postgresql-14", db_engine="postgresql", db_name="testing1", db_user="testing", db_pass="test1234")

# if __name__ == "__main__":

#     installer.remove_service()
#     installer.configure_db()