#!/usr/bin/env python
"""
Advent of Code 2023 - Day 18: Lavaduct Lagoon
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
        self.assertEqual(dig_lagoon(load_file('test.txt')), 62)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        self.assertEqual(dig_lagoon(load_file('input.txt')), 61661)

    #
    # Part Two
    #
    # def test_part2_example(self):
    #     """Test example 1 data from test.txt"""
    #     self.assertEqual(test_function('test.txt', 10), 0)

    # def test_part2_solution(self):
    #     """Test example 1 data from test.txt"""
    #     self.assertEqual(test_function('input.txt', 1000000), 0)

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # read a list of Directons
            return list(map(parse_instruction, file.readlines()))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def ascii_color(hex_color, text):
    """Return text in ASCII color"""
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    mins, maxs = get_grid_size(grid)
    cols = range(int(mins.real), int(maxs.real+1))
    rows = range(int(mins.imag), int(maxs.imag+1))

    for y in rows:
        print(f'\n{y:2}:', end='')
        for x in cols:
            if grid.get(complex(x, y)):
                print(ascii_color(grid.get(complex(x, y)), '#'), end='')
            else:
                print('.', end='')

    print()

def print_grid_csv(grid):
    """Print the grid as CSV"""
    mins, maxs = get_grid_size(grid)
    cols = range(int(mins.real), int(maxs.real+1))
    rows = range(int(mins.imag), int(maxs.imag+1))

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

def get_grid_size(grid):
    """Return the min and max coordinates of the grid"""
    min_x = min(x.real for x in grid)
    max_x = max(x.real for x in grid)

    min_y = min(y.imag for y in grid)
    max_y = max(y.imag for y in grid)

    #print(f'min={min_x}, {min_y}, max={max_x}, {max_y}')
    return complex(min_x, min_y), complex(max_x, max_y)

def on_grid(grid, position):
    """Return True if position on on the grid"""
    mins, maxs = get_grid_size(grid)

    return mins.real <= position.real <= maxs.real+1 and \
            mins.imag <= position.imag <= maxs.imag+1


def parse_instruction(text):
    """Return a parsed instruction"""
    directions = {'U': complex(0, -1), 'D': complex(0, 1),
                  'L': complex(-1, 0), 'R': complex(1, 0)}

    direction_code, length, color_code = text.split()

    direction = directions[direction_code]
    length = int(length)
    # color = int(re.findall(r'[0-9A-Za-z]+', color_code)[0], 16)
    color = re.findall(r'[0-9A-Za-z]+', color_code)[0]
    return (direction, length, color)

def dig_trench(instructions):
    """Perform one trench digging instruction"""
    trench = {}
    position = complex(0, 0)
    for direction, steps, color in instructions:
        while steps:
            trench[position] = color
            position += direction
            steps -= 1

    return trench

def flood_fill_one(grid, position, fill_color):
    """Flood fill the grid with fill_color starting at position"""
    to_fill = [position]
    while to_fill:
        pos = to_fill.pop()
        if grid.get(pos):       # skip if has something
            continue

        grid[pos] = fill_color  # fill it and add unfilled neighbors
        for neighbor_pos in (pos+1, pos+-1, pos+1j, pos+-1j):
            if not grid.get(neighbor_pos):
                to_fill.append(neighbor_pos)

def flood_fill(grid, instructions):
    """Flood fill the grid"""
    position = complex(0, 0)

    fill_directions = {complex(0, -1): complex( 1,  0), # U -> fill right
                       complex(0,  1): complex(-1,  0), # D -> fill left
                       complex(-1, 0): complex( 0, -1), # L -> fill up
                       complex( 1, 0): complex( 0,  1)} # R -> fill down

    # retrace our steps and fill to our right
    for direction, steps, color in instructions:
        while steps:
            grid[position] = color

            # flood fill neighbors
            fill_direction = fill_directions[direction]
            neighbor = position + fill_direction
            while on_grid(grid, neighbor) and not grid.get(neighbor):
                flood_fill_one(grid, neighbor, color)

            position += direction
            steps -= 1

        # TODO: Only need one fill on a single closed object
        break

    return position

def lagoon_volume(instructions, parser=None):
    """Return the number of filled grid locations"""
    return len(grid)

def dig_lagoon(instructions):
    """Dig trench and lagoon according to directions, return volume"""
    lagoon_map = dig_trench(instructions)
    flood_fill(lagoon_map, instructions)
    return lagoon_volume(lagoon_map)

def lagoon_verticies(instructions):
    """Return list of verticies generated in following instructions"""
    position = complex(0, 0)
    points = []
    for direction, steps, color in instructions:
        position += direction * steps
        points.append(position)
        #print(f'vertex: {c_str(position)}')

    return points

# Calculate value of shoelace formula
def shoelace(verticies):
    """Calculate the area of a polygon using shoelace formula.
        https://en.wikipedia.org/wiki/Shoelace_formula
    """
    x = [n.real for n in verticies]
    y = [n.imag for n in verticies]
    area = 0
    for i in range(0, len(verticies)-2, 2):
        area += x[i+1]*(y[i+2]-y[i]) + y[i+1]*(x[i]-x[i+2])

    return int(abs(area) / 2)

# 61661 -- CORRECT (Excel)
# 60093 not right
# 69119 too high
# 78396 too low -- not including all fills
# 91551 too high -- not including inner fills

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

        # flood fill version
        volume = dig_lagoon(instructions)
        print(f'\t1. Flood fill volume: {volume}')

        #
        # Part Two
        #
        lagoon = dig_trench(instructions)
        perimeter = lagoon_volume(lagoon) // 2 + 1
        volume = shoelace(lagoon_verticies(instructions)) + perimeter
        print(f'\t1. Shoelace volume : {volume}')

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
