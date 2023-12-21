#!/usr/bin/env python
"""
Advent of Code 2023 - Day 21: Step Counter
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
from functools import cache
from collections import deque


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


def ascii_color(hex_color, text):
    """Return text in ASCII color"""
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'


def print_grid(grid, highlight=None):
    """Pretty print 2D grid in readable form"""
    rows = set([int(n.imag) for n in grid])    # set comprehension R1718
    cols = set([int(n.real) for n in grid])

    print(' :', end='')
    _ = [print(f'{x%10}', end='') for x in cols] # header
    print('\n :', end='')
    _ = [print('-', end='') for x in cols] # header
    for y in rows:
        print(f'\n{y%10}:', end='')
        for x in cols:
            symbol = grid.get(complex(x,y))
            if highlight and complex(x,y) in highlight:
                    print(ascii_color('ffffff', 'O'), end='')
            else:
                    print(symbol, end='')
            # match char := grid.get(complex(x, y)):
            #     case 'S': # start (and garden plot)
            #         print(ascii_color('ffffff', char), end='')
            #     case '#': # rock
            #         print(ascii_color('00ff00', char), end='')
            #     case '.': # garden plot
            #         print(ascii_color('00ffff', char), end='')
            #     case _:
            #         print(char, end='')

    print()

def c_str(cplx):
    """Pretty print a complex number as (i,j)"""
    return f'({int(cplx.real)}, {int(cplx.imag)})'


def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # returns a dictionary indexed by i,j with c as the value
            return {complex(i,j): c for j, r in enumerate(file)
                                for i, c in enumerate(r.strip())}

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def find_gardens(grid, start_position, end_steps=16):
    rows = set([int(n.imag) for n in grid])    # set comprehension R1718
    cols = set([int(n.real) for n in grid])

    walker = deque([(start_position, 0)])
    closed = set()
    repeats = set()

    walker_len = len(walker)
    while walker:
        position, steps = walker.popleft()
        # print(f'walker {c_str(position)} {steps}')

        if position.real not in cols or position.imag not in rows:
            continue

        if grid.get(position) == '#':
            continue

        if (position, steps) in repeats:
            continue

        repeats.add((position, steps))

        if steps == end_steps:
            closed.add(position)
            continue

        for direction in (1, -1, 1j, -1j):
            neighbor = position + direction
            walker.append((neighbor, steps+1))

        walker_len = max(walker_len, len(walker))

    print(f'max walkers = {walker_len}')
    return closed


def find_start(grid):
    starts = list(filter(lambda x: grid[x] == 'S', grid))

    assert len(starts) == 1
    return starts[0]

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            garden_map = load_file(filename)

            #
            # Part One
            #
            # print_grid(garden_map)
            start = find_start(garden_map)
            gardens = find_gardens(garden_map, start, 64)

            print_grid(garden_map, gardens)
            print(f'\t1. Unique gardens reachable in 64 steps: {len(gardens):,}')

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
