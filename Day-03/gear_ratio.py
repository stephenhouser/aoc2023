#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
from functools import reduce
from itertools import chain


def load_map(filename: str) -> list[str]:
    """Load map of gears and parts from the given file
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as map_file:
            return list(map(str.strip, map_file.readlines()))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def find_symbols(engine_map: list[str]) -> list[tuple[str, tuple[int]]]:
    """Returns a list of (symbol, (x,y)) locations of symbols on map

       Example: [ ('*', (3, 4)), ('$', (4, 5)), ... ]
    """
    symbols = []
    for y, row in enumerate(engine_map):
        for match in re.finditer(r'[^\.\d]', row):
            symbol = match.group(0)
            symbol_loc = (match.start(0), y)
            symbols.append((symbol, symbol_loc))

    return symbols

def find_parts(engine_map: list[str]) -> list[tuple[str, tuple[int]]]:
    """Returns a list of (part_number, ((x1,y1), (x2,y2)) bounding boxes of 
       parts on map. Bounding boxes are (x1, y2), (x2, y2) where
       x1 <= x2 and y1 <= y2. In all cases y1 == y2.

       Example: [ (234, ((7,8), (9,8)), (123, ((4,5), (6,5)), ... ]
    """
    parts = []
    for y, row in enumerate(engine_map):
        for match in re.finditer(r'\d+', row):
            part_n = int(match.group(0))
            part_box = ((match.start(0), y), (match.end(0)-1, y))
            parts.append((part_n, part_box))

    return parts

def find_overlaps(box, parts) -> list[int]:
    """Returns list of part numbers from parts overlap the box"""

    # filter on a part's bounding box overlapping the given box
    return filter(lambda x: overlaps(box, x[1]), parts)

def overlapping_part_numbers(box, parts):
    """Return list of part numbers that overlap box."""
    # use find_overlapping to determine which parts overlap the given box
    # include only the part numbers in the result
    return list(map(lambda part: part[0], find_overlaps(box, parts)))

def find_connected_parts(symbols, parts):
    """Return list of connected parts
       [(symbol, [parts, ...])

       symbol -> box -> symbol, parts
       box 
    """
    # map make_box to symbol center points to get boxes that enclose symbols
    symbol_boxes = map(make_box, map(lambda x: x[1], symbols))
    # map symbol boxes to add overlapping part numbers using find overlaps
    return map(lambda box: overlapping_part_numbers(box, parts), symbol_boxes)

def make_box(center):
    """Return a box ((x1,y1), (x2,y2)) that surrounds a center point (x, y).

       This is a box "outset" by 1 on each side (top, left, bottom, right)
    """
    return ((center[0]-1, center[1]-1), (center[0]+1, center[1]+1))

def overlaps(box_a, box_b):
    """Return True of box_a overlaps box_b

       A box is defined as ((x1, y1), (x2, y2)) where x1 <= x2 and y1 <= y2
    """
    right_of = box_b[0][0] > box_a[1][0] # b is to the left of a
    left_of  = box_b[1][0] < box_a[0][0] # b is to the right of a
    above    = box_b[0][1] > box_a[1][1] # b is above a
    below    = box_b[1][1] < box_a[0][1] # b is below a

    return not (right_of or left_of or above or below)

## Debug and Print Utilities

def print_symbols(symbols, engine_map=None):
    """Pretty print the symbols found in the map"""
    for (symbol, center) in symbols:
        if engine_map:
            show_area(engine_map, center, f'Symbol {symbol}')
        else:
            print(f'{symbol}: {center}')

def print_parts(parts):
    """Pretty print the parts found in the map"""
    for p in parts:
        (part_n, box) = p
        print(f'{part_n:3}: {box}')

def show_area(engine_map, center, header=''):
    """Print the area surrounding the center point from the given map"""
    (x, y) = center

    print(header)
    for py in range(y-1, y+2):
        print('\t', end='')
        for px in range(x-1, x+2):
            try:
                print(engine_map[py][px], end='')
            except IndexError:
                pass
        print()

def symbol_stats(symbols, parts):
    """Print some statistics about the symbol occurrences in the map"""
    for n in ('!', '@', '#', '$', '%', '^', '&', '*'):
        n_symbols = list(filter(lambda x: x[0] == n, symbols))
        n_parts = find_connected_parts(n_symbols, parts)
        n_boxes = list(filter(lambda x: len(x) == 2, n_parts))
        print(f'{n} occurs {len(n_symbols)} times. {len(n_boxes)} of which connect to 2 parts')

#
# Part 1
#
def part_numbers(symbols, parts):
    """Return the part number sum for the symbols and parts."""
    connected = find_connected_parts(symbols, parts)
    return chain(*connected)

#
# Part 2
#
def gear_ratios(symbols, parts):
    """Return the gear ratio for the symbols and parts."""

    # Maybe I got lucky, but only the gear (*) symbol connected
    # to exactly two parts across all my input. This makes the filter
    # for gear_symbols kind of useless...
    #
    # ! occurs 0 times. 0 of which connect to 2 parts
    # @ occurs 52 times. 0 of which connect to 2 parts
    # # occurs 51 times. 0 of which connect to 2 parts
    # $ occurs 35 times. 0 of which connect to 2 parts
    # % occurs 45 times. 0 of which connect to 2 parts
    # ^ occurs 0 times. 0 of which connect to 2 parts
    # & occurs 38 times. 0 of which connect to 2 parts
    # * occurs 367 times. 325 of which connect to 2 parts
    #symbol_stats(symbols, parts)

    gear_symbols = list(filter(lambda x: x[0] == '*', symbols))
    connected_parts = find_connected_parts(gear_symbols, parts)
    gear_boxes = filter(lambda x: len(x) == 2, connected_parts)
    gear_ratios = map(lambda x: x[0] * x[1], gear_boxes)
    return gear_ratios


def main():
    """Main Routine"""
    #engine_map = load_map('test-1.txt')  # 4361
    engine_map = load_map('input.txt')  # 4361

    symbols = find_symbols(engine_map)
    #print('--- Symbols ---')
    #print_symbols(symbols)

    parts = find_parts(engine_map)
    #print('--- Parts ---')
    #print_parts(parts)

    #
    # Part 1
    #
    part_sum = sum(part_numbers(symbols, parts))
    print(f'The sum of the connected part numbers is: {part_sum} (4631, 527446)')

    #
    # Part 2
    #
    gear_ratio_sum = sum(gear_ratios(symbols, parts))
    print(f'The sum of the gear ratios is: {gear_ratio_sum} (467835, 73201705)')


main()
