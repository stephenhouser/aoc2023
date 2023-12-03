#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
from functools import reduce


def parser(line: str):
    return line

def load_input(filename: str):
    """Load ___ from the given file
        
       filename: the file to read game descriptions from.
       returns: { 1:[(1, 2, 3), (5, 14, 12),...], 2:[...] }
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as gf:
            for line in gf.readlines():
                data.append(parser(line))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return data

#
# Part 1
#


#
# Part 2
#
