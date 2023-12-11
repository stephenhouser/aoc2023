#!/usr/bin/env python
"""
Advent of Code 2023 - Day 11: Cosmic Expansion
Stephen Houser <stephenhouser@gmail.com>
"""

import argparse
from itertools import combinations


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

def expand_space(space):
    """Returns the expanded space map.
       empty rows are doubled, empty columns are doubled
    """
    # accomplished by duplicating any empty rows, then transposing the
    # list and doing the same again -- which will duplicate empty columns
    # transpose again to get back to original form.
    for _ in range(2):
        n_space = []
        for row in space:
            n_space.append(row)
            if '#' not in row:
                n_space.append(row)

        space = [[n_space[j][i] for j in range(len(n_space))] for i in range(len(n_space[0]))]

    return space

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
        space = expand_space(space)
        galaxies = find_galaxies(space)

        pairs = combinations(list(galaxies.keys()), 2)
        distances = map(lambda p: distance(galaxies[p[0]], galaxies[p[1]]), pairs)
        print(f'\t1. The sum of the distances between galaxies is {sum(distances)}')

        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
