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

    @field_validator("name")   
    def check_name(cls, name):
        try:
            client.containers.get(name)
            raise ContainerNameInUseError(f"Container with name '{name}' already exists.")
        
        except docker.errors.NotFound:
            return name

    def run_container(self):
        args = self.model_dump()
        container = client.containers.run(detach=True,**args)
        return f"""Successfully started container. 
    ID: {container.id}
    Name: {self.name}
"""
    def stop_container(self):
        container = client.containers.get(self.name)
        container.stop()