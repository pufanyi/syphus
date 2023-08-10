from typing import Dict, Any

import syphus.prompts.qa_pair as qa_pair
import syphus.utils.yaml as yaml
import syphus.utils.jsonl as jsonl

import sys
import os
import json


class Response(object):
    def __init__(
        self,
        gpt_response: Dict[str, Any],
        *,
        question_header: str = "question: ",
        answer_header: str = "answer: ",
        ignore_capitalization: bool = True,
    ):
        self.full_response = gpt_response
        self.warning_message = []
        question = None
        answer = None
        message = gpt_response["choices"][0]["message"]["content"]
        if gpt_response["choices"][0]["message"]["role"] != "assistant":
            self.warning_message.append("Response is not from assistant.")
        self.qa_pairs = []
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
                if question:
                    self.warning_message.append(
                        "There is a question without an answer: ", line
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

    def save_json(self, path: str):
        error_message_path = os.path.join(path, "error_message.json")
        response_path = os.path.join(path, "response.json")
        full_response_path = os.path.join(path, "gpt_full_response.json")
        with open(error_message_path, "w") as f:
            json.dump(self.warning_message, f, indent=4)
        with open(response_path, "w") as f:
            qa_pairs_dict = [qa_pair.to_dict() for qa_pair in self.qa_pairs]
            json.dump(qa_pairs_dict, f, indent=4)
        with open(full_response_path, "w") as f:
            json.dump(self.full_response, f, indent=4)

    def save_yaml(self, path: str):
        error_message_path = os.path.join(path, "error_message.yaml")
        response_path = os.path.join(path, "response.yaml")
        full_response_path = os.path.join(path, "gpt_full_response.yaml")
        yaml.dump(self.warning_message, error_message_path)
        yaml.dump([qa_pair.to_dict() for qa_pair in self.qa_pairs], response_path)
        yaml.dump(self.full_response, full_response_path)


def save_json(responses: Dict[str, Response], path: str):
    error_message_path = os.path.join(path, "error_messages.json")
    response_path = os.path.join(path, "responses.json")
    full_response_path = os.path.join(path, "gpt_full_responses.json")
    responses_dict = {}
    error_messages = {}
    full_responses = {}
    for id, response in responses.items():
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


def save_jsonl(responses: Dict[str, Response], path: str):
    error_message_path = os.path.join(path, "error_messages.jsonl")
    response_path = os.path.join(path, "responses.jsonl")
    full_response_path = os.path.join(path, "gpt_full_responses.jsonl")
    responses_dict = []
    error_messages = []
    full_responses = []
    for id, response in responses.items():
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
