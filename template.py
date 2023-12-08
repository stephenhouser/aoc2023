#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse

class Thing:
    """A class of generic things"""

    def __init__(self, text):
        self._parse_line(text)

    def _parse_line(self, text):
        """Parse text description of thing"""
        match = re.match(r'\d+', text)

    def __repr__(self):
        """Return REPL representation of the thing"""
        return str(self)

    def __str__(self):
        """Return string representation of the thing"""
        return f'Empty'

def load_file(filename: str) -> list[Thing]:
    """Load lines from file into a list of ITEMS
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return list(map(Thing, file.readlines()))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        things = load_file(filename)

        #
        # Part One
        #
        n_things = len(things)
        print(f'\tNumber of things: {n_things}')

        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
