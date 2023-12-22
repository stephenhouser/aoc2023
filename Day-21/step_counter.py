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
from collections.abc import Iterable


class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Part 1 solution for test.txt"""
        garden_map = load_file('test.txt')
        gardens = find_gardens(garden_map, find_start(garden_map), 6)
        self.assertEqual(len(gardens), 16)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        garden_map = load_file('input.txt')
        gardens = find_gardens(garden_map, find_start(garden_map), 64)
        self.assertEqual(len(gardens), 3_746)

    #
    # Part Two
    #
    # def test_part2_example(self):
    #     """Part 2 solution for test.txt"""
    #     things = load_file('test.txt')
    #     result = len(things)
    #     self.assertEqual(result, 10)

    # def test_part2_solution(self):
    #     """Part 2 solution for input.txt"""
    #     things = load_file('input.txt')
    #     result = len(things)
    #     self.assertEqual(result, 10)

def c_str(cplx):
    """Pretty print a complex number as (i,j)"""
    return f'({int(cplx.real)}, {int(cplx.imag)})'

def ascii_color(hex_color, text):
    """Return text in ASCII color"""
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'
    

class Map:
    """Represents a ___"""
    def __init__(self, map_data):
        self.rows = 0
        self.cols = 0
        self._map = None
        self._load_map(map_data)

    def get(self, x, y=None):
        if isinstance(x, complex):
            return self._map.get(x)
        else:
            return self._map.get(complex(x,y))
    
    def infinite_get(self, position):
        x = position.real % cols
        y = position.imag % rows
        return self.get(complex(int(x),int(y)))    

    def load_map(self, text):
        if isinstance(text, str):
            lines = text.split('\n')
        else:
            lines = text

        self._map = {complex(i,j): c for j, r in enumerate(text)
                     for i, c in  enumerate(r.strip())}

    def print(self, highlights=None):
        """Pretty print 2D grid in readable form"""
        print('  ', end='')
        _ = [print(f'{x%10}', end='') for x in range(self.cols)]
        print('\n :', end='')
        _ = [print('-', end='') for x in range(self.cols)]
        for y in range(rows):
            print(f'\n{y%10}:', end='')
            for x in range(cols):
                symbol = self.get(x, y)
                if not symbol:
                    print(ascii_color('777777', '~'), end='')
                elif highlights and complex(x,y) in highlights:
                    print(ascii_color('ffffff', 'O'), end='')
                else:
                    print(symbol, end='')

        print()

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'Empty'


def print_gridX(grid, highlight=None):
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

    print()


def print_grid(grid, highlight=None):
    """Pretty print 2D grid in readable form"""

    print(' :', end='')
    _ = [print(f'{x%10}', end='') for x in range(cols)] # header
    print('\n :', end='')
    _ = [print('-', end='') for x in range(cols)] # header
    for y in range(3*rows):
        print(f'\n{y%10}:', end='')
        for x in range(3*cols):
            symbol = igrid(grid, complex(x,y))
            if not symbol:
                print('#', end='')
            elif highlight and complex(x,y) in highlight:
                    print(ascii_color('ffffff', 'O'), end='')
            else:
                print(symbol, end='')

    print()


def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # returns a dictionary indexed by i,j with c as the value
            return {complex(i,j): c for j, r in enumerate(file)
                                for i, c in enumerate(r.strip())}      

            # # only load grid locations that are valid  
            # return {complex(i,j): c for j, r in enumerate(file)
            #                         for i, c in enumerate(r) if c in '.S'}

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

cols = None
rows = None

def igrid(grid, position):
    # return complex(position.real % 131, position.imag % 131)
    x = position.real % cols
    y = position.imag % rows
    grid_pos = complex(int(x),int(y))
    if grid.get(grid_pos) == None:
        print(x, y, c_str(grid_pos), grid.get(grid_pos))
    return grid.get(grid_pos)
    

def find_gardensX(grid, start_position, end_steps=16):
    """Return the gardens (positions) that would result from
        walking exactly end_steps steps from start_position.
    """
    walker = deque([(start_position, 0)])
    closed = set()
    repeats = set()

    while walker:
        position, steps = walker.popleft()
        # print(f'walker {c_str(position)} {steps}')

        # ignore rocks
        if igrid(grid, position) == '#':
            continue

        # ignore repeated positions with steps
        if (position, steps) in repeats:
            continue

        repeats.add((position, steps))

        # if we are at the end of a path, close it out
        if steps == end_steps:
            closed.add(position)
            continue

        # add neighbors and walkers
        for direction in (1, -1, 1j, -1j):
            neighbor = position + direction
            walker.append((neighbor, steps+1))

    # print(f'max walkers = {walker_len}')
    return closed

def find_gardens(grid, start, end_steps):
    closed = []
    open = {start}

    for step in range(3 * 131):
        if step == 64: 
            print(len(open))

        if step % 131 == 64:
            closed.append(len(open))

        new_open = set()
        for d in {1, -1, 1j, -1j}:
            for p in open:
                if igrid(grid, p+d) != '#':
                    new_open.add(p+d)
        open = new_open

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
            global rows, cols
            rows = len(set([int(n.imag) for n in garden_map]))    # set comprehension R1718
            cols = len(set([int(n.real) for n in garden_map]))

            #
            # Part One
            #
            #print_grid(garden_map)

            # rows = set([int(n.imag) for n in garden_map])    # set comprehension R1718
            # cols = set([int(n.real) for n in garden_map])
            # start = complex(len(cols)//2, len(rows)//2)
            start = find_start(garden_map)




            # # for n in (65, 196, 327):
            # for n in (6, 10, 50, 100, 500):
            #     gardens = find_gardens(garden_map, start, n)
            #     # print_grid(garden_map, gardens)
            #     print(n, ',', len(gardens))
            #     # print(f'\t1. Unique gardens reachable in 64 steps: {n}:{len(gardens):,}')

            #
            # Part Two
            #
            # n_things = len(things)
            # print(f'\t2. umber of things: {n_things:,}')
            # 560_433_720_286_689 too low
            # 623_540_829_615_589 -- fits the quadratic
            # closed = find_gardens(garden_map, start, 0)
            closed = [3889, 34504, 95591]
            print(closed)

            def lagrange_interpolation(v0, v1, v2):
                return [
                    v0 / 2 - v1 + v2 / 2,
                    -3 * (v0 / 2) + 2 * v1 - v2 / 2,
                    v0
                ]

            l = lagrange_interpolation(*closed)
            print(l)

            n = 26501365 // 131
            ans = l[2] + l[1] * n + l[0] * n**2 
            print(ans)

            # 65 , 196, 327
            # quadratic fit calculator {{0, 3889}, {1,34504}, {2,95591}}
            # least-squares best fit = 3889 + 15379 x + 15236 x^2
            # solve 3889 + 15379 x + 15236 x^2 with x=202300
            # 3889 + 15379 x + 15236 x^2 with x=26501365  202300

            # 26501365 // 131
            # print(f(26501365 // 131, *closed))

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
