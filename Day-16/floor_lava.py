#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
import logging as log
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)


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


# beam is (y, x)
# map is (char, energized)
# start at 0, 0, going E  == (0, 0, 'E)'
# save states
# stop when hit cycle

def is_marked(grid, beam):
    return grid[beam[0]][beam[1]][1] == '#'

# moves to next lasewr location
BEAMS = {}
def shoot_laser(grid, beam):
    y, x, dy, dx = beam

    # off end
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return 1

    if beam in BEAMS:
        return 1

    BEAMS[beam] = 1

    print(f'\t{beam} : {grid[beam[0]][beam[1]]})')

    grid_op = grid[beam[0]][beam[1]][0]
    if grid_op == '\\':
        # E->S, S->E, W->N, N->W
        # E (0, 1) -> S(1, 0)
        # S (1, 0) -> E(0, 1)
        # N (-1, 0) -> W(0, -1)
        # W (0, -1) -> N(-1, 0)
        grid[beam[0]][beam[1]][1] = '#'
        new_beam = (y+dx, x+dy, dx, dy)
        return shoot_laser(grid, new_beam)
    elif grid_op == '/':
        # E (0, 1) -> N(-1, 0)
        # S (1, 0) -> W(0, -1)
        # W(0, -1) -> S(1, 0)
        # N(0, -1) -> E(1,0)
        grid[beam[0]][beam[1]][1] = '#'
        new_beam = (y-dx, x-dy, -dx, -dy)
        return shoot_laser(grid, new_beam)
    elif grid_op == '-':
        grid[beam[0]][beam[1]][1] = '#'
        if dy:
            b1 = (y-dx, x-dy, -dx, -dy)
            b2 = (y+dx, x+dy, dx, dy)
            return shoot_laser(grid, b1) + shoot_laser(grid, b2)
        else:
            new_beam = (y+dy, x+dx, dy, dx)
            return shoot_laser(grid, new_beam)
    elif grid_op == '|':
        print('poof')
        grid[beam[0]][beam[1]][1] = '#'
        if dx:
            b1 = (y-dx, x-dy, -dx, -dy)
            b2 = (y+dx, x+dy, dx, dy)
            return shoot_laser(grid, b1) + shoot_laser(grid, b2)
        else:
            new_beam = (y+dy, x+dx, dy, dx)
            return shoot_laser(grid, new_beam)

    # if grid[beam[0]][beam[1]][1] == '#':
    #     return 1

    grid[beam[0]][beam[1]][1] = '#'

    y, x = y+dy, x+dx
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return 1
    
    while grid[y][x][0] == '.':
        grid[y][x][1] = '#'
        y, x = y+dy, x+dx
        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
            return 1

    new_beam = (y, x, dy, dx)
    return shoot_laser(grid, new_beam)

def grid_value(grid):
    sum = 0
    for r in grid:
        for c in r:
            sum += 1 if c[1] == '#' else 0
    return sum

def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    for row in grid:
        for col in row:
            print(f'{col[0]}{col[1]}', end=' ')
        print()


def print_marks(grid):
    """Pretty print 2D grid in readable form"""
    for row in grid:
        for col in row:
            print(f'{col[1]}', end='')
        print()

def load_file(filename: str):
    """Load lines from file into ___
        
       filename: the file to read game descriptions from.
       returns: ...
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # read a grid of text into 2D grid
            #return list(map(list, map(str.strip, file.readlines())))
            grid = []
            for line in file.readlines():
                row = []
                for ch in list(line.strip()):
                    row.append([ch, '.'])
                grid.append(row)

            return grid
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
        floor_map = load_file(filename)

        print_grid(floor_map)
        shoot_laser(floor_map, (0, 0, 0, 1))
        print_marks(floor_map)

        print(grid_value(floor_map))
        #
        # Part One
        #
        # print(f'\tNumber of things: {n_things}')

        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
