import pytest
from os.path import join as path_join, dirname

from ankivim.cards import draw_frame, editor_command, parse_qa
from ankivim.errors import HeaderNotIntactError

DATA_PATH = path_join(dirname(__file__), "data")


def test_draw_frame():
    question_frame = draw_frame(content="QUESTION")
    expected_output = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%						%
%						%
%			QUESTION		%
%						%
%						%
%						%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

    assert(question_frame == expected_output)

    answer_frame = draw_frame(content="ANSWER\t")
    expected_output = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%						%
%						%
%			ANSWER			%
%						%
%						%
%						%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
    assert(answer_frame == expected_output)


def test_editor_command_empty_args():
    editors = ("vim", "vi", "emacs", "nano")
    editor_args, filename = (), "test.txt"

    for editor in editors:
        cmd = editor_command(
            editor=editor, editor_args=editor_args, filename=filename
        )

        expected_cmd = tuple([editor] + list(editor_args) + [filename])
        assert cmd == expected_cmd


def test_emacs_args():
    editor = "emacs"
    filename = "test2.txt"
    editor_args = ("-nw",)

    cmd = editor_command(
        editor=editor, editor_args=editor_args, filename=filename
    )

    assert cmd == ("emacs", "-nw", filename)


def test_parse_qa_valid():
    contents_filename = path_join(DATA_PATH, "test_contents_parse_qa.txt")
    with open(contents_filename, "r") as f:
        contents = f.read()
    question, answer = parse_qa(contents)
    assert question == "testquestionline1<br />testquestionline2<br /><br />"
    assert answer == "<br />testanswerline1<br />testanswerline2<br />"


def test_parse_qa_headers_not_intact():
    with pytest.raises(HeaderNotIntactError):
        parse_qa("")
