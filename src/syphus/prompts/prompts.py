import syphus.utils.yaml as yaml
import syphus.prompts.in_context_example as in_context_example
import syphus.prompts.qa_pair as qa_pair
from typing import List, Dict, Any


class Prompts(object):
    """
    Represents a set of prompts, including a system message and a list of InContextExample objects.

    Attributes:
        system_message (str): The system message for the prompts.
        in_context_examples (List[InContextExample]): A list of InContextExample objects representing examples.
    """

    def __init__(
        self,
        system_message: str,
        in_context_examples: List[in_context_example.InContextExample] = [],
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

    def to_dict(self) -> List[Dict[str, Any]]:
        """
        Converts the Prompts object to a dictionary.

        Returns:
            dict: A dictionary representation of the Prompts object.
        """
        return {
            "system_message": self.system_message,
            "in_context_examples": [
                example.to_dict() for example in self.in_context_examples
            ],
        }

    def get_yaml_dict(self) -> Dict[str, Any]:
        examples = []
        for example in self.in_context_examples:
            examples.append(
                {
                    "user": example.context,
                    "assistant": [qa.to_dict() for qa in example.qa_pairs],
                }
            )

        yaml_dict = {
            "system_message": self.system_message,
            "in_context_examples": examples,
        }
        return yaml_dict

    def to_yaml(self, **kw) -> str:
        """
        Converts the Prompts object to a YAML string.

        Returns:
            str: A YAML string representation of the Prompts object.
        """
        return yaml.dumps(self.get_yaml_dict(), **kw)

    def save_yaml(self, yaml_path: str, **kw):
        """
        Saves the Prompts object to a YAML file.

        Args:
            yaml_path (str): The path to save the YAML file to.
        """
        yaml.dump(self.get_yaml_dict(), yaml_path, **kw)

    def copy(self) -> "Prompts":
        """
        Returns a copy of the Prompts object.

        Returns:
            Prompts: A copy of the Prompts object.
        """
        return Prompts(
            self.system_message,
            [example.copy() for example in self.in_context_examples],
        )


def from_dict(data: Dict[str, Any]) -> Prompts:
    """
    Initializes a new Prompts object from a dictionary.

    Args:
        data (Dict[str, any]): A dictionary containing the system message and a list of InContextExample objects.

    Returns:
        Prompts: A new Prompts object.
    """
    return Prompts(
        data["system_message"],
        [
            in_context_example.from_dict(example)
            for example in data["in_context_examples"]
        ],
    )


def read_yaml(yaml_path) -> Prompts:
    """
    Reads a YAML file and initializes a Prompts object from its contents.

    Args:
        yaml_path (str): The path to the YAML file.

    Returns:
        Prompts: A new Prompts object.
    """
    prompts_data = yaml.load(yaml_path)
    examples = []
    for example in prompts_data["in_context_examples"]:
        examples.append(
            in_context_example.InContextExample(
                example["user"],
                [
                    qa_pair.QAPair(qa["question"], qa["answer"])
                    for qa in example["assistant"]
                ],
            )
        )
    return Prompts(prompts_data["system_message"], examples)
