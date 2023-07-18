from plumbum.cmd import sudo

SERVICE_BASE_DIR = "/opt"
SYSTEMD_BASE_DIR = "/etc/systemd/system"
NGINX_BASE_DIR = "/etc/nginx/conf.d"
NGINX_DEFAULT_CONF_PATH = "src/utils/nginx_default_conf"
CERT_BASE_DIR = "/etc/letsencrypt"

MYSQL_DB_COMMAND = sudo["mysql", "-e"]
POSTGRESQL_DB_COMMAND = sudo["-u", "postgres", "psql", "-c"]


MYSQL_CONF_COMMANDS = [
    "CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}';",
    "CREATE DATABASE {db_name};",
    "GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';",
    "FLUSH PRIVILEGES;"
]

MYSQL_REMOVE_COMMANDS = [
    "DROP DATABASE IF EXISTS {db_name};",
    "DROP USER IF EXISTS '{db_user}'@'localhost';"
]

POSTGRESQL_CONF_COMMANDS = [
    "CREATE USER {db_user} WITH PASSWORD '{db_pass}';",
    "CREATE DATABASE {db_name} OWNER {db_user};",
    "GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};",
    "GRANT USAGE, CREATE ON SCHEMA PUBLIC TO {db_user}"
]

POSTGRESQL_REMOVE_COMMANDS = [
    "DROP DATABASE IF EXISTS {db_name};",
    "REVOKE USAGE, CREATE ON SCHEMA PUBLIC FROM {db_user}",
    "DROP USER IF EXISTS {db_user};"
]


NGINX_PARAMS_APT = [
    {
        "title": "Nginx",
        "pkg_name": "nginx"
    },

    {
        "title": "Certbot",
        "pkg_name": "certbot"
    },

    {
        "title": "Python3-Certbot-Nginx",
        "pkg_name": "python3-certbot-nginx"
    }
]