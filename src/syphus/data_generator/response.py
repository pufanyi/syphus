import sys
import os
import json

from typing import Dict, Any, Optional, Tuple
from tqdm import tqdm

import syphus.prompts.qa_pair as qa_pair
import syphus.utils.yaml as yaml
import syphus.utils.jsonl as jsonl


def extend_name(name: str, format: str) -> str:
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
    error_message_path = os.path.join(
        path, extend_name(error_message_file_name, format)
    )
    response_path = os.path.join(path, extend_name(response_file_name, format))
    full_response_path = os.path.join(
        path, extend_name(full_response_file_name, format)
    )
    return response_path, error_message_path, full_response_path


class Response(object):
    def __init__(
        self,
        *,
        gpt_response: Optional[Dict[str, Any]] = None,
        question_header: str = "question: ",
        answer_header: str = "answer: ",
        ignore_capitalization: bool = True,
        data: Optional[Dict[str, Any]] = None,
        gpt_error_messages: Optional[str] = None,
    ):
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
                        "There is a question without an answer: " + line
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
                    "There is a question without an answer: " + line
                )
            else:
                self.warning_message.append("There is no question and answer pair.")
        if question:
            self.warning_message.append(
                "There is a question without an answer: " + line
            )
        if self.warning_message:
            for warning in self.warning_message:
                print(warning, file=sys.stderr)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "warning_message": self.warning_message,
            "qa_pairs": [qa_pair.to_dict() for qa_pair in self.qa_pairs],
            "full_response": self.full_response,
        }

    def save(
        self,
        path: str,
        *,
        response_file_name: str = "response",
        error_message_file_name: str = "error_message",
        full_response_file_name: str = "gpt_full_response",
        format: str = "json",
    ):
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
        if format == "json":
            with open(error_message_path, "w") as f:
                json.dump(self.warning_message, f, indent=4)
            with open(response_path, "w") as f:
                qa_pairs_dict = [qa_pair.to_dict() for qa_pair in self.qa_pairs]
                json.dump(qa_pairs_dict, f, indent=4)
            with open(full_response_path, "w") as f:
                json.dump(self.full_response, f, indent=4)
        elif format == "yaml":
            yaml.dump(self.warning_message, error_message_path)
            yaml.dump([qa_pair.to_dict() for qa_pair in self.qa_pairs], response_path)
            yaml.dump(self.full_response, full_response_path)


def save_json(
    responses: Dict[str, Response],
    path: str,
    *,
    response_file_name: str = "responses",
    error_message_file_name: str = "error_messages",
    full_response_file_name: str = "gpt_full_responses",
    process_bar: bool = True,
):
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
        response_dict["qa_pairs"]["id"] = id
        response_dict["warning_message"]["id"] = id
        response_dict["full_response"]["id"] = id
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
):
    if format == "json":
        save_json(
            responses,
            path,
            response_file_name=response_file_name,
            error_message_file_name=error_message_file_name,
            full_response_file_name=full_response_file_name,
            process_bar=process_bar,
        )
    elif format == "jsonl":
        save_jsonl(
            responses,
            path,
            response_file_name=response_file_name,
            error_message_file_name=error_message_file_name,
            full_response_file_name=full_response_file_name,
            process_bar=process_bar,
        )
    else:
        raise ValueError("format must be json, jsonl, or yaml")


def read_single(
    path: str,
    *,
    response_file_name: str = "response",
    error_message_file_name: str = "error_message",
    full_response_file_name: str = "gpt_full_response",
    format="json",
) -> Response:
    if format not in ["json", "yaml"]:
        raise ValueError("format must be json or yaml")
    response_path, error_message_path, full_response_path = get_file_path_names(
        path,
        response_file_name,
        error_message_file_name,
        full_response_file_name,
        format,
    )
    if format == "json":
        with open(error_message_path, "r") as f:
            error_message = json.load(f)
        with open(response_path, "r") as f:
            qa_pairs = json.load(f)
        with open(full_response_path, "r") as f:
            full_response = json.load(f)
    elif format == "yaml":
        error_message = yaml.load(error_message_path)
        qa_pairs = yaml.load(response_path)
        full_response = yaml.load(full_response_path)
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
    format: str = "json",
) -> Dict[str, Response]:
    response_path, error_message_path, full_response_path = get_file_path_names(
        path,
        response_file_name,
        error_message_file_name,
        full_response_file_name,
        format,
    )
    responses_dict = {}
    empty_response_dict = {"warning_message": [], "qa_pairs": [], "full_response": {}}
    if format == "json":
        with open(error_message_path, "r") as f:
            error_messages = json.load(f)
        with open(response_path, "r") as f:
            qa_pairs = json.load(f)
        with open(full_response_path, "r") as f:
            full_responses = json.load(f)
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
        error_messages = jsonl.load(error_message_path)
        qa_pairs = jsonl.load(response_path)
        full_responses = jsonl.load(full_response_path)
        for error_message in error_messages:
            id = error_message["id"]
            error_message.pop("id")
            if id not in responses_dict:
                responses_dict[id] = empty_response_dict.copy()
            responses_dict[id]["warning_message"] = error_message
        for qa_pair in qa_pairs:
            id = qa_pair["id"]
            qa_pair.pop("id")
            if id not in responses_dict:
                responses_dict[id] = empty_response_dict.copy()
            responses_dict[id]["qa_pairs"] = qa_pair
        for full_response in full_responses:
            id = full_response["id"]
            full_response.pop("id")
            if id not in responses_dict:
                responses_dict[id] = empty_response_dict.copy()
            responses_dict[id]["full_response"] = full_response
    responses = {}
    for id, response_dict in responses_dict.items():
        responses[id] = Response(data=response_dict)
    return responses


def merge(
    input_path: str,
    output_path: str,
    *,
    input_format: str = "json",
    input_response_file_name: str = "response",
    input_error_message_file_name: str = "error_message",
    input_full_response_file_name: str = "gpt_full_response",
    output_format: str = "json",
    output_response_file_name: str = "responses",
    output_error_message_file_name: str = "error_messages",
    output_full_response_file_name: str = "gpt_full_responses",
    process_bar: bool = True,
) -> Dict[str, Response]:
    responses = {}
    if process_bar:
        responses_ids = tqdm(
            os.listdir(input_path), desc="Loading responses", unit="files"
        )
    else:
        responses_ids = os.listdir(input_path)
    for id in responses_ids:
        try:
            response = read_single(
                os.path.join(input_path, id),
                response_file_name=input_response_file_name,
                error_message_file_name=input_error_message_file_name,
                full_response_file_name=input_full_response_file_name,
                format=input_format,
            )
            responses[id] = response
        except FileNotFoundError:
            print(f"File not found for {id}")
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
