from ruamel.yaml import YAML
from typing import Dict, Any

import io


yaml = YAML()


def dumps(data: Dict[Any, Any], **kw):
    output_stream = io.StringIO()
    yaml.dump(data, output_stream, **kw)
    yaml_string = output_stream.getvalue()
    return yaml_string


def dump(data: Dict[Any, Any], file_name: str, **kw):
    with open(file_name, "w") as f:
        yaml.dump(data, f, **kw)


def loads(data: str, **kw):
    return yaml.load(data, **kw)


def load(file_name: str, **kw):
    with open(file_name, "r") as f:
        return yaml.load(f, **kw)


def equals(data1: str, data2: str):
    return loads(data1) == loads(data2)
