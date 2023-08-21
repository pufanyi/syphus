import sys
import os
import json

from typing import Dict, Any, Optional, Tuple
from tqdm import tqdm

import syphus.prompts.qa_pair as qa_pair
import syphus.utils.yaml as yaml
import syphus.utils.jsonl as jsonl

from syphus.utils.file_format import auto_infer_format, get_loader_by_format, get_saver


def extend_name(name: str, format: str) -> str:
    """
    Extend the given filename if it doesn't already have the specified format extension.

    Args:
        name (str): The original filename.
        format (str): The desired file format extension.

    Returns:
        str: The extended filename with the specified format extension.
    """
    if name.endswith(format):
        return name
    else:
        return f"{name}.{format}"


def get_file_path_names(
    path: str,
    response_file_name: str,
    error_message_file_name: str,
    full_response_file_name: str,
    format: str,
) -> Tuple[str, str, str]:
    """
    Generate file paths for response, error message, and full response files.

    Args:
        path (str): The directory path where the files are located.
        response_file_name (str): The filename for the response file.
        error_message_file_name (str): The filename for the error message file.
        full_response_file_name (str): The filename for the full response file.
        format (str): The desired file format extension.

    Returns:
        Tuple[str, str, str]: A tuple of file paths for response, error message,
        and full response files.
    """
    error_message_path = os.path.join(
        path, extend_name(error_message_file_name, format)
    )
    response_path = os.path.join(path, extend_name(response_file_name, format))
    full_response_path = os.path.join(
        path, extend_name(full_response_file_name, format)
    )
    return response_path, error_message_path, full_response_path


class Response(object):
    """
    Represents GPT generated responses and manages question-answer pairs.

    This class encapsulates the handling of GPT-3 generated responses, specifically focusing on extracting question-answer pairs from the response content. It provides methods for initializing responses, processing question-answer pairs, and saving response data to files.

    Attributes:
        gpt_response (Optional[Dict[str, Any]]): The GPT response dictionary containing the assistant's generated response and related metadata.
        question_header (str): The prefix indicating the start of a question in the response message content.
        answer_header (str): The prefix indicating the start of an answer in the response message content.
        ignore_capitalization (bool): If True, headers are matched without considering capitalization. Otherwise, capitalization is considered.
        warning_message (List[str]): A list of warning messages generated during response processing, such as notifications about missing or mismatched question-answer pairs.
        qa_pairs (List[qa_pair.QAPair]): A list of QA pairs extracted from the response, where each pair consists of a question and its corresponding answer.
        full_response (Dict[str, Any]): The complete GPT-3 response dictionary, including the message content, role, and other metadata.

    Methods:
        __init__: Initialize the Response instance. This constructor can handle both existing data and GPT-3 response inputs.
        to_dict: Convert the Response instance to a dictionary representation, making it easy to serialize the instance data.
        save: Save the Response instance data to files. This method allows users to persist the extracted QA pairs, warning messages, and the full GPT-3 response in specified file formats (JSON or YAML).

    Note:
        - The class provides flexibility in initializing instances from GPT-3 responses or existing data, allowing users to seamlessly integrate the class into their workflows.
        - It automatically processes the response content to extract question-answer pairs, handling headers and formatting variations.
        - The `save` method enables users to save the instance data, making it convenient for further analysis and sharing with others.
    """

    def __init__(
        self,
        *,
        gpt_response: Optional[Dict[str, Any]] = None,
        question_header: str = "question:",
        answer_header: str = "answer:",
        ignore_capitalization: bool = True,
        data: Optional[Dict[str, Any]] = None,
        gpt_error_messages: Optional[str] = None,
    ):
        """
        Initialize a Response instance with GPT-3 generated responses and QA pairs.

        Args:
            gpt_response (Optional[Dict[str, Any]]): The GPT-3 response dictionary.
            question_header (str): The prefix indicating the start of a question.
            answer_header (str): The prefix indicating the start of an answer.
            ignore_capitalization (bool): Whether to ignore capitalization when matching headers.
            data (Optional[Dict[str, Any]]): Pre-existing data to initialize the instance.
            gpt_error_messages (Optional[str]): Error messages from GPT-3 if present.

        Raises:
            ValueError: If neither gpt_response nor gpt_error_messages are provided.
        """
        if data is not None:
            self.full_response = data["full_response"]
            self.warning_message = data["warning_message"]
            self.qa_pairs = [
                qa_pair.from_dict(qa_pair_dict) for qa_pair_dict in data["qa_pairs"]
            ]
            return
        elif gpt_response is None and gpt_error_messages is None:
            raise ValueError("Response is not given.")

        if gpt_error_messages:
            self.warning_message = ["GPT error messages: " + gpt_error_messages]
            self.qa_pairs = []
            self.full_response = {
                "error": gpt_error_messages,
            }
            return

        self.warning_message = []
        self.qa_pairs = []
        self.full_response = gpt_response
        question = None
        answer = None
        message = gpt_response["choices"][0]["message"]["content"]
        if gpt_response["choices"][0]["message"]["role"] != "assistant":
            self.warning_message.append("Response is not from assistant.")
        last = None

        def check_start_with(line, prefix) -> bool:
            if ignore_capitalization:
                return line.lower().startswith(prefix.lower())
            else:
                return line.startswith(prefix)

        for full_line in message.split("\n"):
            line = full_line.strip()
            if line == "":
                continue
            if check_start_with(line, question_header):
                if question and answer:
                    self.qa_pairs.append(qa_pair.QAPair(question, answer))
                    question = None
                    answer = None
                if question:
                    self.warning_message.append(
                        "There is a question without an answer: " + question
                    )
                question = line[len(question_header) :].strip()
                last = "question"
            elif check_start_with(line, answer_header):
                if question is None:
                    self.warning_message.append(
                        "There is an answer without a question: " + line
                    )
                else:
                    answer = line[len(answer_header) :].strip()
                    last = "answer"
            else:
                if last == "question":
                    question += "\n" + line
                elif last == "answer":
                    answer += "\n" + line
                else:
                    self.warning_message.append(
                        "There is a line which is not a question or answer: " + line
                    )
        if question and answer:
            self.qa_pairs.append(qa_pair.QAPair(question, answer))
            question = None
            answer = None
        if len(self.qa_pairs) == 0:
            if question:
                self.warning_message.append(
                    "There is a question without an answer: " + question
                )
            else:
                self.warning_message.append("There is no question and answer pair.")
        if question:
            self.warning_message.append(
                "There is a question without an answer: " + question
            )
        if self.warning_message:
            for warning in self.warning_message:
                print(warning, file=sys.stderr)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Response instance to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing warning messages, QA pairs, and full response.
        """
        return {
            "warning_message": self.warning_message,
            "qa_pairs": [qa_pair.to_dict() for qa_pair in self.qa_pairs],
            "full_response": self.full_response,
        }

    def save(
        self,
        path: str,
        *,
        response_file_name: str = "responses",
        error_message_file_name: str = "error_messages",
        full_response_file_name: str = "gpt_full_responses",
        format: str = "json",
    ):
        """
        Save the Response instance data to files.

        Args:
            path (str): The directory path to save the files.
            response_file_name (str): The filename for the response data.
            error_message_file_name (str): The filename for error messages.
            full_response_file_name (str): The filename for the full response.
            format (str): The format for saving data (json or yaml).

        Raises:
            ValueError: If an invalid format is provided.

        Note:
            This method will create the necessary directories if they do not exist.
        """
        if format not in ["json", "yaml"]:
            raise ValueError("Format must be json or yaml.")
        if not os.path.exists(path):
            os.makedirs(path)
        response_path, error_message_path, full_response_path = get_file_path_names(
            path,
            response_file_name,
            error_message_file_name,
            full_response_file_name,
            format,
        )
        dumper = get_saver(format)
        with open(error_message_path, "w") as f:
            dumper(self.warning_message, f)
        with open(response_path, "w") as f:
            qa_pairs_dict = [qa_pair.to_dict() for qa_pair in self.qa_pairs]
            dumper(qa_pairs_dict, f)
        with open(full_response_path, "w") as f:
            dumper(self.full_response, f)


def save_json(
    responses: Dict[str, Response],
    path: str,
    *,
    response_file_name: str = "responses",
    error_message_file_name: str = "error_messages",
    full_response_file_name: str = "gpt_full_responses",
    process_bar: bool = True,
):
    """
    Save response data, warning messages, and full responses to JSON files.

    Args:
        responses (Dict[str, Response]): A dictionary mapping response IDs to Response instances.
        path (str): The directory path to save the files.
        response_file_name (str): The filename for the response data.
        error_message_file_name (str): The filename for error messages.
        full_response_file_name (str): The filename for the full GPT-3 responses.
        process_bar (bool): If True, display a progress bar during saving.

    Note:
        This function creates necessary directories if they do not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    responses_dict = {}
    error_messages = {}
    full_responses = {}
    response_path, error_message_path, full_response_path = get_file_path_names(
        path,
        response_file_name,
        error_message_file_name,
        full_response_file_name,
        "json",
    )
    items = responses.items()
    if process_bar:
        items = tqdm(items, unit="response", desc="Saving responses")
    for id, response in items:
        response_dict = response.to_dict()
        responses_dict[id] = response_dict["qa_pairs"]
        error_messages[id] = response_dict["warning_message"]
        full_responses[id] = response_dict["full_response"]
    with open(error_message_path, "w") as f:
        json.dump(error_messages, f)
    with open(response_path, "w") as f:
        json.dump(responses_dict, f)
    with open(full_response_path, "w") as f:
        json.dump(full_responses, f)


def save_jsonl(
    responses: Dict[str, Response],
    path: str,
    *,
    response_file_name: str = "responses",
    error_message_file_name: str = "error_messages",
    full_response_file_name: str = "gpt_full_responses",
    process_bar: bool = True,
):
    """
    Save response data, warning messages, and full responses to JSONL files.

    Args:
        responses (Dict[str, Response]): A dictionary mapping response IDs to Response instances.
        path (str): The directory path to save the files.
        response_file_name (str): The filename for the response data.
        error_message_file_name (str): The filename for error messages.
        full_response_file_name (str): The filename for the full GPT-3 responses.
        process_bar (bool): If True, display a progress bar during saving.

    Note:
        This function creates necessary directories if they do not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    response_path, error_message_path, full_response_path = get_file_path_names(
        path,
        response_file_name,
        error_message_file_name,
        full_response_file_name,
        "jsonl",
    )
    responses_dict = []
    error_messages = []
    full_responses = []
    items = responses.items()
    if process_bar:
        items = tqdm(items, unit="response", desc="Saving responses")
    for id, response in items:
        response_dict = response.to_dict()
        response_dict["qa_pairs"] = {
            "id": id,
            "content": response_dict["qa_pairs"],
        }
        response_dict["warning_message"] = {
            "id": id,
            "content": response_dict["warning_message"],
        }
        response_dict["full_response"] = {
            "id": id,
            "content": response_dict["full_response"],
        }
        responses_dict.append(response_dict["qa_pairs"])
        error_messages.append(response_dict["warning_message"])
        full_responses.append(response_dict["full_response"])
    jsonl.dump(error_messages, error_message_path)
    jsonl.dump(responses_dict, response_path)
    jsonl.dump(full_responses, full_response_path)


def save_all(
    responses: Dict[str, Response],
    path: str,
    *,
    format: str = "json",
    response_file_name: str = "responses",
    error_message_file_name: str = "error_messages",
    full_response_file_name: str = "gpt_full_responses",
    process_bar: bool = True,
    split: bool = False,
):
    """
    Save response data in specified format to files.

    Args:
        responses (Dict[str, Response]): A dictionary mapping response IDs to Response instances.
        path (str): The directory path to save the files.
        format (str): The format for saving data (json or jsonl).
        response_file_name (str): The filename for the response data.
        error_message_file_name (str): The filename for error messages.
        full_response_file_name (str): The filename for the full GPT-3 responses.
        process_bar (bool): If True, display a progress bar during saving.
        split (bool): If True, save each response in separate subdirectories.

    Raises:
        ValueError: If an invalid format is provided.

    Note:
        This function creates necessary directories if they do not exist.
    """
    if split:
        if format not in ["json", "yaml"]:
            raise ValueError("Format must be json or yaml.")
        if not os.path.exists(path):
            os.makedirs(path)
        items = responses.items()
        if process_bar:
            items = tqdm(items, unit="response", desc="Saving responses")
        for id, response in items:
            now_path = os.path.join(path, id)
            os.makedirs(now_path)
            response.save(
                now_path,
                response_file_name=response_file_name,
                error_message_file_name=error_message_file_name,
                full_response_file_name=full_response_file_name,
                format=format,
            )
    else:
        if format == "json":
            saver = save_json
        elif format == "jsonl":
            saver = save_jsonl
        else:
            raise ValueError("format must be json or jsonl")
        saver(
            responses,
            path,
            response_file_name=response_file_name,
            error_message_file_name=error_message_file_name,
            full_response_file_name=full_response_file_name,
            process_bar=process_bar,
        )


def read_single(
    path: str,
    *,
    response_file_name: str = "responses",
    error_message_file_name: str = "error_messages",
    full_response_file_name: str = "gpt_full_responses",
    format: str = "auto",
) -> Response:
    """
    Read and construct a single Response instance from saved files.

    Args:
        path (str): The directory path containing the saved files.
        response_file_name (str): The filename for the response data.
        error_message_file_name (str): The filename for error messages.
        full_response_file_name (str): The filename for the full GPT-3 responses.
        format (str): The format for saving data (json or yaml), if it is "auto", try to infer from files.

    Returns:
        Response: A constructed Response instance based on the saved data.
    """
    if format == "auto":
        try:
            format = auto_infer_format(
                path,
                response_file_name,
                error_message_file_name,
                full_response_file_name,
            )
        except ValueError:
            raise FileNotFoundError(
                f"Cannot find files {response_file_name}, {error_message_file_name}, {full_response_file_name} in {path}, or cannot infer format automatically."
            )
    if format not in ["json", "yaml"]:
        raise ValueError("format must be json or yaml")
    response_path, error_message_path, full_response_path = get_file_path_names(
        path,
        response_file_name,
        error_message_file_name,
        full_response_file_name,
        format,
    )
    loader = get_loader_by_format(format)
    with open(error_message_path, "r") as f:
        error_message = loader(f)
    with open(response_path, "r") as f:
        qa_pairs = loader(f)
    with open(full_response_path, "r") as f:
        full_response = loader(f)
    return Response(
        data={
            "warning_message": error_message,
            "qa_pairs": qa_pairs,
            "full_response": full_response,
        }
    )


def read_all(
    path: str,
    *,
    response_file_name: str = "responses",
    error_message_file_name: str = "error_messages",
    full_response_file_name: str = "gpt_full_responses",
    format: str = "auto",
    split: bool = False,
    process_bar: bool = False,
) -> Dict[str, Response]:
    """
    Read and construct Response instances from saved files.

    Args:
        path (str): The directory path containing the saved files.
        response_file_name (str): The filename for the response data.
        error_message_file_name (str): The filename for error messages.
        full_response_file_name (str): The filename for the full GPT-3 responses.
        format (str): The format of saved data files (json or yaml). If it is "auto", try to infer from files.
        split (bool): If True, responses are stored in separate subdirectories.
        process_bar (bool): If True, display a progress bar during loading.

    Returns:
        Dict[str, Response]: A dictionary mapping response IDs to constructed Response instances.

    Note:
        - When split is True, this function loads responses from subdirectories.
        - When split is False, this function loads responses from a single set of files.
    """
    if split is False and process_bar is True:
        print("process_bar is only available when split is True", file=sys.stderr)
        print("process_bar is set to False", file=sys.stderr)
        process_bar = False

    if split:
        responses = {}
        responses_ids = os.listdir(path)
        if process_bar:
            responses_ids = tqdm(responses_ids, desc="Loading responses", unit="files")
        for id in responses_ids:
            try:
                response = read_single(
                    os.path.join(path, id),
                    response_file_name=response_file_name,
                    error_message_file_name=error_message_file_name,
                    full_response_file_name=full_response_file_name,
                    format=format,
                )
                responses[id] = response
            except FileNotFoundError as e:
                print(e, file=sys.stderr)
        return responses
    else:
        responses_dict = {}
        empty_response_dict = {
            "warning_message": [],
            "qa_pairs": [],
            "full_response": {},
        }
        if format == "auto":
            format = auto_infer_format(
                path,
                response_file_name,
                error_message_file_name,
                full_response_file_name,
            )
        response_path, error_message_path, full_response_path = get_file_path_names(
            path,
            response_file_name,
            error_message_file_name,
            full_response_file_name,
            format,
        )
        loader = get_loader_by_format(format)
        response_file = open(response_path, "r")
        error_message_file = open(error_message_path, "r")
        full_response_file = open(full_response_path, "r")
        qa_pairs = loader(response_file)
        error_messages = loader(error_message_file)
        full_responses = loader(full_response_file)
        if format == "json":
            for id, error_messages in error_messages.items():
                if id not in responses_dict:
                    responses_dict[id] = empty_response_dict.copy()
                responses_dict[id]["warning_message"] = error_messages
            for id, qa_pairs in qa_pairs.items():
                if id not in responses_dict:
                    responses_dict[id] = empty_response_dict.copy()
                responses_dict[id]["qa_pairs"] = qa_pairs
            for id, full_responses in full_responses.items():
                if id not in responses_dict:
                    responses_dict[id] = empty_response_dict.copy()
                responses_dict[id]["full_response"] = full_responses
        elif format == "jsonl":
            for error_message in error_messages:
                id = error_message["id"]
                if id not in responses_dict:
                    responses_dict[id] = empty_response_dict.copy()
                responses_dict[id]["warning_message"] = error_message["content"]
            for qa_pair in qa_pairs:
                id = qa_pair["id"]
                if id not in responses_dict:
                    responses_dict[id] = empty_response_dict.copy()
                responses_dict[id]["qa_pairs"] = qa_pair["content"]
            for full_response in full_responses:
                id = full_response["id"]
                if id not in responses_dict:
                    responses_dict[id] = empty_response_dict.copy()
                responses_dict[id]["full_response"] = full_response["content"]
        response_file.close()
        error_message_file.close()
        full_response_file.close()
        responses = {}
        for id, response_dict in responses_dict.items():
            responses[id] = Response(data=response_dict)
        return responses


def merge(
    input_path: str,
    output_path: str,
    *,
    input_format: str = "auto",
    input_response_file_name: str = "responses",
    input_error_message_file_name: str = "error_messages",
    input_full_response_file_name: str = "gpt_full_responses",
    output_format: str = "json",
    output_response_file_name: str = "responses",
    output_error_message_file_name: str = "error_messages",
    output_full_response_file_name: str = "gpt_full_responses",
    process_bar: bool = True,
) -> Dict[str, Response]:
    """
    Merge and re-save response data in different format.

    Args:
        input_path (str): The directory path containing the input response files.
        output_path (str): The directory path to save the merged and re-saved response files.
        input_format (str): The format of input response files (json or yaml). If it is auto, the program will try to infer the format.
        input_response_file_name (str): The filename for the input response data.
        input_error_message_file_name (str): The filename for input error messages.
        input_full_response_file_name (str): The filename for the input full GPT-3 responses.
        output_format (str): The format for saving output response files (json or jsonl).
        output_response_file_name (str): The filename for the output response data.
        output_error_message_file_name (str): The filename for output error messages.
        output_full_response_file_name (str): The filename for the output full GPT-3 responses.
        process_bar (bool): If True, display a progress bar during merging and saving.

    Returns:
        Dict[str, Response]: A dictionary mapping response IDs to Response instances.

    Note:
        - This function reads response data from input files, merges it, and re-saves the data in
          the specified output format.
    """
    responses = read_all(
        input_path,
        response_file_name=input_response_file_name,
        error_message_file_name=input_error_message_file_name,
        full_response_file_name=input_full_response_file_name,
        format=input_format,
        split=True,
        process_bar=process_bar,
    )
    save_all(
        responses,
        output_path,
        format=output_format,
        response_file_name=output_response_file_name,
        error_message_file_name=output_error_message_file_name,
        full_response_file_name=output_full_response_file_name,
        process_bar=process_bar,
    )
    return responses
