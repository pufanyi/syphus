from syphus import QAPair, InContextExample, Prompts


sample_qa_pair = {
    "question": "What is the meaning of life?",
    "answer": "42",
}


def test_qa_pair_init():
    qa_pair = QAPair(sample_qa_pair["question"], sample_qa_pair["answer"])
    assert qa_pair.question == sample_qa_pair["question"]
    assert qa_pair.answer == sample_qa_pair["answer"]


def test_qa_pair_to_dict():
    qa_pair = QAPair(**sample_qa_pair)
    qa_pair.to_dict() == sample_qa_pair


def test_qa_pair_from_dict():
    qa_pair = QAPair(sample_qa_pair)
    assert qa_pair.question == sample_qa_pair["question"]
    assert qa_pair.answer == sample_qa_pair["answer"]
