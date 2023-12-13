#!/usr/bin/env python
"""
Advent of Code 2023 - Day 13:Point of Incidence 
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
import logging as log
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)
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

def reflections_line(row, candidates):
    """Returns possible reflections"""
    new_c = []
    for i in candidates:
        left = list(reversed(row[:i]))
        right = row[i:]
        #print(left, "   ", right)
        #print(list(map(lambda x: x[0]==x[1], zip(left, right))))
        if all(map(lambda x: x[0]==x[1], zip(left, right))):
            new_c.append(i)

    #print(new_c)
    return new_c

def count_reflections(island_map):
    # all columns are candidates
    col_mirrors = list(range(len(island_map[0])))
    for row in island_map:
        # narrows down candidates
        col_mirrors = reflections_line(row, col_mirrors)

    #row_mirrors = list(range(0, len(island_map)-1))
    row_mirrors = list(range(len(island_map)))
    for col in list(map(list, zip(*island_map))):
        row_mirrors = reflections_line(col, row_mirrors)

    cm = sum(col_mirrors)
    rm = sum(row_mirrors)
    return (rm * 100, cm)

def print_grid(grid):
    for r in grid:
        for c in r:
            print(c, end='')
        print()

def load_file(filename: str):
    """Load lines from file into ___
        
       filename: the file to read game descriptions from.
       returns: ...
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            map_blocks = file.read().split('\n\n')
            maps = []
            for block in map_blocks:
                this_map = []
                for line in block.split('\n'):
                    this_map.append(list(line))

                maps.append(this_map)

            return maps

    except FileNotFoundError:
        log.error('File %s not found.', filename)

    return []

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        maps = load_file(filename)

        #
        # Part One
        #
        reflections = list(map(count_reflections, maps))
        reflection_sum = [sum(x) for x in zip(*reflections)]
        ref_summary = reflection_sum[0] + reflection_sum[1]
        print(f'\tNumber of reflections: {ref_summary}') #29366

        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
