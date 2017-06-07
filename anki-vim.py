#!/usr/bin/env python3

""" Using VIM to generate textfiles which are directly anki-importable.  """

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
import optparse
import os
import create_card


def main():
    usage = """anki-vim.py [options]

Using VIM to generate textfiles which are directly anki-importable."""

    fmt = optparse.IndentedHelpFormatter(max_help_position=50, width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    group = optparse.OptionGroup(parser, 'Arguments',
                                 """Options to specify card creation details.
                                 """)
    group.add_option('-d', '--deck', metavar='DECK',
                     help='Name of the deck we write these cards for.')
    parser.add_option_group(group)

    # Parse options
    options, _ = parser.parse_args()

    # If no options are specified, print the help page.
    if len(sys.argv) == 1:
            parser.print_help()
            return 1

    deck = options.deck
    deckpath = os.path.abspath("./decks") + "/" + deck

    content_added = True
    while content_added:
        # If a card is closed without content or changes, stop
        content_added = create_card.create_card(deckpath)


if __name__ == '__main__':
    main()
