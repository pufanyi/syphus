import orjson
from typing import Any, Dict, Iterable


def load(path: str) -> Iterable[Dict[str, Any]]:
    """
    Load and parse a JSON file into an iterable of dictionaries.

    Args:
        path (str): The path to the JSON file.

    Yields:
        dict: A dictionary containing the parsed JSON data for each line in the file.

    Returns:
        Iterable[Dict[str, Any]]: An iterable of dictionaries, each representing a parsed JSON object from the file.
    """
    with open(path, "rb") as f:
        for line in f:
            yield orjson.loads(line)


def dump(data: Iterable[Dict[str, Any]], path: str):
    """
    Serialize and save a sequence of dictionaries as a JSON file.

    Args:
        data (Iterable[Dict[str, Any]]): An iterable of dictionaries to be serialized and saved.
        path (str): The path to save the JSON file.

    Notes:
        Each dictionary in the input sequence will be serialized and written as a separate line in the file.
    """
    with open(path, "wb") as f:
        for line in data:
            f.write(orjson.dumps(line) + b"\n")
