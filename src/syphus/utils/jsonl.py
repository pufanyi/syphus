import json
import io
from typing import Any, Dict, Iterable, Union


def load(file: Union[str, io.IOBase]) -> Iterable[Dict[str, Any]]:
    """
    Load and parse a JSON file, yielding dictionaries for each non-empty line.

    This function accepts either a file path or an IOBase object and reads the file line by line. Each non-empty line is parsed as a JSON object and yielded as a dictionary.

    Args:
        file (Union[str, io.IOBase]): The path to the file or an IOBase object.

    Yields:
        Iterable[Dict[str, Any]]: A dictionary representing the parsed JSON object.

    Note:
        If you want to use IOBase objects, do not close the file before you are done with the returned iterator.

    Example:
        >>> with open("data.json", "r") as f:
        ...     for entry in load(f):
        ...         print(entry)
    """
    if isinstance(file, str):
        with open(file, "r") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)
    elif isinstance(file, io.IOBase):
        for line in file:
            if line.strip():
                yield json.loads(line)
    else:
        raise TypeError("file must be a path or an IOBase object")


def dump(data: Iterable[Dict[str, Any]], file: Union[str, io.IOBase]):
    """
    Serialize and write a sequence of dictionaries as JSON to a file.

    This function takes an iterable of dictionaries and writes each dictionary as a JSON object on a separate line in the specified file.

    Args:
        data (Iterable[Dict[str, Any]]): An iterable of dictionaries to be serialized.
        file (Union[str, io.IOBase]): The path to the file or an IOBase object.

    Example:
        >>> data = [{"key1": "value1"}, {"key2": "value2"}]
        >>> with open("output.json", "w") as f:
        ...     dump(data, f)
    """
    if isinstance(file, str):
        with open(file, "w") as f:
            for line in data:
                f.write(json.dumps(line) + "\n")
    elif isinstance(file, io.IOBase):
        for line in data:
            file.write(json.dumps(line) + "\n")
    else:
        raise TypeError("file must be a path or an IOBase object")
