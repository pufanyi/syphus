import pytest
import yaml
from syphus.data_generator import openai_settings


@pytest.fixture
def yaml_path():
    return "tests/data/gpt_info.example.yaml"


@pytest.fixture
def sample_settings(yaml_path):
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)["OpenAI_API"]


def test_open_ai_settings(sample_settings):
    settings = openai_settings.OpenAISettings(**sample_settings)

    assert settings.type == sample_settings["type"]
    assert settings.base == sample_settings["base"]
    assert settings.key == sample_settings["key"]
    assert settings.version == sample_settings["version"]
    assert settings.engine == sample_settings["engine"]


def test_read_yaml(yaml_path, sample_settings):
    settings = openai_settings.read_yaml(yaml_path)

    assert isinstance(settings, openai_settings.OpenAISettings)
    assert settings.type == sample_settings["type"]
    assert settings.base == sample_settings["base"]
    assert settings.key == sample_settings["key"]
    assert settings.version == sample_settings["version"]
    assert settings.engine == sample_settings["engine"]


def test_to_dict(yaml_path, sample_settings):
    assert openai_settings.read_yaml(yaml_path).to_dict() == sample_settings
