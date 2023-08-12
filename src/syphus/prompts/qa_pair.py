import json
from typing import Dict


class QAPair(object):
    """
    Represents a Question-Answer pair.

    Attributes:
        question (str): The question in the pair.
        answer (str): The answer corresponding to the question.
    """

    def __init__(self, question: str = "", answer: str = ""):
        """
        Initializes a new QAPair object.

        Args:
            question (str): The question in the pair.
            answer (str): The answer corresponding to the question.
        """
        self.question = question
        self.answer = answer

    def to_dict(self) -> Dict[str, str]:
        """
        Converts the QAPair object to a dictionary.

        Returns:
            dict: A dictionary representation of the QAPair object.
        """
        return {"question": self.question, "answer": self.answer}

    def __str__(self) -> str:
        """
        Returns a formatted JSON string of the QAPair object.

        Returns:
            str: A JSON string representing the QAPair object.
        """
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def copy(self) -> "QAPair":
        """
        Returns a copy of the QAPair object.

        Returns:
            QAPair: A copy of the QAPair object.
        """
        return QAPair(self.question, self.answer)


def from_dict(data: Dict[str, str]) -> QAPair:
    """
    Initializes a new QAPair object from a dictionary.

    Args:
        data (Dict[str, str]): A dictionary containing the question and answer.

    Returns:
        QAPair: A new QAPair object.
    """
    return QAPair(data["question"], data["answer"])
