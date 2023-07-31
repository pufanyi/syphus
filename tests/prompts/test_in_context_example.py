from syphus import prompts, in_context_example, qa_pair

import pytest
import json


@pytest.fixture
def get_test_in_context_example():
    test_prompt_path = "tests/data/dense_captions_prompt.yaml"
    test_prompt = prompts.read_yaml(test_prompt_path)
    return test_prompt.in_context_examples[0]


def test_add_qa_pair(get_test_in_context_example):
    test_example = get_test_in_context_example
    len_before = len(test_example.qa_pairs)
    test_example.add_qa_pair("test question", "test answer")
    len_after = len(test_example.qa_pairs)
    assert len_after == len_before + 1
    assert "test question" == test_example.qa_pairs[-1].question
    assert "test answer" == test_example.qa_pairs[-1].answer


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


def test_add_qa_pair(sample_in_context_example):
    example = sample_in_context_example
    assert len(example.qa_pairs) == 2

    example.add_qa_pair("What is 2 + 2?", "4")
    assert len(example.qa_pairs) == 3
    assert example.qa_pairs[-1].question == "What is 2 + 2?"
    assert example.qa_pairs[-1].answer == "4"


def test_to_dict(sample_in_context_example):
    example = sample_in_context_example
    example_dict = example.to_dict()

    assert isinstance(example_dict, dict)
    assert "context" in example_dict
    assert "qa_pairs" in example_dict
    assert example_dict["context"] == "This is the context."
    assert len(example_dict["qa_pairs"]) == 2
    assert isinstance(example_dict["qa_pairs"][0], dict)


def test_from_dict(sample_in_context_example):
    example = sample_in_context_example
    example_dict = example.to_dict()

    new_example = in_context_example.from_dict(example_dict)

    assert isinstance(new_example, in_context_example.InContextExample)
    assert new_example.context == example.context
    assert len(new_example.qa_pairs) == len(example.qa_pairs)
    for new_qa_pair, old_qa_pair in zip(new_example.qa_pairs, example.qa_pairs):
        assert new_qa_pair.question == old_qa_pair.question
        assert new_qa_pair.answer == old_qa_pair.answer


def test_get_formatted_qa_pairs(sample_in_context_example):
    example = sample_in_context_example
    formatted_qa_pairs = example.get_formatted_qa_pairs()

    assert isinstance(formatted_qa_pairs, str)
    assert "Question: What is the capital of France?" in formatted_qa_pairs
    assert "Answer: Paris" in formatted_qa_pairs
    assert "Question: Who wrote the play 'Hamlet'?" in formatted_qa_pairs
    assert "Answer: William Shakespeare" in formatted_qa_pairs


def test_str(sample_in_context_example):
    example = sample_in_context_example
    example_str = str(example)

    assert isinstance(example_str, str)
    assert json.loads(example_str) == example.to_dict()
