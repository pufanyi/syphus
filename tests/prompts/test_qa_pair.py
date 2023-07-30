import yaml

from syphus import QAPair


with open("../data/dense_captions_prompt.yaml", "r") as f:
    sample_qa_pair = yaml.safe_load(f)["in_context_examples"][0]["assistant"][0]


def test_qa_pair_init():
    qa_pair = QAPair(sample_qa_pair["question"], sample_qa_pair["answer"])
    assert qa_pair.question == sample_qa_pair["question"]
    assert qa_pair.answer == sample_qa_pair["answer"]


def test_qa_pair_to_dict():
    qa_pair = QAPair(sample_qa_pair)
    qa_pair.to_dict() == sample_qa_pair


def test_qa_pair_from_dict():
    qa_pair = QAPair()
    qa_pair.from_dict(sample_qa_pair)
    assert qa_pair.question == sample_qa_pair["question"]
    assert qa_pair.answer == sample_qa_pair["answer"]
