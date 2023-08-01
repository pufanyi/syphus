import syphus.utils.yaml as yaml
from abc import ABC, abstractmethod


class Settings(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    def to_yaml(self):
        return yaml.dumps(self.to_dict())

    def save_yaml(self, yaml_path):
        yaml.dump(self.to_dict(), yaml_path)
