import docker
from pydantic import BaseModel, field_validator
from src.utils.exceptions import ContainerNameInUseError

client = docker.from_env()

class DockerInstaller(BaseModel):
    image: str
    name: str
    network: str = None
    volumes: dict = None
    environment: dict = None

    def __init__(self, **config):
        super().__init__(**config)
        if not self.name:
            self.name = self.image

    def install_service(self):
        try:
            client.containers.get(self.name)
        except docker.errors.NotFound:
            args = self.model_dump()
            container = client.containers.run(detach=True,**args)
            print(f"""Successfully started container 
        ID: {container.id}
        Name: {self.name}
    """)
        else:
            raise ContainerNameInUseError(f"Container '{self.name}' already exists")

    def remove_service(self):
        try:
            container = client.containers.get(self.name)
        except docker.errors.NotFound:
            print(f"Container '{self.name}' doesn't exist")
        else:
            container.remove(force=True)
            print(f"Removed container '{self.name}'")

    @property
    def status(self):
        try:
            container = client.containers.get(self.name)
        except docker.errors.NotFound:
            print(f"Container '{self.name}' doesn't exist")
        else:
            print(container.status)

    def stop_container(self):
        container = client.containers.get(self.name)
        container.stop()