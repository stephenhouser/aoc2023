#!/usr/bin/env python
"""
Advent of Code 2023 - Day 23: A Long Walk
Stephen Houser <stephenhouser@gmail.com>
"""

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
        longest_path = find_longest_directional_path(load_file('test.txt'))
        self.assertEqual(longest_path, 94)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        longest_path = find_longest_directional_path(load_file('input.txt'))
        self.assertEqual(longest_path, 2_186)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Part 2 solution for test.txt"""
        longest_path = find_longest_undirected_path(load_file('test.txt'))
        self.assertEqual(longest_path, 154)

    def test_part2_solution(self):
        """Part 2 solution for input.txt"""
        longest_path = find_longest_undirected_path(load_file('input.txt'))
        self.assertEqual(longest_path, 6_802)


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

    # def get_start(self):
    #     """Return the start location on the map"""
    #     starts = list(filter(lambda x: self._map[x] == 'S', self._map))

    #     assert len(starts) == 1
    #     return starts[0]

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

def find_neighbors(trail_map, node, check_neighbor):
    """Return list of neighbors for a node.
        Use check_neighbor to check if traversal is valid with given direction
    """
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
                if symbol and check_neighbor(symbol, direction):
                    if neighbor in trail_map.get_nodes():
                        # print(f'\tfound {neighbor} {neighbor_symbol}')
                        neighbors[neighbor] = distance+1
                    else:
                        # print(f'\twalk {neighbor} {neighbor_symbol}')
                        paths.append((distance+1, neighbor))

    # returns list[tuple(node: complex, distance: int)]
    return neighbors

def get_node_neighbors(trail_map, check_neighbor):
    """Return list of nodes and their neighbors
        Use check_neighbor to check if traversal is valid.
    """
    neighbors = []
    for node in trail_map.get_nodes():
        neighbors.append(find_neighbors(trail_map, node, check_neighbor))

    return dict(zip(trail_map.get_nodes(), neighbors))

def is_valid_direction(symbol, direction):
    """Return True if the given symbol can be traversed in direction"""
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

def find_longest_directional_path(trail_map):
    """Return the length of the longest path using directional paths."""
    # Effectively Dijkstra's with the node weights negated (-G)
    # Then reutrn the - of the shortest found path
    nodes = get_node_neighbors(trail_map, is_valid_direction)

    tentative = []
    confirmed = set()

    heappush(tentative, (0, c_tup(trail_map.start)))
    while tentative:
        distance, node = heappop(tentative)
        confirmed.add((distance, node))
        # print(f'confirmed {node}, {distance} steps')

        # Cannot early return here as we need to find the smallest
        # if node == c_tup(trail_map.finish):
        #     return distance

        for neighbor, neighbor_distance in nodes[complex(*node)].items():
            # print(f'\ttentative {neighbor}, {distance-neighbor_distance} steps')
            heappush(tentative, (distance-neighbor_distance, c_tup(neighbor)))

    longest = -min(map(lambda x: x[0], confirmed))
    return longest

####
def exhaustive_search(node, distance, longest, seen, nodes, finish):
    """Return the length of the longest path using non-directional paths."""
    # Exhaustive n! search of all paths to find the one with the longest length.

    # print(f'search {node}, nodes, {distance}, seen, map')
    if node == finish:
        return distance

    # avoid back-tracking
    if node in seen:
        return longest

    seen.add(node)
    # search neigibors for longest path
    for neighbor, neighbor_distance in nodes[node].items():
        neighbor_path = exhaustive_search(neighbor,
                                          distance+neighbor_distance,
                                          longest,
                                          seen, nodes, finish)
        if neighbor_path > longest:
            longest = neighbor_path

    seen.remove(node)
    return longest

def is_symbol_valid(symbol, _):
    """Returns if the symbol is traversable, ignoring direction (part 2)"""
    return symbol in ('.', '^', 'v', '<', '>')

def find_longest_undirected_path(trail_map):
    """Return the length of the longest path using non-directed paths."""
    # Need to do an exhaustive n! search of all the nodes and paths
    # This is an NP-Hard problem!
    nodes = get_node_neighbors(trail_map, is_symbol_valid)
    start = trail_map.start
    finish = trail_map.finish

    return exhaustive_search(start, 0, 0, set(), nodes, finish)


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
            # 6_802
            longest_path = find_longest_undirected_path(trail_map)
            print(f'\t2. The longest overall path is: {longest_path:,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
