#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from functools import reduce

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

            return file.read().strip().split(',')
            # read a list of Thing
            #return list(map(Thing, file.readlines()))

    except FileNotFoundError:
        log.error('File %s not found.', filename)

    return []

def e_hash(item):
    return reduce(lambda a, c: ((a+ord(c))*17)%256, item, 0)
    # ans = 0
    # for i in item:
    #     ans = ((ans +ord(i)) * 17) % 256

    # return ans


def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        sequence = load_file(filename)

        #
        # Part One
        #
        n_things = len(sequence)
        #print(f'\tNumber of things: {sequence}')

        e_hash('HASH')
        ans = reduce(lambda a, c: a+e_hash(c), sequence, 0)
        print(ans)
        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
