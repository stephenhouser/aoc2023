#!/usr/bin/env python
"""
Advent of Code 2023 - Day 18: Lavaduct Lagoon
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile


class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example_flood(self):
        """Example solution for part 1, test.txt"""
        self.assertEqual(lagoon_volume_flood(load_file('test.txt')), 62)

    def test_part1_example_shoelace(self):
        """Example solution for part 1, test.txt"""
        self.assertEqual(lagoon_volume_shoelace(load_file('test.txt')), 62)

    def test_part1_solution_flood(self):
        """Solution for part 2, input.txt"""
        self.assertEqual(lagoon_volume_flood(load_file('input.txt')), 61661)

    def test_part1_solution_shoelace(self):
        """Solution for part 2, input.txt"""
        self.assertEqual(lagoon_volume_shoelace(load_file('input.txt')), 61661)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Example solution for part 2, test.txt"""
        volume = lagoon_volume_shoelace(load_file('test.txt', parse_instruction2))
        self.assertEqual(volume, 952408144115)

    def test_part2_solution(self):
        """Solution for part 2, input.txt"""
        volume = lagoon_volume_shoelace(load_file('input.txt', parse_instruction2))
        self.assertEqual(volume, 111131796939729)


def parse_instruction1(text):
    """Return a parsed instruction"""
    directions = {'U': complex(0, -1), 'D': complex(0, 1),
                  'L': complex(-1, 0), 'R': complex(1, 0)}

    direction_code, length, color_code = text.split()

    direction = directions[direction_code]
    length = int(length)
    color = re.findall(r'[0-9A-Za-z]+', color_code)[0]
    return (direction, length, color)

def parse_instruction2(text):
    """Return a parsed instruction"""
    directions = {'3': complex(0, -1), '1': complex(0, 1),
                  '2': complex(-1, 0), '0': complex(1, 0)}

    _, _, instruction_code = text.split()
    match = re.match(r'\(#([0-9A-Za-z]{5})([0-9A-Za-z]{1})\)', instruction_code)
    length = int(match.group(1), 16)
    direction = directions[match.group(2)]

    return (direction, length, 'AceAce')

def load_file(filename: str, parser=parse_instruction1):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # read a list of Directons
            return list(map(parser, file.readlines()))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

#
# Grid and complex number printing
#
def get_grid_size(grid):
    """Return the min and max coordinates of the grid"""
    min_x = min(x.real for x in grid)
    max_x = max(x.real for x in grid)

    min_y = min(y.imag for y in grid)
    max_y = max(y.imag for y in grid)

    #print(f'min={min_x}, {min_y}, max={max_x}, {max_y}')
    return complex(min_x, min_y), complex(max_x, max_y)

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

#
# Flood fill version - works o.k. for part 1, but too long!
#
# - Digs trench in complex() grid
# - Uses flood fill to fill interior
# - Counts number of filled locations
#
def lagoon_volume_flood(instructions):
    """Retur volume of lagoon using flood fill"""
    lagoon = dig_trench(instructions)

    flood_fill(lagoon, instructions)
    return len(lagoon)  # count the active locations

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
    grid_min, grid_max = get_grid_size(grid)

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
            while grid_min.real <= position.real <= grid_min.real+1 \
                and grid_max.imag <= position.imag <= grid_max.imag+1 \
                and not grid.get(neighbor):

                flood_fill_one(grid, neighbor, color)

            position += direction
            steps -= 1

        # TODO: Only need one fill on a single closed object
        break

    return position

#
# Shoelace version -- the better version
#
# - Does not do any digging!
# - Collects the list of verticies and the permiter distance
# - Uses shoelace algorithm to compute area
# - add to that 1/2 the permiter to get actual area (# are not zero size!)
#
def lagoon_volume_shoelace(instructions):
    """Return the number of filled grid locations"""            
    #lagoon = dig_trench(instructions)
    verticies, distance = lagoon_verticies(instructions)
    perimeter = distance // 2 + 1    # count sides as 1/2
    interior = shoelace(verticies)
    return interior + perimeter

def lagoon_verticies(instructions):
    """Return list of verticies generated in following instructions 
        and the distance travelled (perimiter of polygon).
    """
    position = complex(0, 0)
    points = []
    distance = 0
    for direction, steps, _ in instructions:
        position += direction * steps
        distance += steps
        points.append(position)
        #print(f'vertex: {c_str(position)}')

    return points, distance

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

        with Profile() as profile:
            #
            # Part One
            #

            # flood fill version
            instructions = load_file(filename)
            volume = lagoon_volume_flood(instructions)
            print(f'\t1. Lagoon volume (flood)   : {volume}')

            # shoelace version
            instructions = load_file(filename)
            volume = lagoon_volume_shoelace(instructions)
            print(f'\t1. Lagoon volume (shoelace): {volume}')

            #
            # Part Two
            #
            instructions = load_file(filename, parse_instruction2)
            volume = lagoon_volume_shoelace(instructions)
            print(f'\t1. Lagoon volume (shoelace): {volume}')

            print()
            profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
