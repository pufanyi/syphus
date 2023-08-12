import syphus.data_generator.response as syphus_response

from syphus.data_generator.response import Response

import os
import pytest


def get_gpt_response(message: str, role: str = "assistant"):
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": message,
                    "role": role,
                },
            }
        ],
        "created": 1677664795,
        "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
        "model": "gpt-3.5-turbo-0613",
        "object": "chat.completion",
        "usage": {"completion_tokens": 17, "prompt_tokens": 57, "total_tokens": 74},
    }


def test_response_with_valid_input():
    response = Response(
        gpt_response=get_gpt_response(
            "question: Sample Question\nanswer: Sample Answer\n"
        )
    )
    assert len(response.qa_pairs) == 1
    assert response.qa_pairs[0].question == "Sample Question"
    assert response.qa_pairs[0].answer == "Sample Answer"


def test_response_with_no_question_and_answer(capsys):
    response = Response(gpt_response=get_gpt_response("998244353"))
    assert len(response.qa_pairs) == 0
    assert (
        "There is a line which is not a question or answer: 998244353"
        in response.warning_message
    )
    assert (
        "There is a line which is not a question or answer: 998244353"
        in capsys.readouterr().err
    )


def test_response_with_multiple_qa_pairs_but_partial_valid(capsys):
    response = Response(
        gpt_response=get_gpt_response(
            "anSWEr: Answer 1\nquEstion: Question 1\nansWer: Answer 2\nQUESTION: Question 2"
        )
    )
    assert len(response.qa_pairs) == 1
    assert response.qa_pairs[0].question == "Question 1"
    assert response.qa_pairs[0].answer == "Answer 2"
    assert len(response.warning_message) != 0
    assert len(capsys.readouterr().err) != 0


def test_response_with_multiple_qa_pairs_valid(capsys):
    response = Response(
        gpt_response=get_gpt_response(
            "QUESTION: Question 1\nansWEr: Answer 1\nquestioN: Question 2\nanSwer: Answer 2"
        )
    )
    assert len(response.qa_pairs) == 2
    assert response.qa_pairs[0].question == "Question 1"
    assert response.qa_pairs[0].answer == "Answer 1"
    assert response.qa_pairs[1].question == "Question 2"
    assert response.qa_pairs[1].answer == "Answer 2"
    assert len(response.warning_message) == 0
    assert capsys.readouterr().err == ""


def test_response_with_multiple_qa_pairs_valid_not_ignore_cap(capsys):
    response = Response(
        gpt_response=get_gpt_response(
            """
            questioN: Question 1
            anSwer: Answer 1
            question: Question 2
            answer: Answer 2
            """
        ),
        ignore_capitalization=False,
    )
    assert len(response.qa_pairs) == 1
    assert response.qa_pairs[0].question == "Question 2"
    assert response.qa_pairs[0].answer == "Answer 2"
    assert len(response.warning_message) != 0
    assert capsys.readouterr().err != ""


def test_response_with_missing_question():
    response = Response(
        gpt_response=get_gpt_response("answer: Answer without question")
    )
    assert len(response.qa_pairs) == 0
    assert "answer without a question" in response.warning_message[0]


def test_response_with_missing_answer(capsys):
    gpt_response = get_gpt_response("question: Question without answer")

    response = Response(gpt_response=gpt_response)
    assert len(response.qa_pairs) == 0
    assert "There is a question without an answer" in response.warning_message[0]
    assert "There is a question without an answer" in capsys.readouterr().err


def test_response_with_invalid_role(capsys):
    response = Response(
        gpt_response=get_gpt_response(
            "answer: Invalid Role Answer\nquestion: Invalid Role Question", role="user"
        )
    )
    assert len(response.qa_pairs) == 0
    assert "Response is not from assistant" in response.warning_message[0]
    assert "Response is not from assistant" in capsys.readouterr().err


def test_extend_name():
    assert syphus_response.extend_name("test.json", "json") == "test.json"
    assert syphus_response.extend_name("test", "json") == "test.json"
    assert syphus_response.extend_name("test", "yaml") == "test.yaml"
    assert syphus_response.extend_name("test", "yml") == "test.yml"


def test_get_file_path_names():
    path = "tests/data_generator/../data/./test_path"
    names = {
        "response_file_name": "response_file_name",
        "error_message_file_name": "error_message_file_name",
        "full_response_file_name": "full_response_file_name",
        "format": "jsonl",
    }
    answer = (
        "tests/data/test_path/response_file_name.jsonl",
        "tests/data/test_path/error_message_file_name.jsonl",
        "tests/data/test_path/full_response_file_name.jsonl",
    )
    answer1 = syphus_response.get_file_path_names(path, **names)
    answer2 = syphus_response.get_file_path_names(path + "/", **names)
    assert len(answer1) == len(answer) and len(answer2) == len(answer)
    for i in range(len(answer)):
        assert os.path.samefile(answer1[i], answer[i])
        assert os.path.samefile(answer2[i], answer[i])


def test_init_response_with_gpt_error_message():
    response = Response(
        gpt_error_messages="test_error_message",
    )
    assert len(response.warning_message) == 1
    assert "test_error_message" in response.warning_message[0]
    assert "error" in response.full_response
    assert response.qa_pairs == []


def test_init_response_with_all_None():
    with pytest.raises(ValueError):
        Response()


def test_init_response_with_dict():
    response_dict = {
        "full_response": get_gpt_response(
            message="""
                question1: Sample Question 1
                answer1: Sample Answer 1

                question2: Sample Question 2
                answer2: Sample Answer 2
                """
        ),
        "warning_message": ["test_warning_message"],
        "qa_pairs": [
            {"question": "Sample Question 1", "answer": "Sample Answer 1"},
            {"question": "Sample Question 2", "answer": "Sample Answer 2"},
        ],
    }
    response = Response(data=response_dict)
    assert response.full_response == response_dict["full_response"]
    assert response.warning_message == response_dict["warning_message"]
    assert [qa_pair.to_dict() for qa_pair in response.qa_pairs] == response_dict[
        "qa_pairs"
    ]


def test_init_response_with_question_without_answer(capsys):
    response = Response(
        gpt_response=get_gpt_response(
            message="""
            question: Question without answer
            question: question2
            answer: answer2
            """
        )
    )
    assert len(response.qa_pairs) == 1
    assert response.qa_pairs[0].question == "question2"
    assert response.qa_pairs[0].answer == "answer2"
    assert len(response.warning_message) == 1
    assert "There is a question without an answer" in response.warning_message[0]
    assert "There is a question without an answer" in capsys.readouterr().err


def test_init_response_with_multiple_lines_qa(capsys):
    response = Response(
        gpt_response=get_gpt_response(
            message="""
            question: Question 1 line 1\nQuestion 1 line 2\nQuestion 1 line 3
            answer: Answer 1 line 1\nAnswer 1 line 2\nAnswer 1 line 3
            question: Question 2 line 1\nQuestion 2 line 2\nQuestion 2 line 3
            answer: Answer 2 line 1\nAnswer 2 line 2\nAnswer 2 line 3
            """
        )
    )
    assert len(response.qa_pairs) == 2
    assert (
        response.qa_pairs[0].question
        == "Question 1 line 1\nQuestion 1 line 2\nQuestion 1 line 3"
    )
    assert (
        response.qa_pairs[0].answer
        == "Answer 1 line 1\nAnswer 1 line 2\nAnswer 1 line 3"
    )
    assert (
        response.qa_pairs[1].question
        == "Question 2 line 1\nQuestion 2 line 2\nQuestion 2 line 3"
    )
    assert (
        response.qa_pairs[1].answer
        == "Answer 2 line 1\nAnswer 2 line 2\nAnswer 2 line 3"
    )
    assert capsys.readouterr().err == ""
    assert len(response.warning_message) == 0


def test_to_dict():
    full_response = get_gpt_response(
        message="""
        question: Sample Question 1
        answer: Sample Answer 1

        question: Sample Question 2
        answer: Sample Answer 2

        question: Sample Question 3
        """
    )

    response = Response(gpt_response=full_response)
    qa_pairs = [
        {"question": "Sample Question 1", "answer": "Sample Answer 1"},
        {"question": "Sample Question 2", "answer": "Sample Answer 2"},
    ]
    assert response.to_dict() == {
        "full_response": full_response,
        "warning_message": response.warning_message,
        "qa_pairs": qa_pairs,
    }


@pytest.fixture
def sample_response():
    return Response(
        gpt_response=get_gpt_response(
            message="""
            question: Sample Question 1
            answer: Sample Answer 1

            question: Sample Question 2
            answer: Sample Answer 2

            question: Sample Question 3
            """
        )
    )


@pytest.fixture
def sample_response_output_path():
    return "tests/test_output/response"


def test_save_single_response_json(sample_response, sample_response_output_path):
    path = os.path.join(sample_response_output_path, "single_json")
    sample_response.save(path)
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(path, "response.json"))
    assert os.path.exists(os.path.join(path, "error_message.json"))
    assert os.path.exists(os.path.join(path, "gpt_full_response.json"))
    loaded_sample_response = syphus_response.read_single(path)
    assert sample_response.to_dict() == loaded_sample_response.to_dict()


def test_save_single_response_yaml(sample_response, sample_response_output_path):
    path = os.path.join(sample_response_output_path, "single_yaml")
    sample_response.save(path, format="yaml")
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(path, "response.yaml"))
    assert os.path.exists(os.path.join(path, "error_message.yaml"))
    assert os.path.exists(os.path.join(path, "gpt_full_response.yaml"))
    loaded_sample_response = syphus_response.read_single(path, format="yaml")
    assert sample_response.to_dict() == loaded_sample_response.to_dict()


def test_save_single_response_other_type(sample_response, sample_response_output_path):
    path = os.path.join(sample_response_output_path, "jsonl")
    with pytest.raises(ValueError):
        sample_response.save(path, format="other")