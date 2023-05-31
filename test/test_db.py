import subprocess

class DBInstaller():
    def __init__(self, db_engine: str, db_name: str, db_user: str, db_pass: str, db_port: int):

        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_engine = db_engine

        self.create_user = f"CREATE USER IF NOT EXISTS '{self.db_user}'@'localhost' IDENTIFIED BY '{self.db_pass}';"
        self.create_db = f"CREATE DATABASE IF NOT EXISTS {self.db_name};"
        self.grant_privileges = f"GRANT ALL PRIVILEGES ON {self.db_name}.* TO '{self.db_user}'@'localhost';"
        self.flush_privileges = "FLUSH PRIVILEGES;"

        self.queries = []
        self.queries.extend([self.create_user, self.create_db, self.grant_privileges, self.flush_privileges])

    def configure_db(self):
        for q in self.queries:
            process = subprocess.run(['mysql', '-e', q])
            process.check_returncode()
        print("Configured database.")


installer = DBInstaller("PostgreSQL", "testing1", "testing", "test1234", "3306")

installer.configure_db()