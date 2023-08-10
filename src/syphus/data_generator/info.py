from typing import Any, Dict, List

import syphus.utils.yaml as yaml
import json


class Info(object):
    def __init__(self, id: str, info: Dict[str, Any] | List[Any] | str):
        self.id = id
        self.info = info

    def get_info(self) -> str:
        if type(self.info) == str:
            return self.info
        else:
            try:
                return yaml.dumps(self.info)
            except Exception:
                return json.dumps(self.info)
