#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
from heapq import heappush, heappop

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Part 1 solution for test.txt"""
        things = load_file('test.txt')
        result = len(things)
        self.assertEqual(result, 10)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        things = load_file('input.txt')
        result = len(things)
        self.assertEqual(result, 10)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Part 2 solution for test.txt"""
        things = load_file('test.txt')
        result = len(things)
        self.assertEqual(result, 10)

    def test_part2_solution(self):
        """Part 2 solution for input.txt"""
        things = load_file('input.txt')
        result = len(things)
        self.assertEqual(result, 10)


def c_str(cplx):
    """Pretty print a complex number as (i,j)"""
    return f'({int(cplx.real)}, {int(cplx.imag)})'

def ascii_color(hex_color, text):
    """Return text in ASCII color"""
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

class Map:
    """Represents a ___"""
    def __init__(self, map_data):
        self.rows = 0
        self.cols = 0
        self.start = None
        self.finish = None
        self._map = None
        self.load_map(map_data)

    def get(self, x, y=None):
        if isinstance(x, complex):
            return self._map.get(x)

        return self._map.get(complex(x,y))

    def infinite_get(self, position):
        x = position.real % self.cols
        y = position.imag % self.rows
        return self.get(complex(int(x),int(y)))

    def load_map(self, map_data):
        if isinstance(map_data, str):
            lines = map_data.split('\n')
        else:
            lines = map_data

        self._map = {complex(i,j): c for j, r in enumerate(lines)
                     for i, c in  enumerate(r.strip()) if c != '#'}

        self.rows = int(max([n.imag for n in self._map]))+1
        self.cols = int(max([n.real for n in self._map]))+1+1

        self.start = complex(1,0)
        self.finish = complex(self.cols-2, self.rows-1)

    def get_start(self):
        starts = list(filter(lambda x: self._map[x] == 'S', self._map))

        assert len(starts) == 1
        return starts[0]

    def print(self, highlights=None):
        print('start', c_str(self.start), self.get(self.start))
        print('finish', c_str(self.finish), self.get(self.finish))

        """Pretty print 2D grid in readable form"""
        print('  ', end='')
        _ = [print(f'{x%10}', end='') for x in range(self.cols)]
        print('\n :', end='')
        _ = [print('-', end='') for x in range(self.cols)]
        for y in range(self.rows):
            print(f'\n{y%10}:', end='')
            for x in range(self.cols):
                symbol = self.get(x, y)
                if not symbol:
                    print(ascii_color('777777', '~'), end='')
                elif highlights and complex(x,y) in highlights:
                    print(ascii_color('ffffff', symbol), end='')
                elif complex(x,y) in (self.start, self.finish):
                    print(ascii_color('ff0000', symbol), end='')
                else:
                    print(symbol, end='')

        print()

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'Empty'

def find_nodes(trail_map):
    nodes = [trail_map.start, trail_map.finish]
    for spot in trail_map._map:
        neighbors = []
        for direction in (1, -1, 1j, -1j):
            n = trail_map.get(spot+direction)
            if n and n != '#':
                neighbors.append(spot+direction)

        if len(neighbors) >= 3:
            print('Node:', c_str(spot), neighbors)
            nodes.append(spot)

    return nodes

def symbol_dir(symbol, direction):
    if not symbol:
        return False

    if symbol == '.':
        return True

    if symbol == '#':
        return False

    match symbol, direction:
        case '^', -1j:
            return True
        case 'v', 1j:
            return True
        case '<', -1:
            return True
        case '>', 1:
            return True

    return False

def find_neighbors(trail_map, nodes, spot):
    neighbors = []
    open_l = [(0, spot)]
    visited = set()
    visited.add(spot)

    print(f'Find neighbors for {spot}')
    while open_l:
        steps, position = open_l.pop()

        for direction in (1, -1, 1j, -1j):
            neighbor = position+direction
            if neighbor not in visited:
                visited.add(neighbor)

                neighbor_symbol = trail_map.get(neighbor)
                if symbol_dir(neighbor_symbol, direction):
                    if neighbor in nodes:
                        print(f'\tfound {neighbor} {neighbor_symbol}')
                        neighbors.append((neighbor, steps+1))
                    else:
                        print(f'\twalk {neighbor} {neighbor_symbol}')
                        open_l.append((steps+1, neighbor))

    return neighbors

def find_paths(trail_map):
    nodes = find_nodes(trail_map)
    neighbors = []
    for node in nodes:
        neighbors.append(find_neighbors(trail_map, nodes, node))

    return dict(zip(nodes, neighbors))

# def find_path(trail_map):
#     open = []
#     closed = {}

#     heappush(open, (0, (trail_map.start.real, trail_map.start.imag)))
#     while open:
#         steps, position = heappop(open)
#         closed[complex(*position)] = steps

#         for direction in (1, -1, 1j, -1j):
#             neighbor = complex(*position) + direction
#             if trail_map.get(neighbor) and neighbor not in closed:
#                 n = trail_map.get(neighbor)
#                 if n == '.' or (n, direction) in (('^', -1j), ('v', 1j), ('<', -1), ('>', 1)):
#                     heappush(open, (steps-1, (neighbor.real, neighbor.imag)))

#     path = closed[trail_map.finish]
#     print(path)
#     return -path

def c_tup(cplx):
    return (cplx.real, cplx.imag)

def find_long(nodes):

    # [((1+0j), [((17+5j), 61)])
    #  (node, [neighbors]) neighbors are (node, steps)
    tentative = []
    confirmed = set()

    first = list(nodes.keys())[0]
    heappush(tentative, (0, c_tup(first)))
    while tentative:
        distance, node = heappop(tentative)
        print(f'evaluate {node}, {distance} steps')

        confirmed.add((distance, node))

        print(f'confirmed {node}, {distance} steps')
        for n in nodes[complex(*node)]:
            print(n)
            print(f'\ttentative {n[0]}, {distance-n[1]} steps')
            heappush(tentative, (distance-n[1], c_tup(n[0])))

    small = 0
    for c in confirmed:
        if c[0] < small:
            small = c[0]
    print(confirmed)
    print(small)


def print_dot(nodes):
    print(nodes)
    def p_node(node):
        return f'{int(node.real):03}{int(node.imag):03}'

    print('digraph {')
    for node in nodes:
        # ((1+0j), [((3+5j), 15)])
        pos, neighbors = node
        for n in neighbors:
            print(f'{p_node(pos)} -> {p_node(n[0])} [label="{n[1]}"]')

    print('}')

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return Map(file)

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            trail_map = load_file(filename)

            trail_map.print()
            #
            # Part One
            #
            # 2_102 too low
            # 2_186
            nodes = find_paths(trail_map)
            for n, v in nodes.items():
                print(n, '->', v)
            # trail_map.print()
            # print_dot(nodes)

            find_long(nodes)


            #
            # Part Two
            #
            # n_things = len(things)
            # print(f'\t2. umber of things: {n_things:,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
