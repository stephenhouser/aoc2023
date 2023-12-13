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
    reflections = []
    for i in candidates:
        left = list(reversed(row[:i]))
        right = row[i:]
        if all(map(lambda x: x[0]==x[1], zip(left, right))):
            reflections.append(i)

    return reflections

def repair_map(island_map, smudge):
    (sx, sy) = smudge


def find_smudge(island_map):
    print()

    cm = 0
    rm = 0

    col_n = len(island_map[0])
    row_n = len(island_map)

    col_mirrors = range(1, col_n)
    cols = []
    #print('COLS')
    for row in island_map:
        # narrows down candidates
        refs = reflections_line(row, col_mirrors)
        print(row, refs)
        cols.extend(reflections_line(row, col_mirrors))

    # smudge would be row with len(island_map[0]) occurrences
    col_bins = list(map(cols.count, range(len(island_map[0]))))
    # if the smudge were fixed this is where the mirror would be
    if row_n-1 in col_bins:
        cm = col_bins.index(row_n-1)
        print(f'found smudge at col {cm}')
    else:
        print(f'no col smudge')


    #print('ROWS')
    row_mirrors = range(1, row_n)
    rows = []
    for col in list(map(list, zip(*island_map))):
        # narrows down candidates
        refs = reflections_line(col, row_mirrors)
        print(''.join(col), refs)
        rows.extend(reflections_line(col, row_mirrors))

    # smudge would be row with len(island_map[0]) occurrences
    row_bins = list(map(rows.count, range(len(island_map))))
    # if the smudge were fixed this is where the mirror would be
    if col_n-1 in row_bins:
        rm = row_bins.index(col_n-1)
        print(f'found smudge at row {rm}')
    else:
        print(f'no row smudge')

    if cm == 0 and rm == 0:
        print(f'HERE ({len(col_bins)}, {len(row_bins)}): {row_bins}, {col_bins}')
        print_grid(island_map)
        print()

    return (rm * 100, cm)       # 29763  26595

def count_reflections(island_map):
    # all columns are candidates
    col_mirrors = list(range(1, len(island_map[0])))
    for row in island_map:
        # narrows down candidates
        col_mirrors = reflections_line(row, col_mirrors)

    row_mirrors = list(range(1, len(island_map)))
    for col in list(map(list, zip(*island_map))):
        row_mirrors = reflections_line(col, row_mirrors)

    print(f'mirrors: {col_mirrors}, {row_mirrors}')
    cm = sum(col_mirrors)
    rm = sum(row_mirrors)
    return (rm * 100, cm)

def print_grid(grid):
    for r in grid:
        print(''.join(r))
        
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
                    #this_map.append(list(line))
                    this_map.append(line)

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
        reflections = list(map(find_smudge, maps))
        reflection_sum = [sum(x) for x in zip(*reflections)]
        ref_summary = reflection_sum[0] + reflection_sum[1]
        print(f'\tNumber of reflections: {ref_summary}') #29366

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
