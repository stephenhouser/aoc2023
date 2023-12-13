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
import itertools

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('test.txt'), 405)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        self.assertEqual(test_function('input.txt'), 37718)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('test.txt', 1), 400)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('input.txt', 1), 40995)


def test_function(filename, smudges=0):
    """Loads sample data and calculates answer...
    """
    maps = load_file(filename)
    return sum((map(lambda x: count_reflections(x, smudges), maps)))

def count_reflections(island_map, smudges):
    (reflection_col, reflection_row) = find_reflections(island_map, smudges)
    return reflection_col * 100 + reflection_row

def find_reflections_single(line):
    """Returns all possible reflection points across a single line"""
    #print(line)
    reflections = []
    for i in range(1, len(line)):   # start at offset 1 to end of line
        left = list(reversed(line[:i]))
        right = line[i:]
        if all(map(lambda x: x[0]==x[1], zip(left, right))):
            reflections.append(i)

    return reflections

def find_reflections(island_map, smudges):
    """Returns calculated"""




    #
    # Vertical Mirrors
    #
    # possible vertical reflection points, one for each row
    reflections = map(find_reflections_single, island_map)
    # merge them into one flat list
    reflections = tuple(itertools.chain(*reflections))
    # make histogram buckets
    bins = tuple(map(reflections.count, range(len(island_map[0]))))
    # look for bin with len(row) elements for a mirror;
    #    this reflection occurs in every row
    # look for bin with len(row)-1 elements for a fixable mirror;
    #   this reflection occurs in all but one rows.
    #   if we fix the one, it will be a reflection
    look_for =  len(island_map) - smudges
    reflection_col = bins.index(look_for) if look_for in bins else 0

    #
    # Horizontal Mirrors
    #
    transposed_map =  tuple(map(list, zip(*island_map)))
    # possible horizontal reflection points, one for each row
    reflections = map(find_reflections_single, transposed_map)
    # merge them into one flat list
    reflections = tuple(itertools.chain(*reflections))
    # make histogram buckets
    bins = tuple(map(reflections.count, range(len(transposed_map[0]))))

    look_for = len(transposed_map) - smudges
    reflection_row = bins.index(look_for) if look_for in bins else 0

    return (reflection_row, reflection_col)

def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    for r in grid:
        for c in r:
            print(c, end='')
        print()

def load_file(filename: str):
    """Load lines from file into 2D list"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return tuple(map(lambda x: x.split('\n'), file.read().split('\n\n')))

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
        reflections = list(map(find_smudge, maps))
        reflection_sum = [sum(x) for x in zip(*reflections)]
        ref_summary = reflection_sum[0] + reflection_sum[1]
        print(f'\tNumber of reflections: {ref_summary}') #29366

        print()

if __name__ == '__main__':
    #main()
    unittest.main()
