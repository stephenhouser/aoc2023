#!/usr/bin/env python
"""
Advent of Code 2023 - Day 20: Pulse Propagation
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
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('test.txt', 2), 0)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        self.assertEqual(test_function('input.txt', 200), 0)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('test.txt', 10), 0)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('input.txt', 1000000), 0)


def test_function(filename, *args):
    """Loads sample data and calculates answer...
    """
    stuff = load_file(filename)
    return len(stuff) * args[0]


class LogicNode:
    """Represents a ___"""
    def __init__(self, text):
        self.name = None
        self.state = False
        self.inputs = []
        self.outputs = []
        self._parse_line(text)

    def _parse_line(self, text):
        pass

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'{self.name}({self.inputs})->{self.state}'

def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    for row in grid:
        for col in row:
            print(col, end='')
        print()

def load_file(filename: str):
    """Load lines from file into ___
        
       filename: the file to read game descriptions from.
       returns: ...
    """
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
            print(f'\tNumber of things: {n_things}')

            #
            # Part Two
            #

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
