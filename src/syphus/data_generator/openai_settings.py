from syphus.utils.settings import Settings

import syphus.utils.yaml as yaml


class OpenAISettings(Settings):
    """
    Represents OpenAI API settings.

    This class is a subclass of the base Settings class and is specifically designed to
    encapsulate OpenAI API settings. It provides an initialization method to set the
    configuration parameters for making API requests.

    Attributes:
        type (str): The type of OpenAI instance (e.g., "local" or "remote").
        base (str): The base URL for making API requests.
        key (str): The API key used for authentication.
        version (str): The OpenAI API version to use.
        engine (str): The OpenAI engine to utilize for generating responses.

    Methods:
        __init__: Initialize the OpenAISettings instance with specified settings.
        to_dict: Convert the OpenAISettings instance to a dictionary representation.

    Note:
        This class inherits from the Settings base class and extends it with OpenAI-specific settings.
    """

    def __init__(
        self,
        *,
        type: str = "local",
        base: str = "http://localhost:8000",
        key: str = "",
        engine: str = "chatgpt0301",
    ):
        """
        Initialize the OpenAISettings instance with specified OpenAI settings.

        Args:
            type (str): The type of OpenAI instance (e.g., "local" or "remote").
            base (str): The base URL for making API requests.
            key (str): The API key used for authentication.
            engine (str): The OpenAI engine to utilize for generating responses.
        """
        self.type = type
        self.base = base
        self.key = key
        self.engine = engine

    def to_dict(self):
        """
        Convert the OpenAISettings instance to a dictionary representation.

        Returns:
            dict: A dictionary containing OpenAI settings attributes.
        """
        return {
            "type": self.type,
            "base": self.base,
            "key": self.key,
            "engine": self.engine,
        }


def read_yaml(yaml_path: str) -> OpenAISettings:
    """
    Read OpenAI API settings from a YAML file.

    Args:
        yaml_path (str): The path to the YAML file containing OpenAI API settings.

    Returns:
        OpenAISettings: An OpenAISettings instance initialized with the settings from the YAML file.
    """
    open_ai_settings_dict = yaml.load(yaml_path)["OpenAI_API"]
    return OpenAISettings(**open_ai_settings_dict)
