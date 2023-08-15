import sys
import os


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
    print(path, file_names, file=sys.stderr)
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
        raise ValueError(f"File {path} does not exist.")
    base_name = os.path.basename(path)
    format = base_name.split(".")[-1]
    if format == "yml":
        format = "yaml"
    return format
