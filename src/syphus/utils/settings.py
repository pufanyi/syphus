import syphus.utils.yaml as yaml
from abc import ABC, abstractmethod


class Settings(ABC):
    """
    Abstract base class for managing settings with YAML serialization support.

    This class defines methods for converting settings to dictionaries and YAML format, as well as
    saving settings to a YAML file.

    Subclasses must implement the `to_dict` method to provide the actual settings data.

    Attributes:
        None

    Methods:
        __init__(self): Constructor method for the Settings class.
        to_dict(self): Abstract method that must be implemented by subclasses to return settings as a dictionary.
        to_yaml(self): Convert the settings to YAML format.
        save_yaml(self, yaml_path): Save the settings to a YAML file.

    Example:
        class MySettings(Settings):
            def __init__(self, data):
                self.data = data

            def to_dict(self):
                return self.data

        settings = MySettings({"key": "value"})
        settings.save_yaml("settings.yaml")
    """

    def __init__(self):
        """
        Constructor for the abstract Settings class.

        Args:
            None

        Returns:
            None
        """
        pass

    @abstractmethod
    def to_dict(self):
        """
        Abstract method that must be implemented by subclasses to return settings as a dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the settings data.
        """
        pass

    def to_yaml(self):
        """
        Convert the settings to YAML format.

        Args:
            None

        Returns:
            str: A string representing the settings in YAML format.
        """
        return yaml.dumps(self.to_dict())

    def save_yaml(self, yaml_path):
        """
        Save the settings to a YAML file.

        Args:
            yaml_path (str): The path to the YAML file to save the settings to.

        Returns:
            None
        """
        yaml.dump(self.to_dict(), yaml_path)
