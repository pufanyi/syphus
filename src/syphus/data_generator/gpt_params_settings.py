from syphus.utils.settings import Settings

import syphus.utils.yaml as yaml

from typing import List, Optional


class GPTParamsSettings(Settings):
    def __init__(
        self,
        *,
        temperature: float = 0.7,
        max_tokens: int = 3200,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        stop: Optional[List[str]] = None,
    ):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stop": self.stop,
        }


def read_yaml(yaml_path: str):
    gpt_params_settings_dict = yaml.load(yaml_path)["GPT_params"]
    return GPTParamsSettings(**gpt_params_settings_dict)
