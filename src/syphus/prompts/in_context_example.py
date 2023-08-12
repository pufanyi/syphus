import json
import syphus.prompts.qa_pair as qa_pair
from syphus.prompts.info import Info
from typing import Dict, List, Any


class InContextExample(object):
    """
    Represents an example containing a context and a list of QAPair objects.

    Attributes:
        context (str): The context for the example.
        qa_pairs (List[QAPair]): A list of QAPair objects containing questions and answers.
    """

    def __init__(
        self,
        context: Any,
        qa_pairs: List[qa_pair.QAPair] = [],
    ):
        """
        Initializes a new InContextExample object.

        Args:
            context (Any): The context for the example.
            qa_pairs (List[QAPair], optional): A list of QAPair objects containing questions and answers.
                Defaults to an empty list.
        """
        self.context = Info(context).content
        self.qa_pairs = qa_pairs

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the InContextExample object to a dictionary.

        Returns:
            dict: A dictionary representation of the InContextExample object.
        """
        return {
            "context": self.context,
            "qa_pairs": [qa_pair.to_dict() for qa_pair in self.qa_pairs],
        }

    def __str__(self) -> str:
        """
        Returns a formatted JSON string of the InContextExample object.

        Returns:
            str: A JSON string representing the InContextExample object.
        """
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def add_qa_pair(self, question: str, answer: str):
        """
        Adds a new QAPair to the InContextExample.

        Args:
            question (str): The question in the pair.
            answer (str): The answer corresponding to the question.

        Returns:
            None
        """
        self.qa_pairs.append(qa_pair.QAPair(question, answer))

    def copy(self) -> "InContextExample":
        """
        Returns a copy of the InContextExample object.

        Returns:
            InContextExample: A copy of the InContextExample object.
        """
        return InContextExample(
            self.context, [qa_pair.copy() for qa_pair in self.qa_pairs]
        )

    def remove_last_qa_pair(self) -> qa_pair.QAPair:
        """
        Removes the last QAPair from the InContextExample.

        Returns:
            QAPair: The last QAPair in the InContextExample.
        """
        return self.qa_pairs.pop()

    def get_formatted_qa_pairs(self) -> str:
        """
        Formats the QAPair objects as a human-readable string.

        Returns:
            str: A formatted string containing questions and answers from the example.
        """
        formatted_qa_pairs = ""
        for qa_pair in self.qa_pairs:
            formatted_qa_pairs += (
                f"Question: {qa_pair.question}\nAnswer: {qa_pair.answer}\n\n"
            )
        return formatted_qa_pairs


def from_dict(data: Dict[str, Any]) -> InContextExample:
    """
    Initializes a new InContextExample object from a dictionary.

    Args:
        data (Dict[str, any]): A dictionary containing the context and list of QAPair objects.

    Returns:
        InContextExample: A new InContextExample object.
    """
    return InContextExample(
        data["context"], [qa_pair.from_dict(qa) for qa in data["qa_pairs"]]
    )
