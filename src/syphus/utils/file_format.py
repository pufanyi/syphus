import sys
import os
import json
import shutil
import syphus.utils.yaml as yaml
import syphus.utils.jsonl as jsonl
from typing import Callable


def auto_infer_format(path: str, *file_names: str) -> str:
    """
    Automatically infers the file format based on file extensions and checks if
    the given file names are present in the specified path.

    This function iterates through the files in the specified directory path and
    groups them by their extensions. It then checks if the provided file names
    exist within the grouped formats. If all specified file names are present
    with the same format, that format is returned.

    Args:
        path (str): The directory path to search for files.
        *file_names (str): Variable number of file names to check for.

    Returns:
        str: The inferred format if all specified file names are present with
             the same format.

    Raises:
        ValueError: If the program cannot automatically determine the format or
                    if specified file names are not found in the path.

    Example:
        >>> auto_infer_format("/path/to/files", "file1", "file2")
        'json'
    """
    files_format = {}
    for file in os.listdir(path):
        format = file.split(".")[-1]
        if format == "yml":
            format = "yaml"
        file_name = ".".join(file.split(".")[:-1])
        if format not in files_format:
            files_format[format] = set()
        files_format[format].add(file_name)
    for format in files_format:
        for file_name in file_names:
            if file_name not in files_format[format]:
                break
        else:
            return format
    raise ValueError(
        f"In path {path}, the program cannot determine format automatically, please specify manually."
    )


def auto_infer_single_file(path: str) -> str:
    """
    Automatically infers the format of a single file based on its extension.

    This function extracts the extension of the provided file path and returns
    the corresponding format. If the extension is 'yml', it is considered as
    'yaml' format.

    Args:
        path (str): The path of the file to infer the format for.

    Returns:
        str: The inferred format of the file.

    Raises:
        ValueError: If the provided path does not correspond to an existing file.

    Example:
        >>> auto_infer_single_file("/path/to/file.json")
        'json'
    """
    if not os.path.isfile(path):
        raise ValueError(f"File {path} does not exist, or is not a file.")
    base_name = os.path.basename(path)
    format = base_name.split(".")[-1]
    if format == "yml":
        format = "yaml"
    return format


def get_loader_by_format(format: str) -> Callable:
    """
    Returns the appropriate loader function based on the provided file format.

    This function takes a file format as input and returns the corresponding loader function
    for that format. The supported formats are "json", "jsonl", "yaml", and "yml".

    Args:
        format (str): The file format for which to get the loader function.

    Returns:
        Callable: The loader function associated with the provided format.

    Raises:
        ValueError: If the specified format is not supported.

    Example:
        >>> loader = get_loader_by_format("json")
        >>> data = loader(open("data.json"))
    """
    if format == "json":
        return json.load
    elif format == "jsonl":
        return jsonl.load
    elif format == "yaml" or format == "yml":
        return yaml.load
    else:
        raise ValueError(f"Format {format} is not supported.")


def get_loader_by_path(path: str, *file_names: str) -> Callable:
    """
    Returns the appropriate loader function based on the provided path and file names.

    This function takes a directory path and a variable number of file names as input. It
    infers the file format based on the provided path and returns the corresponding loader
    function for that format. The file names are used for format inference when the path
    points to a directory.

    Args:
        path (str): The directory path to search for files.
        *file_names (str): Variable number of file names to assist in format inference.

    Returns:
        Callable: The loader function associated with the inferred format.

    Raises:
        ValueError: If the path does not exist or if the format cannot be inferred.

    Example:
        >>> loader = get_loader_by_path("/path/to/files", "file1", "file2")
        >>> data = loader(open("data.json"))
    """
    if os.path.isfile(path):
        format = auto_infer_single_file(path)
    elif os.path.isdir(path):
        format = auto_infer_format(path, *file_names)
    else:
        raise ValueError(f"Path {path} does not exist.")
    return get_loader_by_format(format)


def get_saver(format: str) -> Callable:
    """
    Returns a data saving function based on the specified format.

    This function takes a format as input and returns the appropriate data saving function based on the format.
    The supported formats are "json", "yaml"/"yml", and "jsonl".

    Args:
        format (str): The format of the data to be saved.

    Returns:
        Callable: The data saving function for the specified format.

    Raises:
        ValueError: If the provided format is not supported.

    Example:
        >>> saver = get_saver("json")
        >>> data = {"key": "value"}
        >>> with open("data.json", "w") as f:
        ...     saver(data, f)
    """

    if format == "json":
        return json.dump
    elif format == "yaml" or format == "yml":
        return yaml.dump
    elif format == "jsonl":
        return jsonl.dump
    else:
        raise ValueError(f"Format {format} is not supported.")


def remove_folder(path: str, *, force: bool = False):
    """
    Removes a folder at the specified path.

    This function removes the folder at the given path. If the 'force' parameter is set to True,
    it removes the folder and its contents recursively.

    Args:
        path (str): The path of the folder to be removed.
        force (bool, optional): If True, remove the folder and its contents. If False,
                               remove only if the folder is empty. Default is False.

    Example:
        >>> remove_folder("my_folder")
    """
    if os.path.exists(path):
        if force:
            shutil.rmtree(path)
        else:
            os.rmdir(path)


def create_output_folder(path: str, *, force: bool = False):
    """
    Creates an output folder at the specified path.

    This function creates a new output folder at the given path. If the 'force' parameter is set to True,
    it removes any existing folder at the path before creating a new one.

    Args:
        path (str): The path at which the output folder should be created.
        force (bool, optional): If True, remove any existing folder at the path before
                               creating the new folder. Default is False.

    Example:
        >>> create_output_folder("output", force=True)
    """
    remove_folder(path, force=force)
    os.makedirs(path)
