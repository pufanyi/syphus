from syphus import prompts

import yaml


with open("tests/data/dense_captions_prompt.yaml", "r") as f:
    prompt_dict = yaml.safe_load(f)


def test_read_yaml():
    prompt = prompts.read_yaml("tests/data/dense_captions_prompt.yaml")
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
    prompt = prompts.read_yaml("tests/data/dense_captions_prompt.yaml")
    prompt_yaml = prompt.to_yaml()
    assert yaml.safe_load(prompt_yaml) == prompt_dict
