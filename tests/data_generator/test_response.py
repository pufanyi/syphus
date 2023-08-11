from syphus.data_generator.response import Response


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
