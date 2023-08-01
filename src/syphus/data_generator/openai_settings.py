from syphus.utils.settings import Settings

import syphus.utils.yaml as yaml


class OpenAISettings(Settings):
    def __init__(
        self,
        *,
        type="local",
        base="http://localhost:8000",
        key="",
        version="2023-03-15",
        engine="chatgpt0301",
    ):
        self.type = type
        self.base = base
        self.key = key
        self.version = version
        self.engine = engine

    def to_dict(self):
        return {
            "type": self.type,
            "base": self.base,
            "key": self.key,
            "version": self.version,
            "engine": self.engine,
        }


def read_yaml(yaml_path: str):
    open_ai_settings_dict = yaml.load(yaml_path)["OpenAI_API"]
    return OpenAISettings(**open_ai_settings_dict)
