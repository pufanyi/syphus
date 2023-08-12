from ruamel.yaml import YAML
from typing import Dict, Any
import io

yaml = YAML()


def dumps(data: Dict[Any, Any], **kw) -> str:
    """
    Convert a dictionary to a YAML-formatted string.

    Args:
        data (Dict[Any, Any]): The dictionary to be converted to YAML.
        **kw: Additional keyword arguments to be passed to the ruamel.yaml.dump function.

    Returns:
        str: A string containing the YAML-formatted representation of the input dictionary.
    """
    output_stream = io.StringIO()
    yaml.dump(data, output_stream, **kw)
    yaml_string = output_stream.getvalue()
    return yaml_string


def dump(data: Dict[Any, Any], file_name: str, **kw):
    """
    Serialize a dictionary to a YAML file.

    Args:
        data (Dict[Any, Any]): The dictionary to be serialized.
        file_name (str): The name of the file to save the YAML data to.
        **kw: Additional keyword arguments to be passed to the ruamel.yaml.dump function.

    Returns:
        None
    """
    with open(file_name, "w") as f:
        yaml.dump(data, f, **kw)


def loads(data: str, **kw) -> Dict[Any, Any]:
    """
    Parse a YAML-formatted string into a dictionary.

    Args:
        data (str): The YAML-formatted string to be parsed.
        **kw: Additional keyword arguments to be passed to the ruamel.yaml.load function.

    Returns:
        Dict[Any, Any]: A dictionary containing the parsed data from the YAML-formatted string.
    """
    return yaml.load(data, **kw)


def load(file_name: str, **kw) -> Dict[Any, Any]:
    """
    Load a YAML file and parse its contents into a dictionary.

    Args:
        file_name (str): The name of the YAML file to be loaded.
        **kw: Additional keyword arguments to be passed to the ruamel.yaml.load function.

    Returns:
        Dict[Any, Any]: A dictionary containing the parsed data from the YAML file.
    """
    with open(file_name, "r") as f:
        return yaml.load(f, **kw)


def equals(data1: str, data2: str) -> bool:
    """
    Compare two YAML-formatted strings for equality after parsing.

    Args:
        data1 (str): The first YAML-formatted string to be compared.
        data2 (str): The second YAML-formatted string to be compared.

    Returns:
        bool: True if the parsed dictionaries from both YAML strings are equal, False otherwise.
    """
    return loads(data1) == loads(data2)
