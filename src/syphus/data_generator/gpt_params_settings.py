from syphus.utils.settings import Settings

import syphus.utils.yaml as yaml

from typing import List, Optional, Dict, Any


class GPTParamsSettings(Settings):
    """
    Represents settings for controlling GPT model behavior.

    This class is a subclass of the base Settings class and is designed to store various
    parameters that control the behavior of a GPT language model during text generation.

    Attributes:
        temperature (float): The temperature parameter affecting randomness of output.
        max_tokens (int): The maximum number of tokens in generated output.
        top_p (float): The cumulative probability threshold for selecting next tokens.
        frequency_penalty (float): The frequency penalty applied to encourage diversity.
        presence_penalty (float): The presence penalty applied to discourage repetition.
        stop (Optional[List[str]]): A list of custom tokens to stop generation on.

    Methods:
        __init__: Initialize the GPTParamsSettings instance with specified GPT parameters.
        to_dict: Convert the GPTParamsSettings instance to a dictionary representation.

    Note:
        This class inherits from the Settings base class and is used for fine-tuning GPT behavior.
    """

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
        """
        Initialize the GPTParamsSettings instance with specified GPT parameters.

        Args:
            temperature (float): The temperature parameter affecting randomness of output.
            max_tokens (int): The maximum number of tokens in generated output.
            top_p (float): The cumulative probability threshold for selecting next tokens.
            frequency_penalty (float): The frequency penalty applied to encourage diversity.
            presence_penalty (float): The presence penalty applied to discourage repetition.
            stop (Optional[List[str]]): A list of custom tokens to stop generation on.
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the GPTParamsSettings instance to a dictionary representation.

        Returns:
            dict: A dictionary containing GPT parameters.
        """
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stop": self.stop,
        }


def read_yaml(yaml_path: str) -> GPTParamsSettings:
    """
    Read GPT parameters settings from a YAML file.

    Args:
        yaml_path (str): The path to the YAML file containing GPT parameters settings.

    Returns:
        GPTParamsSettings: A GPTParamsSettings instance initialized with the settings
                          from the YAML file.
    """
    gpt_params_settings_dict = yaml.load(yaml_path)["GPT_params"]
    return GPTParamsSettings(**gpt_params_settings_dict)
