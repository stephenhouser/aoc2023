#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import sys
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


def show_area(map, x, y):
    for py in range(y-2, y+3):
        print('\t', end='')
        for px in range(x-2, x+3):
            try:
                print(map[py][px], end='')
            except IndexError:
                pass
        print()
    
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

def gear_symbols(map):
    symbol_map = []
    for line in map:
        symbol_line = []
        for char in list(line):
            if char == '*':
                symbol_line.append(True)
            else:
                symbol_line.append(False)

        symbol_map.append(symbol_line)

    return symbol_map

def find_parts(map):
    parts = []
    for y in range(len(map)):
        for match in re.finditer(r'\d+', map[y]):
            part_n = int(match.group(0))
            parts.append( (part_n, ( (match.start(0), y), (match.end(0)-1, y) ) ))

    return parts

def find_gear_symbols(map):
    gears = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '*':
                gears.append(((x-1, y-1), (x+1, y+1)))
                             
    return gears

def overlapA(a, b):
    # (x, y), (x, y)
    # [00] 01  10 11
    a_width = abs(a[0][0] - a[1][0])
    b_width = abs(b[0][0] - b[1][0])
    a_height = abs(a[0][1] - a[1][1])
    b_height = abs(b[0][1] - b[1][1])
    return (abs(a[0][0] - b[0][0]) * 2 < (a_width + b_width)) and \
           (abs(a[0][1] - b[0][1]) * 2 < (a_height + b_height))

def overlap(a, b):
    # left [0][0]   right [1][0]
    # top [0][1]     bottom [1][1]
    # if b[0][0] > a[1][0] or  # b.left > a.right
    #     b[1][0] < a[0][0] or # b.right < a.left
    #     b[0][1] > a[1][1] or # b.top < a.bottom
    #     b[1][1] < a[0][1]:   # b.bottom < a.top
    if b[0][0] > a[1][0] or  \
        b[1][0] < a[0][0] or \
        b[0][1] > a[1][1] or \
        b[1][1] < a[0][1]:   

        return False

    return True

def find_connected_parts(gear, parts):
    touches_parts = []
    for (part_n, part_box) in parts:
        if overlap(gear, part_box):
            touches_parts.append(part_n)

    return touches_parts

def find_gears(gear_s, parts, og_map):
    gears = []
    ratios = []
    for gear in gear_s:
        #show_area(og_map, gear[0][0]+1, gear[0][1]+1)

        touches_parts = []
        print(f'Gear {gear}')
        for (part_n, part_box) in parts.items():
            if overlap(gear, part_box):
                touches_parts.append(part_n)
                print('\tpart ', part_n, part_box)

        if len(touches_parts) == 2:
            gears.extend(touches_parts)
            ratios.append(touches_parts[0] * touches_parts[1])

    return ratios

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
            for x in range(match.start(0), match.end(0)-1):
                if symbols[y][x]:
                    touches = True
            
            if touches:
                numbers.append(num)

    return numbers
            
# def number_map(map, tm):
#     # [ 543: [(x, y), (x, y)], ...]
#     number_locs= defaultdict(list)
#     for y in range(len(map)):
#         for match in re.finditer(r'\d+', map[y]):
#             num = int(match.group(0))
#             for x in range(match.start(0), match.end(0)):
#                 number_locs[num] += [(x, y)]

def pp_map(map):
    for row in map:
        for cell in row:
            print(f'{cell:2}', end='')
        print()


#og_map = load_map('test-1.txt')
og_map = load_map('input.txt')
#symbol_map = map_symbols(og_map)
#expand_map = expand_symbols(symbol_map)

# nm = number_map(map)

#number_list = number_touches(og_map, expand_map)
#print(sum(number_list))


gears = find_gear_symbols(og_map)
parts = find_parts(og_map)
gear_ratios = []
for g in gears:
    print(f'Gear {g}')
    show_area(og_map, g[0][0]+1, g[0][1]+1)
    connected = find_connected_parts(g, parts)
    if len(connected) == 2:
        gear_ratios.append(connected[0] * connected[1])
    print(connected)
    print()

print(sum(gear_ratios))

#print('Symbols', gears)
#print('Parts', parts)
#gears = find_gears(gears, parts, og_map)
#print(sum(gears))
#print(len(gears))


#expand_gears = expand_symbols(gear_map)
#p_map(expand_gears)


#
# Part 1
#


#
# Part 2
#
# 127 gears
# 28818010 too low