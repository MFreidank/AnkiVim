"""
Present user-friendly interface to write Anki-cards in VIM, importable into
anki as text files.
"""
import sys
import tempfile
import os
from subprocess import call
delimiter_header = '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'


def drawFrame(content):
    center = '%\t\t\t' + content + '\t\t'
    delimiter_border = '\n%\t\t\t\t\t\t%\n%\t\t\t\t\t\t%\n' + center
    +'%\n%\t\t\t\t\t\t%' + '\n%\t\t\t\t\t\t%\n%\t\t\t\t\t\t%\n'
    return delimiter_header + delimiter_border + delimiter_header


def getQA(contents_file):
    contents_file.seek(0)
    question = ''
    answer = ''
    header_lines = 0
    for line in contents_file:
        # Note: we currently assume the headers to be there at all time.
        if line[0] == '%':
            header_lines += 1
        elif line[0] != '%' and 15 > header_lines > 0:
            question += line.replace('\n', '')
        elif line[0] != '%' and header_lines > 8:
            answer += line.replace('\n', '')
    if header_lines < 8:
        raise ValueError("""You deleted header lines! The FRONT and BACK
        markers must be kept intact, otherwise parsing fails.""")

    return (question, answer)


def createCard(deckpath):
    if not os.path.exists(deckpath):
        call(['mkdir', deckpath])
    qa_string = drawFrame('QUESTION') + '\n \n \n' + drawFrame('ANSWER\t')
    + '\n\n\n'
    with tempfile.NamedTemporaryFile(suffix='.anki_vim') as temp_file:
        temp_file.write(qa_string)
        temp_file.flush()
        # Call vim, set the cursor below the "FRONT" header,
        # allow snippets for our new filetype, set the syntax highlighting
        # so that it supports latex highlighting.
        call(['vim', '+9', '-c set filetype=anki_vim', '-c set syntax=tex',
              temp_file.name])
        with open(temp_file.name, 'r') as contentfile:
            file_contents = contentfile.read()
            if file_contents != qa_string:
                with open(deckpath + '/raw_cards.txt', 'a') as f:
                    question, answer = getQA(contentfile)
                    f.write(question)
                    f.write('\t')
                    f.write(answer)
                    f.write('\n')
                    return True
            else:
                return False


def main():
    if len(sys.argv) != 2:
        print 'USAGE: python create-card.py deckname[STRING]'
        exit(-1)
    deck = sys.argv[1]
    deckpath = os.path.abspath('./decks') + '/' + deck
    createCard(deckpath)


if __name__ == '__main__':
    main()
