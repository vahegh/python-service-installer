from .utils.consts import NGINX_DEFAULT_CONF_PATH
from certbot.main import main as cert
from plumbum.cmd import rm


def configure_webserver(file_path, params):
    print(f"Configuring Nginx...")
    with open(NGINX_DEFAULT_CONF_PATH, 'r') as f:
        config = f.read()

    new_conf = config.format(**params)

    with open(file_path, 'w') as f:
        f.write(new_conf)


def configure_ssl(domain, email):
    print("Configuring SSL...")
    cert(["--nginx", "--redirect", "--agree-tos", "--no-eff-email", "--email", email, "-d", domain])


def remove_webserver_conf(nginx_file_path):
    print("Removing Nginx files...")
    rm(nginx_file_path, retcode = (0, 1))