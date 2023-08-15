import pytest
import os

from syphus.utils.file_format import auto_infer_format, auto_infer_single_file


@pytest.fixture
def sample_files():
    return "tests/data/test_auto_infer_format/single"


def test_auto_infer_format(sample_files):
    path = str(sample_files)
    assert auto_infer_format(path, "file1", "file2") == "json"
    with pytest.raises(ValueError):
        auto_infer_format(path, "file1", "file3")
    with pytest.raises(ValueError):
        auto_infer_format(path, "file2", "file3")


def test_auto_infer_single_file(sample_files):
    path_json = str(os.path.join(sample_files, "file1.json"))
    path_yaml = str(os.path.join(sample_files, "file3.yml"))

    assert auto_infer_single_file(path_json) == "json"
    assert auto_infer_single_file(path_yaml) == "yaml"

    with pytest.raises(ValueError):
        auto_infer_single_file("nonexistent_file.json")
