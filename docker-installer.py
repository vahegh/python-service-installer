import docker
from pydantic import BaseModel, validator
from typing import Optional
import json

with open('config.json', 'r') as f:
    configs = json.load(f)

client = docker.from_env()

class NameInUseError(Exception):
    def __init__(self, msg):
        self.msg = f'{self.__class__.__name__}: {msg}'
        super().__init__(self.msg)
    pass

class Service(BaseModel):
    image: str
    name: Optional[str]
    network: Optional[str] = None
    volumes: Optional[dict]
    environment: Optional[dict] = []

    def __init__(self, **config):
        super().__init__(**config)
        if not self.name:
            self.name = self.image
    
    @validator("name")   
    def check_name(cls, v):
        try:
            client.containers.get(v)
            raise NameInUseError(f"Container with name '{v}' already exists.")
        
        except docker.errors.NotFound:
            return v


    def run_container(self):
        container = client.containers.run(detach=True,**config)
        return f"""Successfully started container. 
    ID: {container.id}
    Name: {self.name}
"""

for config in configs:
    try:
        service = Service(**config)
        result = service.run_container() 
        print(result)

    except NameInUseError as e:
        print(e)

    except ValueError as e:
        print(e)