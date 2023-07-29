import json
from typing import List, Dict


class QAPair(object):
    """
    Represents a Question-Answer pair.

    Attributes:
        question (str): The question in the pair.
        answer (str): The answer corresponding to the question.
    """

    def __init__(self, question: str, answer: str):
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

    def from_dict(self, qa_pair_dict: Dict[str, str]):
        """
        Populates the QAPair object from a dictionary.

        Args:
            qa_pair_dict (dict): A dictionary containing 'question' and 'answer' keys.

        Returns:
            None
        """
        self.question = qa_pair_dict["question"]
        self.answer = qa_pair_dict["answer"]

    def __str__(self) -> str:
        """
        Returns a formatted JSON string of the QAPair object.

        Returns:
            str: A JSON string representing the QAPair object.
        """
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)


class InContextExample(object):
    """
    Represents an example containing a context and a list of QAPair objects.

    Attributes:
        context (str): The context for the example.
        qa_pairs (List[QAPair]): A list of QAPair objects containing questions and answers.
    """

    def __init__(self, context: str, qa_pairs: List[QAPair] = []):
        """
        Initializes a new InContextExample object.

        Args:
            context (str): The context for the example.
            qa_pairs (List[QAPair], optional): A list of QAPair objects containing questions and answers.
                Defaults to an empty list.
        """
        self.context = context
        self.qa_pairs = qa_pairs

    def to_dict(self) -> Dict[str, any]:
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
        self.qa_pairs.append(QAPair(question, answer))

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


class Prompts(object):
    """
    Represents a set of prompts, including a system message and a list of InContextExample objects.

    Attributes:
        system_message (str): The system message for the prompts.
        in_context_examples (List[InContextExample]): A list of InContextExample objects representing examples.
    """

    def __init__(
        self, system_message: str, in_context_examples: List[InContextExample] = []
    ):
        """
        Initializes a new Prompts object.

        Args:
            system_message (str): The system message for the prompts.
            in_context_examples (List[InContextExample], optional): A list of InContextExample objects representing examples.
                Defaults to an empty list.
        """
        self.system_message = system_message
        self.in_context_examples = in_context_examples

    def get_messages(self) -> List[Dict[str, str]]:
        """
        Gets a list of messages in the prompts, including system, user, and assistant messages.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each representing a message with 'role' and 'content' keys.
        """
        messages = [{"role": "system", "content": self.system_message}]
        for example in self.in_context_examples:
            messages.append({"role": "user", "content": example.context})
            messages.append(
                {"role": "assistant", "content": example.get_formatted_qa_pairs()}
            )
        return messages
