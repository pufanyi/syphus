from ruamel.yaml import YAML
from typing import Dict, Any, Union
import io


yaml = YAML()


def dumps(data: Dict[Any, Any], **kw) -> str:
    """
    Convert a dictionary to a YAML-formatted string.

    Args:
        data (Dict[Any, Any]): The dictionary to be converted to YAML.
        **kw: Additional keyword arguments to pass to the ruamel.yaml.dump function.

    Returns:
        str: The YAML-formatted string representing the input dictionary.
    """
    output_stream = io.StringIO()
    yaml.dump(data, output_stream, **kw)
    yaml_string = output_stream.getvalue()
    return yaml_string


def dump(data: Dict[Any, Any], file_name: Union[str, io.IOBase], **kw):
    """
    Write a dictionary to a YAML file.

    Args:
        data (Dict[Any, Any]): The dictionary to be written to the YAML file.
        file_name (Union[str, io.IOBase]): The name of the file or a file-like object to write to.
        **kw: Additional keyword arguments to pass to the ruamel.yaml.dump function.

    Raises:
        TypeError: If file_name is neither a string nor a file-like object.
    """
    if isinstance(file_name, str):
        with open(file_name, "w") as f:
            yaml.dump(data, f, **kw)
    elif isinstance(file_name, io.IOBase):
        yaml.dump(data, file_name, **kw)
    else:
        raise TypeError("file_name must be a string or a file-like object")


def loads(data: str, **kw) -> Dict[Any, Any]:
    """
    Parse a YAML-formatted string into a dictionary.

    Args:
        data (str): The YAML-formatted string to be parsed.
        **kw: Additional keyword arguments to pass to the ruamel.yaml.load function.

    Returns:
        Dict[Any, Any]: The dictionary parsed from the input YAML-formatted string.
    """
    return yaml.load(data, **kw)


def load(file: Union[str, io.IOBase], **kw) -> Dict[Any, Any]:
    """
    Load a dictionary from a YAML file.

    Args:
        file (Union[str, io.IOBase]): The name of the file or a file-like object to read from.
        **kw: Additional keyword arguments to pass to the ruamel.yaml.load function.

    Raises:
        TypeError: If file is neither a string nor a file-like object.

    Returns:
        Dict[Any, Any]: The dictionary parsed from the input YAML file.
    """
    if isinstance(file, str):
        with open(file, "r") as f:
            return yaml.load(f, **kw)
    elif isinstance(file, io.IOBase):
        return yaml.load(file, **kw)
    else:
        raise TypeError("file must be a string or a file-like object")


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
