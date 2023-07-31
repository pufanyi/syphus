from ruamel.yaml import YAML

import io


yaml = YAML()


def dumps(data, **kw):
    output_stream = io.StringIO()
    yaml.dump(data, output_stream, **kw)
    yaml_string = output_stream.getvalue()
    return yaml_string


def dump(data, file_name, **kw):
    with open(file_name, "w") as f:
        yaml.dump(data, f, **kw)


def loads(data, **kw):
    return yaml.load(data, **kw)


def load(file_name, **kw):
    with open(file_name, "r") as f:
        return yaml.load(f, **kw)
