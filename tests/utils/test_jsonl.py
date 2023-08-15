import syphus.utils.jsonl as jsonl
import pytest
import json


@pytest.fixture
def jsonl_path():
    return "tests/data/sample_jsonl.jsonl"


@pytest.fixture
def jsonl_output_path():
    return "tests/test_output/sample_jsonl_output.jsonl"


@pytest.fixture
def sample_jsonl(jsonl_path):
    jsonl_input = []
    with open(jsonl_path, "r") as f:
        for line in f.readlines():
            jsonl_input.append(json.loads(line))
    return jsonl_input


def test_load(jsonl_path, sample_jsonl):
    test_input = list(jsonl.load(jsonl_path))
    assert test_input == sample_jsonl
    with open(jsonl_path, "r") as f:
        test_input = list(jsonl.load(f))
    assert test_input == sample_jsonl


def test_dump(jsonl_output_path, sample_jsonl):
    test_input = sample_jsonl
    jsonl.dump(test_input, jsonl_output_path)
    assert list(jsonl.load(jsonl_output_path)) == test_input
    with open(jsonl_output_path, "w") as f:
        jsonl.dump(test_input, f)
    assert list(jsonl.load(jsonl_output_path)) == test_input
