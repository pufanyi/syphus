from syphus import prompts, in_context_example, qa_pair

import yaml
import pytest


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


@pytest.fixture
def sample_qa_pairs():
    return [
        qa_pair.QAPair("What is the capital of France?", "Paris"),
        qa_pair.QAPair("Who wrote the play 'Hamlet'?", "William Shakespeare"),
    ]


@pytest.fixture
def sample_in_context_example(sample_qa_pairs):
    return in_context_example.InContextExample(
        "This is the context.", qa_pairs=sample_qa_pairs
    )


@pytest.fixture
def sample_prompts(sample_in_context_example):
    return prompts.Prompts(
        "System Message", in_context_examples=[sample_in_context_example]
    )


def test_get_messages(sample_prompts):
    prompts = sample_prompts
    messages = prompts.get_messages()

    assert isinstance(messages, list)
    assert len(messages) == 3
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "System Message"
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "This is the context."
    assert messages[2]["role"] == "assistant"
    assert "What is the capital of France?" in messages[2]["content"]
    assert "Paris" in messages[2]["content"]
    assert "Who wrote the play 'Hamlet'?" in messages[2]["content"]
    assert "William Shakespeare" in messages[2]["content"]


def test_copy(sample_prompts):
    prompts = sample_prompts
    prompts_copy = prompts.copy()

    assert prompts_copy.system_message == prompts.system_message
    assert len(prompts_copy.in_context_examples) == len(prompts.in_context_examples)
    for i, example in enumerate(prompts_copy.in_context_examples):
        assert example.context == prompts.in_context_examples[i].context
        assert len(example.qa_pairs) == len(prompts.in_context_examples[i].qa_pairs)
        for j, qa_pair in enumerate(example.qa_pairs):
            assert (
                qa_pair.question == prompts.in_context_examples[i].qa_pairs[j].question
            )
            assert qa_pair.answer == prompts.in_context_examples[i].qa_pairs[j].answer

    prompts_copy.system_message = "New System Message"
    assert prompts_copy.system_message != prompts.system_message
