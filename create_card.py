"""
Present user-friendly interface to write Anki-cards in VIM, importable into
anki as text files.
"""
import os
from subprocess import call
import sys
import tempfile

# for python2+3 compatibility in file writing
if sys.version_info.major == 3:
    def write_file(file_handle, string):
        file_handle.write(string.encode("utf-8"))
else:
    def write_file(file_handle, string):
        file_handle.write(string)

python_three = sys.version_info.major == 3


def draw_frame(content):
    center = '%\t\t\t' + content + '\t\t'
    delim_header = '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    delim_border = "{0}{1}{2}{0}".format('\n%\t\t\t\t\t\t%\n%\t\t\t\t\t\t%\n',
                                         center, '%\n%\t\t\t\t\t\t%')
    return "{0}{1}{0}".format(delim_header, delim_border)


class HeaderNotIntactError(ValueError):
    """ QUESTION/ANSWER header was not left intact."""


def get_qa(contents_file):
    question = ''
    answer = ''
    header_lines = 0
    for line in contents_file:
        # Note: we currently assume the headers to be there at all time.
        if line[0] == '%':
            header_lines += 1
        elif line[0] != '%' and 15 > header_lines > 0:
            question += line.replace('\n', "<br />")
        elif line[0] != '%' and header_lines > 8:
            answer += line.replace('\n', "<br />")
    if header_lines < 8:
        raise HeaderNotIntactError("You deleted header lines!"
                                   "The QUESTION and ANSWER markers must "
                                   "be kept intact, otherwise parsing fails.")

    return (question, answer)


def has_no_user_input(filename, header):
    with open(filename, 'r') as contents_file:
        return contents_file.read() == header


def create_card(deckpath):
    if not os.path.exists(deckpath):
        call(['mkdir', "-p", deckpath])
    headers = "{0}{1}{2}{1}".format(draw_frame('QUESTION'), '\n\n\n',
                                    draw_frame('ANSWER\t'))
    with tempfile.NamedTemporaryFile(suffix='.anki_vim') as temp_file:
        write_file(temp_file, headers)

        # necessary to ensure headers are already in the temp file when
        # we open it in vim
        temp_file.flush()

        # Call vim, set the cursor below the "FRONT" header,
        # allow snippets for our new filetype, set the syntax highlighting
        # so that it supports latex highlighting.
        pattern = r'/\v\%\n\zs(^$|^[^\%]{1}.*$)'
        call(['vim', '-c {0}'.format(pattern),
              '-c set filetype=anki_vim',
              '-c set syntax=tex',
              temp_file.name])
        if has_no_user_input(temp_file.name, headers):
            return False

        with open(temp_file.name, 'r') as contentfile:
                with open(deckpath + '/raw_cards.txt', 'a') as f:
                    question, answer = get_qa(contentfile)
                    f.write(question)
                    f.write("\t")
                    f.write(answer)
                    f.write("\n")
                    return True
