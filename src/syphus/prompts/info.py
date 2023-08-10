from typing import Any, Dict, List, Optional

import syphus.utils.yaml as yaml
import json


class Info(object):
    def __init__(
        self, info: Dict[str, Any] | List[Any] | str, *, id: Optional[str] = None
    ):
        self.id = id
        if type(info) == str:
            self.content = info
        else:
            try:
                self.content = yaml.dumps(info)
            except Exception:
                self.content = json.dumps(info)
