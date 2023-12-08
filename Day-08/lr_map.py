#!/usr/bin/env python
"""
Advent of Code 2023 - Day 8: Haunted Wasteland
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
from functools import partial

class Node:
    def __init__(self, text):
        match = re.match(r'(\w+) = \((\w+), (\w+)\)', text)
        self.label = match.group(1)
        self.left = match.group(2)
        self.right = match.group(3)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.label} = ({self.left}, {self.right})'

def load_file(filename: str):
    """Load lines from file into a list of ITEMS
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
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
    for (label, node) in nodes.items():
        if label[2] == 'A':
            print(f'{label} = ({node.left}, {node.right})')

def traverse(directions, nodes):
    """Return steps to traverse nodes using directions"""

    steps = 0
    node = nodes['AAA']
    while node.label != 'ZZZ':
        direction = directions[steps % len(directions)]
        steps += 1
        #print(f'{label}: {direction} ->', end='')

        label = node.left if direction == 'L' else node.right
        #print(f'{label}')
        node = nodes[label]

    return steps

def traverse_multiple(directions, nodes):
    """Return steps to traverse nodes using directions"""

    steps = 0
    start_nodes = list(filter(lambda x: x.label[2] == 'A', nodes.values()))
    current = start_nodes
    end_z = []

    while len(end_z) != len(start_nodes):

        direction = directions[steps % len(directions)]
        steps += 1

        next_nodes = []
        print(f'{steps:10}: ', end='')
        for node in current:
            label = node.left if direction == 'L' else node.right
            next_nodes.append(nodes[label])
            c = '*' if label[2] == 'Z' else ' '
            print(f'{node.label}:{direction} -> {nodes[label].label}{c} ', end='')

        current = next_nodes
        end_z = list(filter(lambda x: x.label[2] == 'Z', current))
        print(len(end_z), '*' * len(end_z))

    return steps


def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        (directions, nodes) = load_file(filename)

        #
        # Part One
        #
        #print(f'Directions: {directions}')
        #print_nodes(nodes)
        #steps = traverse(directions, nodes)
        #print(f'\tIt took {steps} steps to traverse the map.')

        #
        # Part Two
        #
        steps = traverse_multiple(directions, nodes)
        print(f'\tIt took {steps} steps to traverse the map.')

        print()

if __name__ == '__main__':
    main()
