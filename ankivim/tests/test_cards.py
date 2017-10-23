from ankivim.cards import draw_frame, editor_command
from ankivim.errors import HeaderNotIntactError


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

        expected_cmd = [editor] + editor_args + [filename]
        assert cmd == expected_cmd


def test_emacs_args():
    editor = "emacs"
    filename = "test2.txt"
    editor_args = ("-nw",)

    cmd = editor_command(
        editor=editor, editor_args=editor_args, filename=filename
    )

    assert cmd == ("emacs", "-nw", filename)


# XXX: Test parsing qa
