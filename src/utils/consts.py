from plumbum.cmd import mysql, sudo

service_base_dir = "/opt"
systemd_base_dir = "/etc/systemd/system"


mysql_db_command = mysql["-e"]
postgresql_db_command = sudo["-u", "postgres", "psql", "-c"]


mysql_conf_commands = [
    "CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}';",
    "CREATE DATABASE {db_name};",
    "GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';",
    "FLUSH PRIVILEGES;"
]

mysql_remove_commands = [
    "DROP DATABASE IF EXISTS {db_name};",
    "DROP USER IF EXISTS '{db_user}'@'localhost';"
]

postgresql_conf_commands = [
    "CREATE USER {db_user} WITH PASSWORD '{db_pass}';",
    "CREATE DATABASE {db_name} OWNER {db_user};",
    "GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};",
    "GRANT USAGE, CREATE ON SCHEMA PUBLIC TO {db_user}"
]

postgresql_remove_commands = [
    "DROP DATABASE IF EXISTS {db_name};",
    "REVOKE USAGE, CREATE ON SCHEMA PUBLIC FROM {db_user}",
    "DROP USER IF EXISTS {db_user};"
]