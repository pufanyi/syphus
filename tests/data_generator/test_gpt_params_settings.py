import syphus.data_generator.gpt_params_settings as gpt_params_settings

import pytest
import os
import yaml


@pytest.fixture
def default_gpt_params_settings():
    return gpt_params_settings.GPTParamsSettings()


@pytest.fixture
def yaml_path():
    if os.path.exists("tests/data/gpt_info.yaml"):
        return "tests/data/gpt_info.yaml"
    else:
        return "tests/data/gpt_info.example.yaml"


def test_default_values(default_gpt_params_settings):
    assert default_gpt_params_settings.temperature == 0.7
    assert default_gpt_params_settings.max_tokens == 3200
    assert default_gpt_params_settings.top_p == 0.95
    assert default_gpt_params_settings.frequency_penalty == 0
    assert default_gpt_params_settings.presence_penalty == 0
    assert default_gpt_params_settings.stop is None


def test_to_dict(default_gpt_params_settings):
    expected_dict = {
        "temperature": 0.7,
        "max_tokens": 3200,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None,
    }
    assert default_gpt_params_settings.to_dict() == expected_dict


def test_custom_values():
    custom_gpt_params_settings = gpt_params_settings.GPTParamsSettings(
        temperature=0.5,
        max_tokens=500,
        top_p=0.9,
        frequency_penalty=1,
        presence_penalty=2,
        stop=["word1", "word2"],
    )

    assert custom_gpt_params_settings.temperature == 0.5
    assert custom_gpt_params_settings.max_tokens == 500
    assert custom_gpt_params_settings.top_p == 0.9
    assert custom_gpt_params_settings.frequency_penalty == 1
    assert custom_gpt_params_settings.presence_penalty == 2
    assert custom_gpt_params_settings.stop == ["word1", "word2"]


def test_custom_values_to_dict():
    custom_gpt_params_settings = gpt_params_settings.GPTParamsSettings(
        temperature=0.5,
        max_tokens=500,
        top_p=0.9,
        frequency_penalty=1,
        presence_penalty=2,
        stop=["word1", "word2"],
    )

    expected_dict = {
        "temperature": 0.5,
        "max_tokens": 500,
        "top_p": 0.9,
        "frequency_penalty": 1,
        "presence_penalty": 2,
        "stop": ["word1", "word2"],
    }
    assert custom_gpt_params_settings.to_dict() == expected_dict


def test_load_yaml(yaml_path):
    read_settings = gpt_params_settings.read_yaml(yaml_path)
    with open(yaml_path, "r") as yaml_path:
        actual_dict = yaml.safe_load(yaml_path)["GPT_params"]
    assert read_settings.to_dict() == actual_dict
