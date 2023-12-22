#!/usr/bin/env python
"""
Advent of Code 2023 - Day 21: Step Counter
Stephen Houser <stephenhouser@gmail.com>
"""

import argparse
import unittest
from cProfile import Profile
from collections import deque


class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Part 1 solution for test.txt"""
        garden_map = load_file('test.txt')
        gardens_reached = find_gardens_brute(garden_map, 6)
        self.assertEqual(gardens_reached, 16)

    def test_part1_example_fast(self):
        """Part 1 solution for test.txt"""
        garden_map = load_file('test.txt')
        gardens_reached = find_gardens_fast(garden_map, [6])[0]
        self.assertEqual(gardens_reached, 16)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        garden_map = load_file('input.txt')
        gardens_reached = find_gardens_brute(garden_map, 64)
        self.assertEqual(gardens_reached, 3_746)

    def test_part1_solution_fast(self):
        """Part 1 solution for input.txt"""
        garden_map = load_file('input.txt')
        gardens_reached = find_gardens_fast(garden_map, [64])[0]
        self.assertEqual(gardens_reached, 3_746)

    #
    # Part Two
    #
    def test_part2_example_10(self):
        """Part 2 solution for test.txt"""
        garden_map = load_file('test.txt')
        gardens_reached = find_gardens_fast(garden_map, [10])[0]
        self.assertEqual(gardens_reached, 50)

    def test_part2_example_50(self):
        """Part 2 solution for test.txt"""
        garden_map = load_file('test.txt')
        gardens_reached = find_gardens_fast(garden_map, [50])[0]
        self.assertEqual(gardens_reached, 1_594)

    def test_part2_example_100(self):
        """Part 2 solution for test.txt"""
        garden_map = load_file('test.txt')
        gardens_reached = find_gardens_fast(garden_map, [100])[0]
        self.assertEqual(gardens_reached, 6_536)
        
    # def test_part2_example_500(self):
    #     """Part 2 solution for test.txt"""
    #     garden_map = load_file('test.txt')
    #     gardens_reached = find_gardens_fast(garden_map, [500])[0]
    #     self.assertEqual(gardens_reached, 167_004)
        
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
        self.load_map(map_data)

    def get(self, x, y=None):
        if isinstance(x, complex):
            return self._map.get(x)
        else:
            return self._map.get(complex(x,y))
    
    def infinite_get(self, position):
        x = position.real % self.cols
        y = position.imag % self.rows
        return self.get(complex(int(x),int(y)))    

    def load_map(self, text):
        if isinstance(text, str):
            lines = text.split('\n')
        else:
            lines = text

        self._map = {complex(i,j): c for j, r in enumerate(lines)
                     for i, c in  enumerate(r.strip())}
        self.rows = int(max([n.imag for n in self._map]))+1
        self.cols = int(max([n.real for n in self._map]))+1 

    def get_start(self):
        starts = list(filter(lambda x: self._map[x] == 'S', self._map))
        
        assert len(starts) == 1
        return starts[0]
    
    def print(self, highlights=None):
        """Pretty print 2D grid in readable form"""
        print('  ', end='')
        _ = [print(f'{x%10}', end='') for x in range(self.cols)]
        print('\n :', end='')
        _ = [print('-', end='') for x in range(self.cols)]
        for y in range(self.rows):
            print(f'\n{y%10}:', end='')
            for x in range(self.cols):
                symbol = self.get(x, y)
                if not symbol:
                    print(ascii_color('777777', '~'), end='')
                elif highlights and complex(x,y) in highlights:
                    print(ascii_color('ffffff', symbol), end='')
                else:
                    print(symbol, end='')

        print()

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'Empty'

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return Map(file)

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def find_gardens_brute(garden_map, end_steps=16):
    """Return the gardens (positions) that would result from
        walking exactly end_steps steps from start_position.
    """
    walker = deque([(garden_map.get_start(), 0)])
    reached = set()
    repeats = set()

    while walker:
        position, steps = walker.popleft()
        # print(f'walker {c_str(position)} {steps}')

        # ignore rocks
        if garden_map.get(position) == '#':
            continue

        # ignore repeated positions with steps
        if (position, steps) in repeats:
            continue

        repeats.add((position, steps))

        # if we are at the end of a path, close it out
        if steps == end_steps:
            reached.add(position)
            continue

        # add neighbors and walkers
        for direction in (1, -1, 1j, -1j):
            neighbor = position + direction
            walker.append((neighbor, steps+1))

    return len(reached)

def find_gardens_fast(garden_map, step_counts):
    closed = []
    open = {garden_map.get_start()}

    step = 0
    while len(step_counts):
        if step in step_counts:
            step_counts.pop(step_counts.index(step))
            closed.append(len(open))

        new_open = set()
        for direction in (1, -1, 1j, -1j):
            for position in open:
                if garden_map.infinite_get(position+direction) != '#':
                    new_open.add(position+direction)

        open = new_open
        step += 1

    return closed

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
            # garden_map.print([garden_map.get_start()])

            #
            # Part One
            #
            steps = 64
            gardens_reached = find_gardens_brute(garden_map, steps)
            print(f'\t1. Unique gardens reachable in 64 steps: {gardens_reached:,}')

            gardens_reached = find_gardens_fast(garden_map, [steps])[0]
            print(f'\t1. Unique gardens reachable in {steps:,} steps: {gardens_reached:,}')

            #
            # Part Two
            #

            # one "map" will fill up in half_map steps
            half_map = garden_map.rows // 2
            # we search for three terms to interpolate a quadratic
            step_search = [half_map, 
                           half_map + garden_map.rows, 
                           half_map + garden_map.rows * 2]
            # find the terms
            #gardens_reached = find_gardens_fast(garden_map, step_search)
            gardens_reached = [3889, 34504, 95591]
            print('gardens reached', gardens_reached)

            # Wolfram Alpha...
            # quadratic fit calculator {{0, 3889}, {1,34504}, {2,95591}}
            # least-squares best fit = 3889 + 15379 x + 15236 x^2
            # divide steps by the map size; x= 26501365 // 131
            # solve 3889 + 15379 x + 15236 x^2 with x=202300
            # 623_540_829_615_589 -- fits the quadratic!!
            def lagrange_interpolation(vec):
                """Returns the three terms of the quadratic; c + bx + ax**2
                    Can't say I understand this one, just used the formula
                """
                return [int(vec[0] / 2 - vec[1] + vec[2] / 2),
                        int(-3 * (vec[0] / 2) + 2 * vec[1] - vec[2] / 2),
                        int(vec[0])
                    ]

            steps = 26_501_365
            x = steps // garden_map.rows
            a, b, c = lagrange_interpolation(gardens_reached)
            print('quadratic terms', a, b, c)

            gardens_reached = a*x**2 + b*x + c
            print(f'\t2. Unique gardens reached in {steps:,} steps: {gardens_reached:,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
