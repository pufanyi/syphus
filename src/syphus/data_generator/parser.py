import syphus.prompts.qa_pair as qa_pair


def split_question_and_answer(pair_of_answer: str) -> qa_pair.QAPair:
    lines = pair_of_answer.strip().split("\n")
    question = None
    answer = None

    for line in lines:
        prefix, content = line.split(":", 1)
        if prefix.lower() == "question":
            question = content.strip()
        elif prefix.lower() == "answer":
            answer = content.strip()

    if question is None or answer is None:
        raise ValueError("Both Question and Answer are required.")

    return qa_pair.QAPair(question, answer)
