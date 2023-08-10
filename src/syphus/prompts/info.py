from typing import Any, Optional

import syphus.utils.yaml as yaml
import json


class Info(object):
    def __init__(
        self, info: Any, *, id: Optional[str] = None, converting_type: str = "str"
    ):
        self.id = id
        if converting_type == "str":
            self.content = str(info)
        elif converting_type == "yaml":
            self.content = yaml.dumps(info)
        elif converting_type == "json":
            self.content = json.dumps(info, indent=4)
        else:
            raise ValueError("Invalid converting type")
