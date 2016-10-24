#!/usr/bin/env/python
# -*- coding: iso-8859-15 -*-
import os


def update_zshrc():
    zshrc_path = os.path.expanduser("~/.zshrc")
    with open(zshrc_path, 'r') as f:
        new_lines = (["fpath=(~/.zsh/custom_completions $fpath)\n"] +
                     f.readlines())
    with open(zshrc_path, 'w') as f:
        f.writelines(new_lines)

update_zshrc()
