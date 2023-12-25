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
from collections import defaultdict

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

def c_tup(cplx):
    """Return a tuple(x,y) from a complex(x,y)"""
    return (int(cplx.real), int(cplx.imag))

def ascii_color(hex_color, text):
    """Return text in ASCII color"""
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

class Node:
    def __init__(self):
        self.x = None
        self.y = None
        self.neighbors = None

class Map:
    """Represents a ___"""
    def __init__(self, map_data):
        self.rows = 0
        self.cols = 0
        self.start = None
        self.finish = None
        self._map = None
        self.nodes = defaultdict(list)
        self.load_map(map_data)

    def get(self, x, y=None):
        """Return symbol at position on the map"""
        if isinstance(x, complex):
            return self._map.get(x)

        return self._map.get(complex(x,y))

    def infinite_get(self, position):
        """Return symbol at position on the map
            as if the map were infinite copies of itself
        """
        x = position.real % self.cols
        y = position.imag % self.rows
        return self.get(complex(int(x),int(y)))

    def load_map(self, map_data):
        """Load the map from map_data"""
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
        """Return the start location on the map"""
        starts = list(filter(lambda x: self._map[x] == 'S', self._map))

        assert len(starts) == 1
        return starts[0]

    def get_nodes(self):
        """Returns dictionary of nodes on the map, keys are complex(x,y).
            Nodes are where two or more paths join
        """
        if not self.nodes:
            nodes = {}
            nodes[self.start] = []
            nodes[self.finish] = []

            for location in self._map:
                adjacent = []
                for direction in (1, -1, 1j, -1j):
                    symbol = self.get(location+direction)
                    if symbol and symbol != '#':
                        adjacent.append(location+direction)

                if len(adjacent) >= 3: # and not location in nodes:
                    nodes[location] = []

            self.nodes = nodes

        return self.nodes

    def print(self, highlights=None):
        """Pretty print map in readable form"""

        print('start', c_str(self.start), self.get(self.start))
        print('finish', c_str(self.finish), self.get(self.finish))

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

def symbol_direction(symbol, direction):
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

def find_neighbors(trail_map, node):
    neighbors = []
    paths = [(0, node)]

    # to prevent backtracking
    visited = set()
    visited.add(node)

    # print(f'Find neighbors for {node}')
    while paths:
        distance, position = paths.pop()

        for direction in (1, -1, 1j, -1j):
            neighbor = position+direction
            if neighbor not in visited:
                visited.add(neighbor)
                symbol = trail_map.get(neighbor)
                if symbol and symbol_direction(symbol, direction):
                    if neighbor in trail_map.get_nodes():
                        # print(f'\tfound {neighbor} {neighbor_symbol}')
                        neighbors.append((neighbor, distance+1))
                    else:
                        # print(f'\twalk {neighbor} {neighbor_symbol}')
                        paths.append((distance+1, neighbor))

    # returns list[tuple(node: complex, distance: int)]
    return neighbors

def get_node_neighbors(trail_map):
    neighbors = []
    for node in trail_map.get_nodes():
        neighbors.append(find_neighbors(trail_map, node))

    return dict(zip(trail_map.get_nodes(), neighbors))

def find_longest_directional_path(trail_map):
    nodes = get_node_neighbors(trail_map)

    # [((1+0j), [((17+5j), 61)])
    #  (node, [neighbors]) neighbors are (node, steps)
    tentative = []
    confirmed = set()

    first = list(nodes.keys())[0]
    heappush(tentative, (0, c_tup(first)))
    while tentative:
        distance, node = heappop(tentative)
        # print(f'evaluate {node}, {distance} steps')

        confirmed.add((distance, node))

        # print(f'confirmed {node}, {distance} steps')
        for n in nodes[complex(*node)]:
            # print(f'\ttentative {n[0]}, {distance-n[1]} steps')
            heappush(tentative, (distance-n[1], c_tup(n[0])))

    longest = -min(map(lambda x: x[0], confirmed))
    return longest

####

def find_all_neighbors(trail_map, node):
    neighbors = dict()
    paths = [(0, node)]

    # to prevent backtracking
    visited = set()
    visited.add(node)

    # print(f'Find neighbors for {node}')
    while paths:
        distance, position = paths.pop()

        for direction in (1, -1, 1j, -1j):
            neighbor = position+direction
            if neighbor not in visited:
                visited.add(neighbor)
                symbol = trail_map.get(neighbor)
                if symbol and symbol and symbol in ('.', '^', 'v', '<', '>'):
                    if neighbor in trail_map.get_nodes():
                        # print(f'\tfound {neighbor} {neighbor_symbol}')
                        neighbors[neighbor] = distance+1
                    else:
                        # print(f'\twalk {neighbor} {neighbor_symbol}')
                        paths.append((distance+1, neighbor))

    # returns list[tuple(node: complex, distance: int)]
    return neighbors

def get_all_neighbors(trail_map):
    neighbors = []
    for node in trail_map.get_nodes():
        neighbors.append(find_all_neighbors(trail_map, node))

    return dict(zip(trail_map.get_nodes(), neighbors))


def find_longest_pathXXX(trail_map):
    nodes = get_all_neighbors(trail_map)

    for n, neigh in nodes.items():
        print(n, neigh)

    tentative = []
    confirmed = set()

    heappush(tentative, (0, c_tup(trail_map.start)))
    while tentative:
        distance, node = heappop(tentative)

        if (distance, node) in confirmed:
            continue

        print(f'confirmed {node}, {distance} steps')
        confirmed.add((distance, node))

        for n, d in nodes[complex(*node)].items():
            print(f'\ttentative {n}, {distance-d} steps')
            heappush(tentative, (distance-d, c_tup(n)))

    longest = -min(map(lambda x: x[0], confirmed))
    return longest

def search(node, nodes, distance, longest, seen, trail_map):
    # print(f'search {node}, nodes, {distance}, seen, map')
    if node == trail_map.finish:
        return distance
    
    if node in seen:
        return longest
    
    seen.add(node)
    # search neigibors for longest path
    # print('distance', distance)
    for neigh, d in nodes[node].items():
        # print(f'\t check {neigh} {d}')
        ddd = search(neigh, nodes, distance+d, longest, seen, trail_map)
        if ddd > longest:
            longest = ddd

    seen.remove(node)
    return longest

def find_longest_path(trail_map):
    nodes = get_all_neighbors(trail_map)
    start = trail_map.start

    return search(start, nodes, 0, 0, set(), trail_map)



####

def print_dot(nodes):
    """Print GraphViz `.dot` digraph of nodes"""
    def p_node(node):
        return f'{int(node.real):03}{int(node.imag):03}'

    print('digraph {')
    for node, neighbors in nodes.items():
        for n in neighbors:
            if node in nodes[n]:
                print(f'{p_node(node)} -- {p_node(n[0])} [label="{n[1]}"]')
            else:
                print(f'{p_node(node)} -> {p_node(n[0])} [label="{n[1]}"]')

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

            # trail_map.print()
            # print_dot(get_node_neighbors(trail_map))

            #
            # Part One
            #

            # 2_186
            longest_path = find_longest_directional_path(trail_map)
            print(f'\t1. The longest directional path is: {longest_path:,}')

            #
            # Part Two
            #
            longest_path = find_longest_path(trail_map)
            print(f'\t2. The longest overall path is: {longest_path:,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
