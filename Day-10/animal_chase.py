#!/usr/bin/env python
"""
Advent of Code 2023 - Day 10: Day 10: Pipe Maze
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import math

def load_file(filename: str):
    """Load lines from file into a list of ITEMS
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            start = (0, 0)
            lines = []
            for y, line in enumerate(file.readlines()):
                l = list(line.strip())
                lines.append(l)

                if 'S' in line:
                    start = (line.index('S'), y)

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return (start, lines)

def next_tile(tile, grid):
    # always go N, E, S, W
    next_tile = None
    (x, y, direction) = tile
    match (grid[y][x], direction):
        case ['-', 'W']:
            next_tile = (x-1, y, 'W')

        case ['-', 'E']:
            next_tile = (x+1, y, 'E')

        case ['|', 'S']:
            next_tile = (x, y+1, 'S')

        case ['|', 'N']:
            next_tile = (x, y-1, 'N')

        case ['J', 'E']:
            next_tile = (x, y-1, 'N')

        case ['J', 'S']:
            next_tile = (x-1, y, 'W')

        case ['F', 'W']:
            next_tile = (x, y+1, 'S')

        case ['F', 'N']:
            next_tile = (x+1, y, 'E')

        case ['7', 'E']:
            next_tile = (x, y+1, 'S')

        case ['7', 'N']:
            next_tile = (x-1, y, 'W')

        case ['L', 'S']:
            next_tile = (x+1, y, 'E')

        case ['L', 'W']:
            next_tile = (x, y-1, 'N')

    print(f'\t{grid[y][x]} {tile} --> {next_tile}')
    return next_tile

def print_grid(grid):
    for y in grid:
        for x in y:
            print(x, end='')
        print()

def find_path(start, grid):
    (sx, sy) = start
    # north
    if  sy > 0 and grid[sy-1][sx] in '|7F':
        return (sx, sy-1, 'N')
    # east
    if sx < len(grid[0]) and grid[sy][sx+1] in '-J7':
        return (sx+1, sy, 'E')
    # south
    if sy < len(grid) and grid[sy+1][sx] in '|JL':
        return (sx, sy+1, 'S')
    # west
    if sx > 0 and grid[sy][sx-1] in '-FL':
        return (sx-1, sy, 'W')

def is_animal(tile, grid):
    (x, y, _) = tile
    return grid[y][x] == 'S'

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        (start, grid) = load_file(filename)

        #
        # Part One
        #
        print(f'\tStart at: {start}')
        print_grid(grid)

        tile = find_path(start, grid)
        print(f'\tStart {tile}')
        count = 0
        trail = []
        while not is_animal(tile, grid):
            trail.append(tile)
            tile = next_tile(tile, grid)
            print(tile)
            count += 1

        far = math.ceil(len(trail)/2)
        print(far)

        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
