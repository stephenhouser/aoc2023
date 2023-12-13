#!/usr/bin/env python
"""
Advent of Code 2023 - Day 11: Cosmic Expansion
Stephen Houser <stephenhouser@gmail.com>
"""

import argparse
from itertools import combinations
import unittest


#
# Testing how things might work if I use Python unittest framework
# for running the examples and the final solution code...
#
# These would replace the main() function.
#
class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    def test_part1_example1(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(galaxy_distances('test.txt', 2), 374)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        self.assertEqual(galaxy_distances('input.txt', 2), 9742154)

    def test_part2_example1(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(galaxy_distances('test.txt', 10), 1030)

    def test_part2_example2(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(galaxy_distances('test.txt', 100), 8410)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(galaxy_distances('input.txt', 1000000), 411142919886)


def galaxy_distances(filename, expansion):
    """Return the sum of the distances beteen galaxy pairs as defined in the
       space map from filename. Use expansion factor for expanding empty space
       on the map
    """
    space = load_file(filename)
    galaxies = find_galaxies(space)
    expand_galaxies(space, galaxies, expansion)
    return sum_distances(galaxies)

class Galaxy:
    """A class of generic things"""
    NEXT_GALAXY_ID = 1  # to assign unique ids to each galaxy

    def __init__(self, x, y):
        self.id = Galaxy.NEXT_GALAXY_ID
        Galaxy.NEXT_GALAXY_ID += 1

        self.location = (x, y)

    def __repr__(self):
        """Return REPL representation of a galaxy"""
        return str(self)

    def __str__(self):
        """Return string representation of a galaxy"""
        return f'{self.id} {self.location}'

def load_file(filename: str):
    """Load map of space from file
       filename: the file to read game descriptions from.
       returns: a list of lists of characters representing the space map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return list(map(list,map(str.strip, file.readlines())))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def expand_galaxies(space, galaxies, expansion=2):
    """Expand galaxy locations based on empty rows and columns in space map
        use expansion as expansion factor, 
        e.g. 10 means each empty row is 10 rows
    """
    for y in reversed(range(len(space))):
        #print(f'Expand Y {y} {space[y]}')
        if '#' not in space[y]:
            for galaxy in galaxies.values():
                if y < galaxy.location[1]:
                    e_y = galaxy.location[1] + expansion -1
                    #print(f'\t{galaxy.id}:{galaxy.location[1]} -> {e_y}')
                    galaxy.location = (galaxy.location[0], e_y)

    col_space = [[space[j][i] for j in range(len(space))] for i in range(len(space[0]))]

    for x in reversed(range(len(col_space))):
        if '#' not in col_space[x]:
            #print(f'Expand X {x} {col_space[x]}')
            for galaxy in galaxies.values():
                if x < galaxy.location[0]:
                    e_x = galaxy.location[0] + expansion -1
                    #print(f'\t{galaxy.id}:{galaxy.location[0]} -> {e_x}')
                    galaxy.location = (e_x, galaxy.location[1])

def find_galaxies(space):
    """Returns a dictionary of galaxies keyed by thier assigned numeric id
    """
    galaxies = {}

    for y, row in enumerate(space):
        for x, col in enumerate(row):
            if col == '#':
                galaxy = Galaxy(x, y)
                galaxies[galaxy.id] = galaxy

    return galaxies

def distance(g1, g2):
    """Compute the distance between two galaxies as the integer path between them.
    """
    (x1, y1) = g1.location
    (x2, y2) = g2.location
    return abs(x2 - x1) + abs(y2 - y1)

def find_distances(galaxies):
    """Return a list of the distances between all galaxy pairs.
    """
    pairs = combinations(list(galaxies.keys()), 2)
    return list(map(lambda p: distance(galaxies[p[0]], galaxies[p[1]]), pairs))

def sum_distances(galaxies):
    """Return the sum of the distances between galaxy pairs.
    """
    return sum(find_distances(galaxies))

def print_space(space):
    """Pretty print the space map
    """
    for row in space:
        for col in row:
            print(f'{col:2}', end='')
        print()

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        space = load_file(filename)
        #print_space(space)
        #print()

        #
        # Part One
        #

        # expand by 2
        galaxies = find_galaxies(space)
        expand_galaxies(space, galaxies, 2)

        #pairs = combinations(list(galaxies.keys()), 2)
        #distances = map(lambda p: distance(galaxies[p[0]], galaxies[p[1]]), pairs)
        answer = sum_distances(galaxies)
        print(f'\t1. The sum of the distances between galaxies is {answer}, with expansion=2')

        #
        # Part Two
        #

        # expand by 1,000,000
        galaxies = find_galaxies(space)
        expand_galaxies(space, galaxies, 1000000)

        answer = sum_distances(galaxies)
        print(f'\t2. The sum of the distances between galaxies is {answer}, with expansion=1,000,000')

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
