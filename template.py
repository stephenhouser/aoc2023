#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile


class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Part 1 solution for test.txt"""
        things = load_file('test.txt')
        result = len(things)
        self.assertEqual(result, 10)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        things = load_file('input.txt')
        result = len(things)
        self.assertEqual(result, 10)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Part 2 solution for test.txt"""
        things = load_file('test.txt')
        result = len(things)
        self.assertEqual(result, 10)

    def test_part2_solution(self):
        """Part 2 solution for input.txt"""
        things = load_file('input.txt')
        result = len(things)
        self.assertEqual(result, 10)


class Thing:
    """Represents a ___"""
    def __init__(self, text):
        self._parse_line(text)

    def _parse_line(self, text):
        """Parse text description of ___"""
        match = re.match(r'\d+', text)

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'Empty'

def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    for row in grid:
        for col in row:
            print(col, end='')
        print()

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # read a grid of text into 2D grid
            return list(map(list,map(str.strip, file.readlines())))

            # read a list of Thing
            #return list(map(Thing, file.readlines()))

            # returns a dictionary indexed by i,j with c as the value
            # return {complex(i,j): c for j, r in enumerate(file)
            #                     for i, c in enumerate(r.strip())}

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            things = load_file(filename)

            #
            # Part One
            #
            n_things = len(things)
            print(f'\t1. Number of things: {n_things:,}')

            #
            # Part Two
            #
            # n_things = len(things)
            # print(f'\t2. umber of things: {n_things:,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
