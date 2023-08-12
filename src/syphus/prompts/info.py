from typing import Any, Optional
import syphus.utils.yaml as yaml
import json


class Info(object):
    """
    Represents an information object with various converting options.

    Attributes:
        id (Optional[str]): An optional identifier for the information.
        content (str): The converted content of the information.
    """

    def __init__(
        self, info: Any, *, id: Optional[str] = None, converting_type: str = "str"
    ):
        """
        Initializes a new Info object.

        Args:
            info (Any): The information to be converted.
            id (Optional[str], optional): An optional identifier for the information.
            converting_type (str, optional): The type of conversion to be applied ("str", "yaml", or "json").
                Defaults to "str".

        Raises:
            ValueError: If an invalid converting type is provided.
        """
        self.id = id
        if converting_type == "str":
            self.content = str(info)
        elif converting_type == "yaml":
            self.content = yaml.dumps(info)
        elif converting_type == "json":
            self.content = json.dumps(info, indent=4)
        else:
            raise ValueError("Invalid converting type")
