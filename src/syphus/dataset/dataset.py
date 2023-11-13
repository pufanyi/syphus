from typing import Union, Dict, List, Any
from PIL import Image

import syphus.utils.image_processor as image_processor

import datetime
import orjson
import pandas as pd


def get_date():
    current_date = datetime.date.today()
    return current_date.strftime("%Y-%m")


class Dataset(object):
    def __init__(
        self,
        name: str,
        short_name: Union[None, str] = None,
        *,
        author: str = "ntu",
        version: str = "0.0.1",
        date: Union[None, str] = None,
        max_zerofill: int = 8,
    ):
        self.name = name
        if short_name is None:
            self.short_name = name.upper()
        self.author = author
        if date is None:
            self.time = get_date()
        else:
            self.time = date
        self.version = version
        self.data = {}
        self.max_zerofill = max_zerofill
        self.images = {}

    def get_meta(self) -> Dict[str, str]:
        return {
            "version": self.version,
            "time": self.time,
            "author": self.author,
        }

    def clear(self):
        self.data = {}

    def update_data_by_list(self, data: List[Any]):
        for i, item in enumerate(data):
            index = str(i + len(self.data))
            id = f"{self.short_name}_INS_{index.zfill(self.max_zerofill)}"
            self.data[id] = item

    def update_data_by_dict(self, data: Dict[str, Any]):
        self.data.update(data)

    def update_data(self, data: Union[List[str], Dict[str, str]]):
        while len(data) + len(self.data) >= 10**self.max_zerofill:
            self.max_zerofill += 2
        if isinstance(data, list):
            self.update_data_by_list(data)
        elif isinstance(data, dict):
            self.update_data_by_dict(data)
        else:
            raise TypeError("data should be list or dict")

    def get_instruction_id(self, id: Union[str, None] = None) -> str:
        if id is None:
            id = str(len(self.data))
        if len(id) > 10**self.max_zerofill:
            max_zerofill += 2
        return f"{self.short_name}_INS_{id.zfill(self.max_zerofill)}"

    def add_single_instruction(
        self, data: Dict[str, Any], *, id: Union[str, None] = None
    ):
        id = self.get_instruction_id(id)
        self.data[id] = data
        return id

    def get_image_id(self, id: Union[str, None] = None) -> str:
        if id is None:
            id = str(len(self.images))
        return f"{self.short_name}_IMG_{id.zfill(self.max_zerofill)}"

    def add_image_by_path(self, image_path: str, *, id: Union[str, None] = None) -> id:
        id = self.get_image_id(id)
        self.images[id] = image_processor.get_image(image_path)
        return id

    def add_image_by_base64(self, image_base64: str, *, id: Union[str, None] = None):
        id = self.get_image_id(id)
        self.images[id] = image_base64
        return id

    def add_image_by_bytes(self, image_bytes: bytes, *, id: Union[str, None] = None):
        id = self.get_image_id(id)
        self.images[id] = image_processor.convert_image_to_base64(image_bytes)
        return id

    def add_image_by_pil_image(self, id: str, image: Image.Image):
        id = self.get_image_id(id)
        self.images[id] = image_processor.convert_pil_image_to_base64(image)
        return id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "meta": self.get_meta(),
            "data": self.data,
        }

    def save_instructions(self, path: str):
        with open(path, "wb") as f:
            f.write(orjson.dumps(self.to_dict()))

    def convert_ins_id(self, ins_id: Any) -> str:
        if type(ins_id) != str:
            ins_id = str(ins_id)
        return f"{self.short_name}_INS_{ins_id.zfill(self.max_zerofill)}"

    def save_images(self, ouput_file: str, *, format: str = "parquet"):
        format = format.lower()
        SUPPORTED_FORMAT = {"json", "csv", "parquet"}
        assert format in SUPPORTED_FORMAT, f"format should be one of {SUPPORTED_FORMAT}"
        if format == "json":
            with open(ouput_file, "wb") as f:
                f.write(orjson.dumps(self.images))
        elif format in {"csv", "parquet"}:
            data = pd.DataFrame.from_dict(
                self.images, orient="index", columns=["base64"]
            )
            if format == "csv":
                data.to_csv(ouput_file)
            elif format == "parquet":
                data.to_parquet(ouput_file)
