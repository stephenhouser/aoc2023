#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse

class Thing:
    """A class of generic things"""

    def __init__(self, thing_line):
        self.line = None
        self._parse_line(thing_line)

    def _parse_line(self, thing_line):
        """Parse text description of thing"""
        self.line = thing_line

    def get_line(self):
        return self.line

    def __repr__(self):
        """Return REPL representation of the thing"""
        return str(self)

    def __str__(self):
        """Return string representation of the thing"""
        return self.line

def load_file(filename: str) -> list[Thing]:
    """Load lines from file into a list of ITEMS
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file_handle:
            return list(map(Thing, file_handle.readlines()))

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

        # Part One
        n_things = len(things)
        print(f'\tNumber of things: {n_things}')

        # Part Two
        n_chars = sum(map(len, map(Thing.get_line, things)))
        print(f'\tTotal number of characters: {n_chars}')

        print()

if __name__ == '__main__':
    main()
