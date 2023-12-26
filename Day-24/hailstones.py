#!/usr/bin/env python
"""
Advent of Code 2023 - Day 24: Never Tell Me The Odds
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
from itertools import combinations


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


def c_str(cplx):
    """Pretty print a complex number as (i,j)"""
    return f'({int(cplx.real)}, {int(cplx.imag)})'

def c_tup(cplx):
    """Return a tuple(x,y) from a complex(x,y)"""
    return (int(cplx.real), int(cplx.imag))


class Hailstone:
    """Represents a ___"""
    def __init__(self, text):
        self.position = None
        self.velocity = None
        self._parse_line(text)

    def _parse_line(self, text):
        """Parse text description of ___"""
        # 19, 13, 30 @ -2,  1, -2
        match = list(map(int, re.findall(r'-?\d+', text)))
        self.position = complex(match[0], match[1])
        self.velocity = complex(match[3], match[4])

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'Stone {c_str(self.position)}, {c_str(self.velocity)}'

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return list(map(Hailstone, file.readlines()))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def intersection(s1, s2):
    """Returns where s1 and s2 intersect"""
    line1 = (c_tup(s1.position), c_tup(s1.position+s1.velocity))
    line2 = (c_tup(s2.position), c_tup(s2.position+s2.velocity))

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return complex(x, y)

def in_future(line, point):
    x, y = c_tup(line.position)
    dx, dy = c_tup(line.velocity)

    if dx < 0 and point.real > x:
        return False

    if dx > 0 and point.real < x:
        return False
    
    if dy < 0 and point.imag > y:
        return False
    
    if dy > 0 and point.imag < y:
        return False
    
    return True

def simulate(stones, test_area):
    intersection_count = 0
    for s1, s2 in combinations(stones, 2):
        i_point = intersection(s1, s2)
        # print(f'{s1} and {s2} -> {i_point}')
        if i_point and \
            test_area[0].real <= i_point.real <= test_area[1].real and \
            test_area[0].imag <= i_point.imag <= test_area[1].imag:

            if in_future(s1, i_point) and in_future(s2, i_point):
                print(f'{s1} and {s2} -> {c_str(i_point)}')
                intersection_count += 1

    return intersection_count


def print_stones(stones):
    for stone in stones:
        print(stone)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            stones = load_file(filename)

            # print_stones(stones)
            #
            # Part One
            #
            n_stones = len(stones)
            # i_count = simulate(stones, (complex(7,7), complex(27, 27)))
            i_count = simulate(stones, (complex(200000000000000,200000000000000), complex(400000000000000, 400000000000000)))
            print(f'\t1. Number of things: {i_count:,}')

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
