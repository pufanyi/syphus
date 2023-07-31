from syphus import prompts

import yaml


test_yaml_path = "tests/data/dense_captions_prompt.yaml"

with open(test_yaml_path, "r") as f:
    prompt_dict = yaml.safe_load(f)


def test_read_yaml():
    prompt = prompts.read_yaml(test_yaml_path)
    assert prompt.system_message == prompt_dict["system_message"]
    assert len(prompt.in_context_examples) == len(prompt_dict["in_context_examples"])
    for i, example in enumerate(prompt.in_context_examples):
        assert example.context == prompt_dict["in_context_examples"][i]["user"]
        assert len(example.qa_pairs) == len(
            prompt_dict["in_context_examples"][i]["assistant"]
        )
        for j, qa_pair in enumerate(example.qa_pairs):
            assert (
                qa_pair.question
                == prompt_dict["in_context_examples"][i]["assistant"][j]["question"]
            )
            assert (
                qa_pair.answer
                == prompt_dict["in_context_examples"][i]["assistant"][j]["answer"]
            )


def test_to_yaml():
    prompt = prompts.read_yaml(test_yaml_path)
    prompt_yaml = prompt.to_yaml()
    assert yaml.safe_load(prompt_yaml) == prompt_dict


def test_to_dict():
    prompt = prompts.read_yaml(test_yaml_path).to_dict()
    assert prompt["system_message"] == prompt_dict["system_message"]
    assert len(prompt["in_context_examples"]) == len(prompt_dict["in_context_examples"])
    for i, example in enumerate(prompt["in_context_examples"]):
        assert example["context"] == prompt_dict["in_context_examples"][i]["user"]
        assert len(example["qa_pairs"]) == len(
            prompt_dict["in_context_examples"][i]["assistant"]
        )
        for j, qa_pair in enumerate(example["qa_pairs"]):
            assert (
                qa_pair["question"]
                == prompt_dict["in_context_examples"][i]["assistant"][j]["question"]
            )
            assert (
                qa_pair["answer"]
                == prompt_dict["in_context_examples"][i]["assistant"][j]["answer"]
            )


def test_from_dict():
    prompt = prompts.read_yaml(test_yaml_path).to_dict()
    assert prompts.from_dict(prompt).to_dict() == prompt


def test_save_yaml():
    prompt = prompts.read_yaml(test_yaml_path)
    prompt_yaml_path = "tests/test_output/test_save_yaml.yaml"
    prompt.save_yaml(prompt_yaml_path)
    yaml.safe_load(prompt_yaml_path) == yaml.safe_load(test_yaml_path)
