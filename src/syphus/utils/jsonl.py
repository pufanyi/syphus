import orjson

from typing import Any, Dict, Iterable


def load(path: str) -> Iterable[Dict[str, Any]]:
    with open(path, "rb") as f:
        for line in f:
            yield orjson.loads(line)


def dump(data: Iterable[Dict[str, Any]], path: str):
    with open(path, "wb") as f:
        for line in data:
            f.write(orjson.dumps(line) + b"\n")
