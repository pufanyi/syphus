import sys
import os


def auto_infer_format(path: str, *file_names) -> str:
    """
    Automatically infer the file format based on file extensions and check if
    the given file names are present in the specified path.

    Args:
        path (str): The directory path to search for files.
        *file_names (str): Variable number of file names to check for.

    Returns:
        str: The inferred format if all specified file names are present with
             the same format, otherwise raises a ValueError.

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
