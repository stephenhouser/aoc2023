#!/usr/bin/env python
"""
Advent of Code 2023 - Day 13:Point of Incidence 
Stephen Houser <stephenhouser@gmail.com>
"""

import argparse
import unittest
import itertools


class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(summarize_reflections('test.txt'), 405)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        self.assertEqual(summarize_reflections('input.txt'), 37718)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(summarize_reflections('test.txt', 1), 400)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(summarize_reflections('input.txt', 1), 40995)


def summarize_reflection(island_map, smudges):
    """Return the reflection summary for a single map"""
    reflection_row, reflection_col = find_reflection(island_map, smudges)
    return reflection_col * 100 + reflection_row

def summarize_reflections(filename, smudges=0):
    """Loads sample data file and returns summary answer
    """
    maps = load_file(filename)
    return sum((map(lambda x: summarize_reflection(x, smudges), maps)))

def find_reflections_single(line):
    """Returns all possible reflection points across a single line"""
    reflections = []
    for i in range(1, len(line)):   # start at offset 1 to end of line
        left = list(reversed(line[:i]))
        right = line[i:]
        if all(map(lambda x, y: x==y, left, right)):
            reflections.append(i)
        # if all(map(lambda x: x[0]==x[1], zip(left, right))):
        #     reflections.append(i)

    return reflections

def find_reflection(island_map, smudges):
    """Returns calculated (reflection_row, reflection_column)
        based on repairable `smudges`
    """

    result = []
    # Do this for the map and then the transposed map
    #   ...to get reflection row (vertical) and column (vertical)
    for island in (island_map, tuple(map(list, zip(*island_map)))):
        # possible vertical reflection points, one for each row
        reflections = map(find_reflections_single, island)
        # merge them into one flat list
        reflections_flat = tuple(itertools.chain(*reflections))
        # make histogram buckets
        bins = tuple(map(reflections_flat.count, range(len(island[0]))))
        # look for bin with len(row) elements for a mirror;
        #    this reflection occurs in every row
        # look for bin with len(row)-1 elements for a fixable mirror;
        #   this reflection occurs in all but one rows.
        #   if we fix the one, it will be a reflection
        look_for =  len(island) - smudges
        reflection_col = bins.index(look_for) if look_for in bins else 0

        result.append(reflection_col)

    return result

def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    for row in grid:
        for col in row:
            print(col, end='')
        print()

def load_file(filename: str):
    """Load lines from file into 2D list"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return tuple(map(lambda x: x.split('\n'), file.read().split('\n\n')))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        maps = load_file(filename)

        # Part One
        summary = sum((map(lambda x: summarize_reflection(x, 0), maps)))
        print(f'\t1. Number of reflections (no fixes)    : {summary}')

        # Part Two
        summary = sum((map(lambda x: summarize_reflection(x, 1), maps)))
        print(f'\t2. Number of reflections (fixed smudge): {summary}')

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
