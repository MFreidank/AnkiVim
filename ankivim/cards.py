"""
Present user-friendly interface to write Anki-cards in VIM, importable into
anki(1) as text files.
"""
from os import makedirs, getenv
from os.path import abspath, exists as path_exists, join as path_join
from subprocess import check_call, CalledProcessError
import sys
import tempfile

import ankivim
from ankivim.errors import HeaderNotIntactError

# for python2+3 compatibility in file writing
if sys.version_info.major == 3:
    def write_file(file_handle, string):
        file_handle.write(string.encode("utf-8"))
else:
    def write_file(file_handle, string):
        file_handle.write(string)


draw_frame = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%\t\t\t\t\t\t%\n%\t\t\t\t\t\t%\n%\t\t\t{content}\t\t%\n%\t\t\t\t\t\t%\n%\t\t\t\t\t\t%\n%\t\t\t\t\t\t%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
""".format


def parse_qa(contents):
    """ Read front (question) and back (answer) of a new anki card from
        `contents_file`.

    Parameters
    ----------
    contents : string

    Returns
    -------
    (question, answer): (string, string) 2-tuple
        User-input for `question` and `answer` for the new card.

    Raises
    -------
    `HeaderNotIntactError` if user has modified the QUESTION/ANSWER headers
    that serve as markers during parsing.

    """

    question, answer = [], []
    header_lines = 0

    for line in contents.split("\n"):
        if line.startswith("%"):
            header_lines += 1
        elif 0 < header_lines < 15:
            question.append(line.replace('\n', "<br />"))
        elif header_lines > 8:
            answer.append(line.replace('\n', "<br />"))

    if header_lines < 8:
        raise HeaderNotIntactError(
            "You deleted header lines! "
            "The QUESTION and ANSWER markers must be kept intact, "
            "otherwise parsing fails."
        )
    return "<br />".join(question), "<br />".join(answer)


def editor_command(filename,
                   editor=getenv("EDITOR", "vim"),
                   # editor args below target vim 7.4, overwrite for other
                   # editor choices.
                   editor_args=(
                       # set cursor below headers
                       "-c {}".format(r'/\v\%\n\zs(^$|^[^\%]{1}.*$)'),
                       # use anki_vim snippets
                       "-c set filetype=anki_vim",
                       # latex syntax highlighting
                       "-c set syntax=tex",
                       # load anki-vim snippets for this buffer
                       '-c let b:UltiSnipsSnippetDirectories=["UltiSnips", "{snippet_directory}"]'.format(
                           snippet_directory=abspath(path_join(
                               ankivim.__path__[0],
                               "..",
                               "AnkiVim_snippets",
                               "UltiSnips",))),),):
    """
    Open `filename` using `editor` which is called with arguments
    `editor_args`.

    Parameters
    ----------
    filename : string
        (Full) path to a file to open.
    editor : string, optional
        (Full) path to an editor executable to use.
        Defaults to the result of calling `getenv("EDITOR", "vim")`,
        that is either environment variable $EDITOR if it is set
        with fallback "vim" if it is not.
    editor_args : tuple, optional
        Additional arguments to pass to `editor` upon calling.
        Defaults to a suggested sequence of default arguments for vim(1).

    Returns
    ----------
    editor_call : tuple
        Tuple that contains full call to `editor` with `editor_args`
        to open `filename`. Can directly be passed to `subprocess.call`.
    """

    return tuple([editor] + list(editor_args) + [filename])


def open_editor(filename,
                editor=getenv("EDITOR", "vim"),
                # editor args below target vim 7.4, overwrite for other
                # editor choices.
                editor_args=(
                    # set cursor below headers
                    "-c {}".format(r'/\v\%\n\zs(^$|^[^\%]{1}.*$)'),
                    # use anki_vim snippets
                    "-c set filetype=anki_vim",
                    # latex syntax highlighting
                    "-c set syntax=tex",
                    # load anki-vim snippets for this buffer
                    '-c let b:UltiSnipsSnippetDirectories=["UltiSnips", "{snippet_directory}"]'.format(
                        snippet_directory=abspath(path_join(
                            ankivim.__path__[0],
                            "..",
                            "AnkiVim_snippets",
                            "UltiSnips",))),),):
    """
    Open `filename` using `editor` which is called with arguments
    `editor_args`.

    Parameters
    ----------
    filename : string
        (Full) path to a file to open.
    editor : string, optional
        (Full) path to an editor executable to use.
        Defaults to the result of calling `getenv("EDITOR", "vim")`,
        that is either environment variable $EDITOR if it is set
        with fallback "vim" if it is not.
    editor_args : tuple, optional
        Additional arguments to pass to `editor` upon calling.
        Defaults to a suggested sequence of default arguments for vim(1).

    """
    call_command = editor_command(filename, editor, editor_args)
    try:
        check_call(call_command)
    except CalledProcessError:
        raise ValueError(
            "Failed to call editor '{editor}' on filename '{filename}'.\n "
            "Full call string was: {call}""".format(
                editor=editor, filename=filename, call=" ".join(call_command)
            )

        )


def create_card(deckpath, editor=getenv("EDITOR", "vim"),
                # editor args below target vim 7.4, overwrite for other
                # editor choices.
                editor_args=(
                    # set cursor below headers
                    "-c {}".format(r'/\v\%\n\zs(^$|^[^\%]{1}.*$)'),
                    # use anki_vim snippets
                    "-c set filetype=anki_vim",
                    # latex syntax highlighting
                    "-c set syntax=tex",
                    # load anki-vim snippets for this buffer
                    '-c let b:UltiSnipsSnippetDirectories=["UltiSnips", "{snippet_directory}"]'.format(
                        snippet_directory=abspath(path_join(
                            ankivim.__path__[0],
                            "..",
                            "AnkiVim_snippets",
                            "UltiSnips",))),),):
    """
    Create a new anki-card in deck at path `deckpath`, by appending new
    formatted content to deckpath/raw_cards.txt.

    Will create a new deck directory at `deckpath` if there is none yet.

    Parameters
    ----------
    deckpath : string
        Full path to a folder containing raw textual data that can be imported
        into anki(1) directly.
    editor : string, optional
        (Full) path to an editor executable to use.
        Defaults to the result of calling `getenv("EDITOR", "vim")`,
        that is either environment variable $EDITOR if it is set
        with fallback "vim" if it is not.
    editor_args : tuple, optional
        Additional arguments to pass to `editor` upon calling.
        Defaults to a suggested sequence of default arguments for vim(1).

    """

    if not path_exists(deckpath):
        makedirs(deckpath)

    qa_headers = "{question}{space}{answer}{space}".format(
        question=draw_frame(content="QUESTION"),
        answer=draw_frame(content="ANSWER\t"),
        space="\n\n\n",
    )

    with tempfile.NamedTemporaryFile(suffix='.anki_vim') as temporary_file:
        write_file(temporary_file, qa_headers)

        # flush to ensure Q/A headers are already in the file when we
        # open it in vim.
        temporary_file.flush()

        # Call vim, set the cursor below the "FRONT" header,
        # allow snippets for our new filetype, set the syntax highlighting
        # so that it supports latex highlighting.
        open_editor(
            filename=temporary_file.name, editor=editor, editor_args=editor_args
        )

        with open(temporary_file.name, 'r') as contents_file:
            contents = contents_file.read()

    has_no_user_input = contents == qa_headers

    if has_no_user_input:
        return False

    with open(path_join(deckpath, "raw_cards.txt"), "a") as f:
        question, answer = parse_qa(contents)
        f.writelines([question, "\t", answer, "\n"])

    return True
