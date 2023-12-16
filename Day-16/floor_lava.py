#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import copy
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

def is_valid(grid, y, x):
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        return True

    return False

# moves to next lasewr location
BEAMS = set()
def shoot_laser(grid, beam):
    y, x, dy, dx = beam

    # goes off edge of board or alreadly traversed
    if not is_valid(grid, y, x) or beam in BEAMS:
        return 0

    # mark this path as traversed
    BEAMS.add(beam)

    # Score when we mark it
    score = 0 if grid[y][x][1] == '#' else 1
    grid[beam[0]][beam[1]][1] = '#'

    # print(f'\t{beam} : {grid[y][x]}) {score}')

    grid_op = grid[beam[0]][beam[1]][0]
    if grid_op == '\\':
        score += shoot_laser(grid, (y+dx, x+dy, dx, dy))
    elif grid_op == '/':
        score += shoot_laser(grid, (y-dx, x-dy, -dx, -dy))
    elif grid_op == '-' and dy:
        score += shoot_laser(grid, (y-dx, x-dy, -dx, -dy)) + \
                 shoot_laser(grid, (y+dx, x+dy, dx, dy))
    elif grid_op == '|' and dx:
        score += shoot_laser(grid, (y-dx, x-dy, -dx, -dy)) + \
                 shoot_laser(grid, (y+dx, x+dy, dx, dy))
    else:
        y, x = y+dy, x+dx
        while is_valid(grid, y, x) and grid[y][x][0] == '.':
            # Score when we mark it
            score += 0 if grid[y][x][1] == '#' else 1
            grid[y][x][1] = '#'
            #print(f'\t {y}, {x}, {dy}, {dx}  : {grid[y][x]} {score}')
            y, x = y+dy, x+dx

        score += shoot_laser(grid, (y, x, dy, dx))

    return score

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

def clear_marks(grid):
    """Pretty print 2D grid in readable form"""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x][1] = '.'

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

        #
        # Part One
        #
        #print_grid(floor_map)
        BEAMS.clear()
        energized = shoot_laser(copy.deepcopy(floor_map), (0, 0, 0, 1))
        # print_marks(floor_map)
        print(f'\t1. Energized tiles: {energized}')

        #
        # Part Two
        #
        max_y = len(floor_map)
        max_x = len(floor_map[0])
        energized = []
        for y in range(max_y):
            BEAMS.clear()
            energized.append(shoot_laser(copy.deepcopy(floor_map), (y, 0, 0, 1)))
            BEAMS.clear()
            energized.append(shoot_laser(copy.deepcopy(floor_map), (y, max_x, 0, -1)))
        for x in range(max_x):
            BEAMS.clear()
            energized.append(shoot_laser(copy.deepcopy(floor_map), (0, x, 1, 0)))
            BEAMS.clear()
            energized.append(shoot_laser(copy.deepcopy(floor_map), (max_y, x, -1, 0)))

        # print(energized)
        print(f'\t1. Max Energized tiles: {max(energized)}')

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
