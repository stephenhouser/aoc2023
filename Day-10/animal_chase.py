#!/usr/bin/env python
"""
Advent of Code 2023 - Day 10: Day 10: Pipe Maze
Stephen Houser <stephenhouser@gmail.com>
"""

import argparse
import math


def load_file(filename: str):
    """Load lines from file into a list of lists of characters
        
       filename: the file to read game descriptions from.
       returns: tuple of 
        - starting location
        - list of lists of characters describing the grid/map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return list(map(list, map(str.strip, file.readlines())))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def print_grid(grid):
    """Pretty print the grid using the marks we made"""
    for y in grid:
        print('\t', end='')
        for x in y:
            if len(x) == 2 and x[1] == '*':
                print(f'\x1b[1;31m{x[0]}\x1b[0m', end='')
            elif len(x) == 2 and x[1] == '+':
                print(f'\x1b[1m{x[0]}\x1b[0m', end='')
            elif len(x) == 2 and x[1] == '-':
                print(f'\x1b[1;33m{x[0]}\x1b[0m', end='')
            else:
                print(f'{x[0]}', end='')
        print()

def find_start(grid, start_char='S'):
    """Returns the (x, y) of the starting location
       Starting location has `start_char` value
    """
    for y, row in enumerate(grid):
        if start_char in row:
            return (row.index(start_char), y)

    # We should never get here, gauranteed to have a start tile
    return None

def get_next_tile(grid, tile):
    """Return the next tile to visit from the given tile.

       Preference given to N, then E, S, W. 
       Approximation of _always go right_ from maze solving.
    """

    next_tile = None
    (x, y, direction) = tile
    match (grid[y][x][0], direction):
        case ['-', 'W'] | ['J', 'S'] | ['7', 'N']:
            next_tile = (x-1, y, 'W')

        case ['-', 'E'] | ['F', 'N'] | ['L', 'S']:
            next_tile = (x+1, y, 'E')

        case ['|', 'S'] | ['F', 'W'] | ['7', 'E']:
            next_tile = (x, y+1, 'S')

        case ['|', 'N'] | ['J', 'E'] | ['L', 'W']:
            next_tile = (x, y-1, 'N')

    #print(f'\t{grid[y][x]} {tile} --> {next_tile}')
    if len(grid[y][x]) == 1:
        # Mark the tile as one we have traversed with a `*`
        grid[y][x] = grid[y][x] + '*'

    return next_tile

def find_path(grid, start):
    """Returns the tile and direction we should start at based on `start`
       being the starting tile.
    """
    (sx, sy) = start
    # north
    if  sy > 0 and grid[sy-1][sx][0] in '|7F':
        return (sx, sy-1, 'N')
    # east
    if sx < len(grid[0]) and grid[sy][sx+1][0] in '-J7':
        return (sx+1, sy, 'E')
    # south
    if sy < len(grid) and grid[sy+1][sx][0] in '|JL':
        return (sx, sy+1, 'S')
    # west
    if sx > 0 and grid[sy][sx-1][0] in '-FL':
        return (sx-1, sy, 'W')

    # Should never get here, start tile is gauranteed to have connections
    return None

def patch_tile(grid, tile):
    """Replace a missing `tile` in the grid with a tile that fits
       based on adjacent tiles.

       Used to deduce and set what the start tile should be.
    """
    (x, y) = tile
    (mx, my) = (len(grid[0]), len(grid))

    north = y > 0    and grid[y-1][x][0] in ('7', 'F', '|')
    south = y < my-1 and grid[y+1][x][0] in ('L', 'J', '|')
    west =  x > 0    and grid[y][x-1][0] in ('L', 'F', '-')
    east =  x < mx-1 and grid[y][x+1][0] in ('J', '7', '-')

    match (north, east, south, west):
        case (True, True, False, False):
            grid[y][x] = 'L'
        case (True, False, True, False):
            grid[y][x] = '|'
        case (True, False, False, True):
            grid[y][x] = 'J'
        case (False, True, True, False):
            grid[y][x] = 'F'
        case (False, True, False, True):
            grid[y][x] = '-'
        case (False, False, True, True):
            grid[y][x] = '7'

def same_tile(tile_1, tile_2):
    """Return True if the two tile specifications identify the same tile"""
    return tile_1[0] == tile_2[0] and tile_1[1] == tile_2[1]

def mark_tile(grid, tile, mark):
    """Add mark to the tile in the grid"""
    (x, y) = tile[:2]
    grid[y][x] = f'{grid[y][x][0]}' + mark

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        grid = load_file(filename)
        start = find_start(grid)

        #print_grid(grid)
        print(f'\tStart at: {start}\n')
        #
        # Part One
        #
        mark_tile(grid, start, '*') # mark starting tile as "on the path"
        tile = find_path(grid, start)
        trail = []
        while not same_tile(tile, start):
            trail.append(tile)
            tile = get_next_tile(grid, tile) # will also mark tiles

        farthest = math.ceil(len(trail)/2)

        #print_grid(grid)
        print(f'\t1. The farthest tile is: {farthest} steps away')
        print()

        #
        # Part Two
        #

        patch_tile(grid, start) # Replace starting tile with it's true form
        mark_tile(grid, start, '*') # mark starting tile as "on the path"

        # for each line count the enclosed ground symbols `.`
        enclosed_count = 0
        for i, y in enumerate(grid):
            crossings = 0
            started_with = None
            for j, x in enumerate(y):
                # sequences of `L---J` and `F---7` don't count as crossings,
                # they are the bottom and top of boxes.
                if x in ('F*', 'L*'):   # F, L might be start of box boundary
                    crossings += 1
                    started_with = x
                elif x == '7*' and started_with == 'F*':
                    crossings -= 1      # this was a box bounday, don't count
                    started_with = None
                elif x == 'J*' and started_with == 'L*':
                    crossings -= 1      # this was a box bounday, don't count
                    started_with = None

                if x == '|*':           # crossed a boundary
                    crossings += 1

                # of the crossings is odd we are "inside" the loop
                if len(x) == 1 and crossings != 0 and crossings % 2 == 1:
                    grid[i][j] = 'I+'   # mark cell for display
                    enclosed_count += 1

        #mark_tile(grid, start, '-')
        #print_grid(grid)
        print(f'\t2. There are {enclosed_count} enclosed tiles. (269)')
        print()

if __name__ == '__main__':
    main()
