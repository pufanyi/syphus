import io
import json
import pytest

import syphus.utils.yaml as yaml

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
    info = Info(info_dict)
    assert info.content == str(info_dict)
    info = Info(info_list)
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
