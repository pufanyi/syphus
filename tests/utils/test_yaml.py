import syphus.utils.yaml as test_yaml
import yaml as standard_yaml


yaml_data_path = "tests/data/dense_captions_prompt.yaml"


def test_load_yaml():
    test_data = test_yaml.load(yaml_data_path)
    with open(yaml_data_path, "r") as f:
        standard_data = standard_yaml.safe_load(f)
    assert test_data == standard_data


def test_dump_yaml():
    with open(yaml_data_path, "r") as f:
        standard_data = standard_yaml.safe_load(f)
    test_output_path = "tests/test_output/test_dump_yaml.yaml"
    test_yaml.dump(standard_data, test_output_path)
    with open(test_output_path, "r") as f:
        test_data = standard_yaml.safe_load(f)
    assert test_data == standard_data


def test_loads_yaml():
    with open(yaml_data_path, "r") as f:
        standard_data = standard_yaml.safe_load(f)
    with open(yaml_data_path, "r") as f:
        test_data = test_yaml.loads(f.read())
    assert test_data == standard_data


def test_dumps_yaml():
    with open(yaml_data_path, "r") as f:
        standard_data = standard_yaml.safe_load(f)
    test_str = test_yaml.dumps(standard_data)
    assert standard_data == standard_yaml.safe_load(test_str)
