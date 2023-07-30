import yaml
import json

from syphus import qa_pair


with open("tests/data/dense_captions_prompt.yaml", "r") as f:
    sample_qa_pair = yaml.safe_load(f)["in_context_examples"][0]["assistant"][0]


def test_qa_pair_init():
    qa = qa_pair.QAPair(sample_qa_pair["question"], sample_qa_pair["answer"])
    assert qa.question == sample_qa_pair["question"]
    assert qa.answer == sample_qa_pair["answer"]


def test_qa_pair_to_dict():
    qa = qa_pair.QAPair(**sample_qa_pair)
    assert qa.to_dict() == sample_qa_pair


def test_qa_pair_from_dict():
    qa = qa_pair.from_dict(sample_qa_pair)
    assert qa.question == sample_qa_pair["question"]
    assert qa.answer == sample_qa_pair["answer"]

def test_qa_pair_to_str():
    qa = qa_pair.QAPair(**sample_qa_pair)
    assert json.loads(str(qa)) == sample_qa_pair
