#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest


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

def color_code(hex_color):
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'\033[38;2;{r};{g};{b}m'

def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    mins, maxs = get_grid_size(grid)
    # print("SIZE", mins, maxs)
    cols = range(int(mins.real), int(maxs.real+1))
    # rows = range(int(mins.imag), int(maxs.imag+1))
    rows = range(int(maxs.imag-1), int(maxs.imag+1))

    #print('   ', end='')
    #_ = [print(f'{x:1}', end='') for x in cols] # header
    # print('\n  ', end='')
    # _ = [print('-', end='') for x in cols] # header
    for y in rows:
        print(f'\n{y:2}:', end='')
        for x in cols:
            if grid.get(complex(x, y)):
                color = color_code(grid.get(complex(x, y)))
                print(f'{color}#\033[0m', end='')
                # print(f'{grid.get(complex(x, y)):^3}', end='')
            else:
                print('.', end='')

    print()

def print_grid_csv(grid):
    """Pretty print 2D grid in readable form"""
    mins, maxs = get_grid_size(grid)
    # print("SIZE", mins, maxs)
    cols = range(int(mins.real), int(maxs.real+1))
    rows = range(int(mins.imag), int(maxs.imag+1))
    # rows = range(int(maxs.imag-1), int(maxs.imag+1))

    #print('   ', end='')
    #_ = [print(f'{x:1}', end='') for x in cols] # header
    # print('\n  ', end='')
    # _ = [print('-', end='') for x in cols] # header
    for y in rows:
        for x in cols:
            if grid.get(complex(x, y)):
                print('1,', end='')
            else:
                print(',', end='')
        print()

    print()

def c_str(cplx):
    """Pretty print a complex number as (i,j)"""
    return f'({int(cplx.real)}, {int(cplx.imag)})'

def parse_direction(text):
    directions = {'U': complex(0, -1), 
                  'D': complex(0, 1), 
                  'L': complex(-1, 0), 
                  'R': complex(1, 0)}

    direction_code, length, color_code = text.split()

    direction = directions[direction_code]
    length = int(length)
    # color = int(re.findall(r'[0-9A-Za-z]+', color_code)[0], 16)
    color = re.findall(r'[0-9A-Za-z]+', color_code)[0]
    return (direction, length, color)

def dig_trench_step(grid, position, direction, steps, color):
    while steps:
        grid[position] = color
        position += direction
        steps -= 1

    return position
    
def dig_trench(grid, instructions):
    position = complex(0, 0)
    for direction, steps, color in instructions:
        position = dig_trench_step(grid, position, direction, steps, color)

    return position

def lagoon_volume(grid):
    fill = '000000'
    hashes = sum((1 for x in grid if grid[x] != fill))
    print('hashes', hashes)

    fills = sum((1 for x in grid if grid[x] == fill))
    print('fills', fills)

    mins, maxs = get_grid_size(grid)
    cols = abs(int(mins.real) - int(maxs.real+1))
    rows = abs(int(mins.imag) - int(maxs.imag+1))
    size = cols * rows

    print('lagoon', size-fills)

    inner = sum((1 for x in grid if grid[x] != fill))
    print('lagoon inner', size-fills)


    return len(grid)
    # mins, maxs = get_grid_size(grid)
    # cols = range(int(mins.real), int(maxs.real+1))
    # rows = range(int(mins.imag), int(maxs.imag+1))

    # for y in rows:
    #     for x in cols:
    #         if grid.get(complex(x, y)):

# 78396 too low -- not including all fills
def fill_lagoon(grid):
    mins, maxs = get_grid_size(grid)
    cols = range(int(mins.real), int(maxs.real+1))
    rows = range(int(mins.imag), int(maxs.imag+1))

    inner_fill = 'ffffff'

    for y in rows:
        fill = None
        prev = None
        for x in cols:
            save = grid.get(complex(x, y))
            if save == '000000':
                continue

            if grid.get(complex(x, y)):
                if fill:
                    if prev:
                        fill = inner_fill
                    else:
                        fill = None
                else: # turn on filling
                    fill = inner_fill
            elif fill:
                grid[complex(x,y)] = fill

            prev = save

# 91551 too high -- not including inner fills
def flood(grid):
    mins, maxs = get_grid_size(grid)
    cols = list(range(int(mins.real), int(maxs.real+1)))
    rows = list(range(int(mins.imag), int(maxs.imag+1)))

    fill = '000000'

    for y in rows:
        # fill >
        for x in cols:
            pos = complex(x, y)
            if grid.get(pos) and grid.get(pos) != fill:
                break

            grid[pos] = fill

        # fill <
        for x in reversed(cols):
            pos = complex(x, y)
            if grid.get(pos) and grid.get(pos) != fill:
                break

            grid[pos] = fill

    for x in cols:
        # fill v
        for y in rows:
            pos = complex(x, y)
            if grid.get(pos) and grid.get(pos) != fill:
                break

            grid[pos] = fill

        # fill ^
        for y in reversed(rows):
            pos = complex(x, y)
            if grid.get(pos) and grid.get(pos) != fill:
                break

            grid[pos] = fill


def get_grid_size(grid):
    min_x = min(x.real for x in grid)
    max_x = max(x.real for x in grid)

    min_y = min(y.imag for y in grid)
    max_y = max(y.imag for y in grid)

    #print(f'min={min_x}, {min_y}, max={max_x}, {max_y}')
    return complex(min_x, min_y), complex(max_x, max_y)

def load_file(filename: str):
    """Load lines from file into ___
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # read a list of Directons
            return list(map(parse_direction, file.readlines()))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

# 60093 not right
# 69119 too high
def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        instructions = load_file(filename)

        #
        # Part One
        #
        lagoon_map = dict()
        position = dig_trench(lagoon_map, instructions)
        print_grid_csv(lagoon_map)
        print(f'\t1. Volume before fill: {lagoon_volume(lagoon_map)}')

        # flood(lagoon_map)
        # print_grid(lagoon_map)
        # fill_lagoon(lagoon_map)
        # print_grid(lagoon_map)
        # print(f'\t1. Volume after fill : {lagoon_volume(lagoon_map)}')

        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
