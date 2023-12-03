#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
from functools import reduce
from itertools import chain

# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..

def load_map(filename: str):
    """Load map of gears and parts from the given file
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as gf:
            return list(map(str.strip, gf.readlines()))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def find_symbols(map):
    """Returns list of (x,y) locations of symbols on map"""
    symbols = []
    for y, row in enumerate(map):
        for match in re.finditer('[^\.\d]', row):
            symbol = match.group(0)
            symbol_loc = (match.start(0), y)
            symbols.append((symbol, symbol_loc))

    return symbols

def filter_symbols(symbols, match):
    return list(filter(lambda x: x[0] == match, symbols))

def find_parts(map):
    parts = []
    for y, row in enumerate(map):
        for match in re.finditer(r'\d+', row):
            part_n = int(match.group(0))
            part_box = ( (match.start(0), y), (match.end(0)-1, y) ) 
            parts.append( (part_n, part_box))

    return parts

def make_gearbox(symbol, margin=1):
    (s, center) = symbol
    return (s, ((center[0] - margin, center[1] - margin),
                (center[0] + margin, center[1] + margin)))


def find_overlaps(gear_box, parts):
    """Returns which part numbers overlap the gear_box"""
    return filter(lambda x: overlaps(gear_box, x[1]), parts)
                       

def find_connected_parts(symbols, parts):
    """Return list of connected parts
       [(symbol, [parts, ...])
    """
    gear_boxes = list(map(make_gearbox, symbols))

    connected = [] 
    for (symbol, gear_box) in gear_boxes:
        overlapping_parts = find_overlaps(gear_box, parts)
        overlappint_part_numbers = map(lambda part: part[0], overlapping_parts)
        connected.append(list(overlappint_part_numbers))

    return connected


## Utilities

def print_symbols(symbols, map=None):
    for (symbol, center) in symbols:
        if map:
            show_area(map, center, f'Symbol {symbol}')
        else:
            print(f'{symbol}: {center}')

def print_parts(parts):
    for p in parts:
        (part_n, box) = p
        print(f'{part_n:3}: {box}')

def show_area(map, center, header=''):
    (x, y) = center

    print(header)
    for py in range(y-1, y+2):
        print('\t', end='')
        for px in range(x-1, x+2):
            try:
                print(map[py][px], end='')
            except IndexError:
                pass
        print()

def overlaps(a, b):
    """Return True of box a overlaps box b

       a box is defined as ((x1, y1), (x2, y2)) where x1 <= x2 and y1 <= y2
    """
    right_of = b[0][0] > a[1][0] # b is to the left of a
    left_of  = b[1][0] < a[0][0] # b is to the right of a
    above    = b[0][1] > a[1][1] # b is above a
    below    = b[1][1] < a[0][1] # b is below a

    return not (right_of or left_of or above or below)


#
# Loading...
#
engine_map = load_map('test-1.txt')  # 4361
engine_map = load_map('input.txt')  # 4361

symbols = find_symbols(engine_map)
parts = find_parts(engine_map)

#print('--- Symbols ---')
#print_symbols(symbols)

#print('--- Parts ---')
#print_parts(parts)

#
# Part 1
#
connected = find_connected_parts(symbols, parts)
connected_part_sum = sum(chain(*connected))
print(f'The sum of the connected part numbers is: {connected_part_sum}')


#
# Part 2
#
# 127 gears
# 28818010 too low
gear_symbols = filter_symbols(symbols, '*')
connected_parts = find_connected_parts(symbols, parts)
gear_boxes = filter(lambda x: len(x) == 2, connected_parts)
gear_ratios = map(lambda x: x[0] * x[1], gear_boxes)
print(f'The sum of the gear ratios is: {sum(gear_ratios)}')
