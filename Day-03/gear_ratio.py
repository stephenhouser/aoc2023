#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
from functools import reduce
from collections import defaultdict

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

def parser(line: str):
    return line

def load_map(filename: str):
    """Load ___ from the given file
        
       filename: the file to read game descriptions from.
    """
    map = []
    try:
        with open(filename, 'r', encoding='utf-8') as gf:
            for line in gf.readlines():
                map.append(line.strip())

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return map

def map_symbols(map):
    symbol_map = []
    for line in map:
        symbol_line = []
        for char in list(line):
            if char.isdigit() or char == '.':
                symbol_line.append(False)
            else:
                symbol_line.append(True)

        symbol_map.append(symbol_line)

    return symbol_map

def set_touches(map, x, y):
    for ny in [-1, 0, 1]:
        for nx in [-1, 0, 1]:
            try:
                map[y+ny][x+nx] = True
            except IndexError:
                pass

def expand_symbols(map):
    nmap = [row[:] for row in map]
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x]:
                set_touches(nmap, x, y)

    return nmap

def number_touches(map, symbols):
    numbers = []
    for y in range(len(map)):
        for match in re.finditer(r'\d+', map[y]):
            num = int(match.group(0))
            span = match.span(0)

            touches = False
            for x in range(match.start(0), match.end(0)):
                if symbols[y][x]:
                    touches = True
            
            if touches:
                numbers.append(num)

    return numbers
            
def number_map(map, tm):
    # [ 543: [(x, y), (x, y)], ...]
    number_locs= defaultdict(list)
    for y in range(len(map)):
        for match in re.finditer(r'\d+', map[y]):
            num = int(match.group(0))
            for x in range(match.start(0), match.end(0)):
                number_locs[num] += [(x, y)]

def pp_map(map):
    for row in map:
        for cell in row:

            print(f'{cell:2}', end='')
        print()

map = load_map('input.txt')
symbol_map = map_symbols(map)
expand_map = expand_symbols(symbol_map)
pp_map(expand_map)

# nm = number_map(map)

number_list = number_touches(map, expand_map)
print(sum(number_list))

#
# Part 1
#


#
# Part 2
#
