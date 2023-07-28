import json

from typing import List, Dict


class QAPair(object):
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        return {"question": self.question, "answer": self.answer}

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)


class InContextExample(object):
    def __init__(self, context: str, qa_pairs: List[QAPair] = []):
        self.context = context
        self.qa_pairs = qa_pairs

    def to_dict(self):
        return {
            "context": self.context,
            "qa_pairs": [qa_pair.to_dict() for qa_pair in self.qa_pairs],
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def add_qa_pair(self, question: str, answer: str):
        self.qa_pairs.append(QAPair(question, answer))

    def get_formatted_qa_pairs(self) -> str:
        formatted_qa_pairs = ""
        for qa_pair in self.qa_pairs:
            formatted_qa_pairs += (
                f"Question: {qa_pair.question}\nAnswer: {qa_pair.answer}\n\n"
            )
        return formatted_qa_pairs


class Prompts(object):
    def __init__(
        self, system_message: str, in_context_examples: List[InContextExample] = []
    ):
        self.system_message = system_message
        self.in_context_examples = in_context_examples

    def get_messages(self) -> List[Dict[str, str]]:
        messages = [{"role": "system", "content": self.system_message}]
        for example in self.in_context_examples:
            messages.append({"role": "user", "content": example.context})
            messages.append(
                {"role": "assistant", "content": example.get_formatted_qa_pairs()}
            )
        return messages
