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
import itertools

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Test example 1 from test.txt"""
        weight = calculate_weight(roll_north(load_file('test.txt')))
        self.assertEqual(weight, 136)

    def test_part1_solution(self):
        """Solution for part 2 from input.txt"""
        weight = calculate_weight(roll_north(load_file('input.txt')))
        self.assertEqual(weight, 109596)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Test example 1 from test.txt"""
        weight = calculate_weight(
            roll_cycles(load_file('test.txt'), 1_000_000_000))
        self.assertEqual(weight, 64)

    def test_part2_solution(self):
        """Solution for part 2 from input.txt"""
        weight = calculate_weight(
            roll_cycles(load_file('input.txt'), 1_000_000_000))
        self.assertEqual(weight, 96105)

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

def transpose(grid):
    return tuple(map(tuple, zip(*grid)))

def flip(grid):
    return tuple(map(tuple, map(reversed, grid)))

def roll_row(row):
    #print(row)
    blocks = re.findall(r'[.O]*#*', ''.join(row))

    n_row = ''
    for block in blocks:
        n_row += 'O' * block.count('O') + \
                 '.' * block.count('.') + \
                 '#' * block.count('#')
    return n_row

#   N  W  S    E
#   tt x tfft  f
def roll_cycle(dish):
    # north
    dish = transpose(map(roll_row, transpose(dish)))
    # west
    dish = map(roll_row, dish)
    # south
    dish = transpose(flip(map(roll_row, flip(transpose(dish)))))
    #east
    dish = flip(map(roll_row, flip(dish)))

    return dish

def roll_cycles(dish, cycles):
    """Simulate rolling `dish` through N,W,S,E cycles and return
        the final dish arrangement after `cycles`
    """
    arrangements = {}               # cache past arrangement (hash values)
    
    i = 0
    while dish_key := map_hash(dish) not in arrangements:
        arrangements[dish_key] = i  # save the arrangement
        dish = roll_cycle(dish)     # roll it around
        i += 1

    prev = arrangements[dish_key]
    cycle = (prev, i-prev)

    # # First, find the cycle in the arrangements
    # cycle = (None, None)            # (start, length) of cycle (result of loop)
    # for i in range(cycles):         # start counting at 1 end before cycles
    #     dish_key = map_hash(dish)   # have we seen this arrangement before
    #     if dish_key in arrangements:
    #         prev = arrangements[dish_key]
    #         cycle = (prev, i-prev)
    #         break                   # stop the madness

    #     arrangements[dish_key] = i  # save the arrangement
    #     dish = roll_cycle(dish)     # roll it around

    # The target cycle is `end_offset` rolls from the start of the repeating
    # cycle. We can just play that many more forward and end at the same 
    # arrangement we would have if we played thorough all the actual cycles
    # This is remaining cycles % cycle_length
    end_offset = (cycles - cycle[0]) % cycle[1]

    # Restart rolling until we get to the cycle we are looking for
    #   ...I could have saved these arrangements, but... cheap to replay
    for i in range(end_offset):
        dish = roll_cycle(dish)

    return dish

def map_hash(dish):
    """Returns an SHA256 hash value for the map arrangement
        Used to index saved values for hopefully faster lookup
    """
    text = ''.join(itertools.chain(*dish))
    return hashlib.sha256(text.encode()).hexdigest()

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
            return tuple(map(tuple, map(str.strip, file.readlines())))

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
        dish = roll_cycles(dish, 1_000_000_000)
        weight = calculate_weight(dish)
        print(f'\t2. The weight on the north beam: {weight}')
        #print_grid(dish)
        #print()

if __name__ == '__main__':
    main()
    #unittest.main()
