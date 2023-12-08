#!/usr/bin/env python
"""
Advent of Code 2023 - Day 8: Haunted Wasteland
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import math
from functools import partial

class Node:
    """Represents a node in the map to traverse"""

    def __init__(self, text):
        """Initialize from text string"""
        match = re.match(r'(\w+) = \((\w+), (\w+)\)', text)
        self.label = match.group(1)
        self.left = match.group(2)
        self.right = match.group(3)

    def __repr__(self):
        """Return REPL for Node"""
        return str(self)

    def __str__(self):
        """Return str for Node"""
        return f'{self.label} = ({self.left}, {self.right})'

def load_file(filename: str):
    """Load directions and nodes from file
        
       filename: the file to read game descriptions from.
       returns: tuple (directions, nodes)
    """
    directions = []
    nodes = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            directions = list(next(file).strip())
            next(file)

            for line in file.readlines():
                node = Node(line)
                nodes[node.label] = node

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return (directions, nodes)

def print_nodes(nodes):
    """Pretty print nodes"""
    for (label, node) in nodes.items():
        if label[2] == 'A':
            print(f'{label} = ({node.left}, {node.right})')

def traverse(is_end_func, node, directions, nodes):
    """Return the number of steps to traverse
        - starting from `node`
        - ending when is_end_func(node.label) returns True
        - using `directions` for each step
        - using `nodes` as the mappings.

       returns: number of steps/mappings
    """
    steps = 0
    while not is_end_func(node.label):
        direction = directions[steps % len(directions)]
        steps += 1

        label = node.left if direction == 'L' else node.right
        node = nodes[label]

    return steps

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        (directions, nodes) = load_file(filename)

        #print(f'Directions: {directions}')
        #print_nodes(nodes)

        #
        # Part One
        #

        # Start with 'AAA'
        start_node = nodes['AAA']
        # partial function to traverse from start node to 'ZZZ' node
        traverse_3z = partial(traverse, lambda l: l == 'ZZZ',
                              directions=directions, nodes=nodes)
        steps = traverse_3z(start_node)
        print(f'\t1. It took {steps} steps to traverse from \'AAA\' to \'ZZZ\'')

        #
        # Part Two
        #

        # start with any node with a label ending with 'A'
        start_nodes = filter(lambda x: x.label[2] == 'A', nodes.values())

        # partial function to traverse from start node to 'xxZ' nodes
        traverse_1z = partial(traverse, lambda l: l[2] == 'Z',
                              directions=directions, nodes=nodes)

        # map traversal onto all start nodes, get list of steps for each
        steps = map(traverse_1z, start_nodes)

        # least common multiple is where they will converge
        lcm = math.lcm(*list(steps))

        print(f'\tIt took {lcm} steps to traverse the map.')

        print()

if __name__ == '__main__':
    main()
