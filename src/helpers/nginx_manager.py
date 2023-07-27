from ..utils.consts import NGINX_DEFAULT_CONF_PATH
from certbot.main import main as cert
from plumbum.cmd import rm, systemctl

def configure_nginx(file_path, domain, upstream_address):
    print(f"Configuring Nginx...")
    with open(NGINX_DEFAULT_CONF_PATH, 'r') as f:
        config = f.read()

    new_conf = config.format(domain=domain, upstream_address=upstream_address)

    with open(file_path, 'w') as f:
        f.write(new_conf)
    systemctl('reload', 'nginx', retcode = (0, 1))


def configure_ssl(domain, email):
    print("Configuring SSL...")
    cert(["--nginx", "--redirect", "--agree-tos", "--no-eff-email", "--email", email, "-d", domain])


def remove_webserver_conf(nginx_file_path):
    print("Removing Nginx files...")
    rm(nginx_file_path, retcode = (0, 1))
    systemctl('reload', 'nginx', retcode = (0, 1))