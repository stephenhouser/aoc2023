#!/usr/bin/env python
"""
Advent of Code 2023 - Day 14: Parabolic Reflector Dish 
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
import logging as log
import hashlib
import sys

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

def transpose(grid):
    return list(map(list, zip(*grid)))

def flip(grid):
    return list(map(list, map(reversed, grid)))

def roll_row(row):
    #print(row)
    blocks = re.findall(r'[.O]*#*', ''.join(row))

    n_row = ''
    for block in blocks:
        n_row += 'O' * block.count('O') + \
                 '.' * block.count('.') + \
                 '#' * block.count('#')
    return list(n_row)

#   N  W  S    E
#   tt x tfft  f
MEMORY = {}
def roll_cycle(dish, cycle_n):
    digest = hash_value(dish)
    if digest in MEMORY:
        (o_cycle, dish) = MEMORY[digest]
        print(f'REPEAT at {cycle_n} of {o_cycle}')
        return dish
    
    # north
    dish = transpose(map(roll_row, transpose(dish)))
    # west
    dish = list(map(roll_row, dish))
    # south
    dish = transpose(flip(map(roll_row, flip(transpose(dish)))))
    #east
    dish = flip(map(roll_row, flip(dish)))

    MEMORY[digest] = (cycle_n, dish)
    return dish

def hash_value(dish):
    char_map = ''
    for r in dish:
        char_map += ''.join(r)
    
    return hashlib.sha256(char_map.encode()).hexdigest()

def roll_north(dish):
    dish = transpose(map(roll_row, transpose(dish)))
    return dish


def calculate_weight(dish):
    weight = 0
    for i, row in enumerate(reversed(dish)):
        weight += (i + 1) * sum(rock=='O' for rock in row)

    return weight

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
        dish = load_file(filename)

        #
        # Part One
        #
        dish = roll_north(dish)
        weight = calculate_weight(dish)
        print(f'\t1. The weight on the north beam: {weight}')

        #
        # Part Two
        #

# ...999999998  = 96105

        for i in range(96):
            dish = roll_cycle(dish, i)

        while i < 1_000_000_000:
            i += 11

        i -= 11
        print(f'restart at {i}')
        while i < 1_000_000_010:
            dish = roll_cycle(dish, i)
            weight = calculate_weight(dish)
            print(f'...{i} = {weight}')
            i += 1

        # cycle starts at 96 and repeats every 11
        # start = 999,999,904 # 1_000_000_000 - 96
        # start = 96 + 90,909,082
        # for i in range(start, 1_000_000_00)

        weight = calculate_weight(dish)
        print(f'\t2. The weight on the north beam ({i}): {weight}')
        #print_grid(dish)
        #print()

if __name__ == '__main__':
    main()
    #unittest.main()
