from typing import Any, Optional, Dict, Union, List, Tuple, Iterable

import syphus.utils.yaml as yaml
import json

from syphus.utils.file_format import auto_infer_single_file, get_loader_by_format


class Info(object):
    """
    Represents information content along with an optional ID.

    This class is designed to hold information content, which can be of various types. It provides the option to specify an ID for the information. The content can be converted to different formats, such as string, YAML, or JSON.

    Args:
        info (Any): The information content.
        id (Optional[str], optional): An optional identifier for the information. Defaults to None.
        converting_type (str, optional): The type of conversion to be applied to the information content. Can be "str", "yaml", or "json". Defaults to "str".

    Raises:
        ValueError: If an invalid converting type is provided.
    """

    def __init__(
        self, info: Any, *, id: Optional[str] = None, converting_type: str = "yaml"
    ):
        self.id = id
        if isinstance(info, str):
            self.content = info
        elif converting_type == "str":
            self.content = str(info)
        elif converting_type == "yaml":
            self.content = yaml.dumps(info)
        elif converting_type == "json":
            self.content = json.dumps(info, indent=4)
        else:
            raise ValueError("Invalid converting type")


def from_dict(
    info: Union[
        Dict[str, Any], List[Any], Tuple[str, Union[Dict[str, Any], List[Any]]]
    ],
    *,
    has_id: bool = False,
    mandatory_id: Optional[str] = None
) -> Info:
    """
    Creates an Info object from a dictionary, list, or tuple.

    This function creates an Info object from various types of data, such as dictionaries, lists, or tuples. The 'has_id' parameter specifies whether the data has an ID field, and 'mandatory_id' can be provided to forcefully assign an ID.

    Args:
        info (Union[Dict[str, Any], List[Any], Tuple[str, Union[Dict[str, Any], List[Any]]]]): The information data.
        has_id (bool, optional): Whether the information has an ID. Defaults to False.
        mandatory_id (Optional[str], optional): A mandatory identifier for the information. Overrides 'has_id'. Defaults to None.

    Returns:
        Info: An Info object representing the converted information.

    Raises:
        ValueError: If 'has_id' is True and the provided information is a list.
    """

    id = None

    if has_id:
        if isinstance(info, dict):
            id = info.get("id")
            info.pop("id")
        elif isinstance(info, list):
            raise ValueError("Cannot have an id for a list")
        elif isinstance(info, tuple):
            id = info[0]
            info = info[1]

    if mandatory_id:
        id = mandatory_id

    return Info(info, id=id)


def read_single(
    file_path: str,
    *,
    format: str = "auto",
    has_id: bool = False,
    mandatory_id: Optional[str] = None
) -> Info:
    """
    Reads a single Info object from a file.

    This function reads a single Info object from the specified file. The format of the file can be automatically inferred or explicitly provided.

    Args:
        file_path (str): The path to the file containing the information.
        format (str, optional): The format of the file. Defaults to "auto".
        has_id (bool, optional): Whether the information has an ID. Defaults to False.
        mandatory_id (Optional[str], optional): A mandatory identifier for the information. Overrides 'has_id'. Defaults to None.

    Returns:
        Info: The read Info object.
    """

    if format == "auto":
        format = auto_infer_single_file(file_path)
    loader = get_loader_by_format(format)
    with open(file_path, "r") as f:
        return from_dict(loader(f), has_id=has_id, mandatory_id=mandatory_id)


def load(file_path: str, *, format: str = "auto") -> Iterable[Info]:
    """
    Loads multiple Info objects from a file.

    This function loads multiple Info objects from the specified file. The format of the file can be automatically inferred or explicitly provided. The function returns an iterable of Info objects.

    Args:
        file_path (str): The path to the file containing the information.
        format (str, optional): The format of the file. Defaults to "auto".

    Yields:
        Info: An iterable of Info objects.
    """

    if format == "auto":
        format = auto_infer_single_file(file_path)
    loader = get_loader_by_format(format)
    with open(file_path, "r") as f:
        infos = loader(f)
        if isinstance(infos, dict):
            infos = infos.items()
        for info in infos:
            yield from_dict(info, has_id=True)


def to_dict(infos: Iterable[Info]) -> Dict[str, str]:
    """
    Convert Info objects to a dictionary.

    This function takes an iterable of Info objects and converts them into a dictionary where the keys are the IDs of the Info objects and the values are the content of the Info objects.

    Args:
        infos (Iterable[Info]): An iterable of Info objects.

    Returns:
        Dict[str, str]: A dictionary mapping Info IDs to their content.
    """
    infos_dict = {}
    for info in infos:
        infos_dict[info.id] = info.content
    return infos_dict
