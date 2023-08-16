import os
import json
import pytest

import syphus.utils.yaml as yaml
import syphus.prompts.info as syphus_info

from syphus.prompts.info import Info

from typing import Any, Dict, List


@pytest.fixture
def info_dict() -> Dict[str, Any]:
    return {
        "key 1": "value 1",
        "key 2": "value 2",
        "key 3": {
            "key 3.1": "value 3.1",
            "key 3.2": "value 3.2",
            "key 3.3": {
                "key 3.3.1": "value 3.3.1",
                "key 3.3.2": "value 3.3.2",
            },
        },
        "key 4": [
            "value 4.1",
            "value 4.2",
        ],
    }


@pytest.fixture
def info_list() -> List[Any]:
    return [
        "value 1",
        {
            "key 2.1": "value 2.1",
            "key 2.2": "value 2.2",
        },
        [
            "value 3.1",
            "value 3.2",
        ],
    ]


def test_info_str(info_dict: Dict[str, Any], info_list: List[Any]):
    info = Info("This is a test info")
    assert info.content == "This is a test info"
    info = Info(info_dict, converting_type="str")
    assert info.content == str(info_dict)
    info = Info(info_list, converting_type="str")
    assert info.content == str(info_list)


def test_info_yaml(info_dict: Dict[str, Any], info_list: List[Any]):
    info = Info(info_dict, converting_type="yaml")
    assert yaml.loads(info.content) == info_dict
    info = Info(info_list, converting_type="yaml")
    assert yaml.loads(info.content) == info_list


def test_info_json(info_dict: Dict[str, Any], info_list: List[Any]):
    info = Info(info_dict, converting_type="json")
    assert json.loads(info.content) == info_dict
    info = Info(info_list, converting_type="json")
    assert json.loads(info.content) == info_list


def test_info_invalid_converting_type(info_dict: Dict[str, Any]):
    with pytest.raises(ValueError):
        Info(info_dict, converting_type="invalid converting type")


@pytest.fixture
def info_load_path() -> str:
    return "tests/data/test_info"


def test_read_single_info(info_load_path: str):
    data_path = os.path.join(info_load_path, "single_info", "john.json")
    info = syphus_info.read_single(data_path, has_id=True)
    with open(data_path, "r") as f:
        data = json.load(f)
    assert info.id == data["id"]
    info_content = yaml.loads(info.content)
    assert len(info_content) == 2
    assert info_content["name"] == data["name"]
    assert info_content["grade"] == data["grade"]


def test_read_multiple_infos(info_load_path: str):
    data_path = os.path.join(info_load_path, "multiple_infos")
    jsonl_data_path = os.path.join(data_path, "data.jsonl")
    json_dict_data_path = os.path.join(data_path, "data_dict.json")
    json_list_data_path = os.path.join(data_path, "data_list.json")
    info_dict = syphus_info.to_dict(syphus_info.load(json_dict_data_path))
    info_list = syphus_info.to_dict(syphus_info.load(json_list_data_path))
    info_jsonl = syphus_info.to_dict(syphus_info.load(jsonl_data_path))
    with open(json_dict_data_path, "r") as f:
        data_dict = json.load(f)
    assert (
        set(info_dict.keys())
        == set(info_list.keys())
        == set(info_jsonl.keys())
        == set(data_dict.keys())
    )
    for key in info_dict.keys():
        assert (
            yaml.loads(info_dict[key])
            == yaml.loads(info_list[key])
            == yaml.loads(info_jsonl[key])
            == data_dict[key]
        )
