from models.basemodel import BinaryInstaller, PackageInstaller
import os
import subprocess
import json



class MysqlInstaller(PackageInstaller):
    def __init__(self, title: str, version: str, pkg_name: str):
        super().__init__(title, version, pkg_name)



class MattermostInstaller(BinaryInstaller):
    def __init__(self, title: str, version: str, file_name: str):
        super().__init__(title, version, file_name)
        self.version = version
        self.base_url = "https://releases.mattermost.com/{}/mattermost-{}-linux-amd64.tar.gz".format(version, version)
        self.file_name = file_name

    def check_installed(self):
        pass

    def pre_install(self):
        super().pre_install()


    def main_install(self):
        return super().main_install()
    
    def post_install(self):

        pkg_name = self.pkg_name
        datadir = "/opt/mattermost"

        db_driver = "postgres"
        mm_pass = "qwer4321"
        mm_port = "5432"


        os.mkdir(f'{datadir}/data')
        subprocess.run(['useradd', '--system', '--user-group', pkg_name])
        subprocess.run(['chown', '-R', f'{pkg_name}:{pkg_name}', datadir])
        subprocess.run(['chmod', '-R', 'g+w', datadir])

        with open(f"{datadir}/config/config.json", "w") as f:
            config = json.load(f)

        config['SqlSettings']['Drivername'] = db_driver
        config['SqlSettings']['Datasource'] = f"{db_driver}://{pkg_name}:{mm_pass}@db:{mm_port}/{pkg_name}?sslmode=disable&connect_timeout=10"
        config['ServiceSettings']['SiteURL'] = "mm.vahe.fun"


mattermost = MattermostInstaller()