#!/usr/bin/env python

"""
Using VIM to generate textfiles which are directly anki-importable.

Copyright (C) 2016 Moritz Freidank
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
must display the following acknowledgement:
This product includes software developed by the organization.
4. Neither the name of the organization nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY Moritz Freidank ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Moritz Freidank BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
import optparse
import os
import create_card


def main():
    usage = """anki-vim.py [options] """

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
    deckpath = os.path.abspath("./decks")+"/"+deck

    content_added = True
    while content_added:
        # If a card is closed without content or changes, stop
        content_added = createCard.createCard(deckpath)

if __name__ == '__main__':
    main()
