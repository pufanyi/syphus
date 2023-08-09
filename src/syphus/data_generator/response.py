from typing import Dict, Any

import syphus.prompts.qa_pair as qa_pair

import sys


class Response(object):
    def __init__(
        self,
        gpt_response: Dict[str, Any],
        *,
        question_header: str = "question: ",
        answer_header: str = "answer: ",
        ignore_capitalization: bool = True,
    ):
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
