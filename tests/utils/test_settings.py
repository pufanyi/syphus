import pytest
from syphus.utils.yaml import dumps

from syphus.utils.settings import Settings


@pytest.fixture
def settings_instance():
    class ConcreteSettings(Settings):
        def to_dict(self):
            return {
                "key1": "value1",
                "key2": "value2",
            }

    return ConcreteSettings()


def test_to_yaml(settings_instance):
    expected_yaml = dumps({"key1": "value1", "key2": "value2"})
    assert settings_instance.to_yaml() == expected_yaml


def test_save_yaml(settings_instance, mocker):
    mock_dump = mocker.patch("syphus.utils.yaml.dump")
    settings_instance.save_yaml("test.yaml")
    mock_dump.assert_called_once_with({"key1": "value1", "key2": "value2"}, "test.yaml")
