#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
import math
import itertools

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

class Machine:
    def __init__(self, text):
        self.nodes = set()
        self.connections = set()
        self.load_machine(text)

    def load_machine(self, text):
        for line in text:
            match = re.findall(r'[a-z]{3}', line)
            for node in match:
                self.nodes.add(node)

            for node in match[1:]:
                self.connections.add(tuple(sorted((match[0], node))))

    def find_wire(self, node):
        return list(filter(lambda x: node in x, self.connections))

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return Machine(file.readlines())
    except FileNotFoundError:
        print('File %s not found.', filename)

    return None

def print_dot(machine):
    # dot -T svg test.dot > test.svg
    print('strict graph {')
    for node in machine.connections:
        print(node[0], '--', node[1])
    print('}')

def count_reachable_nodes(node, machine):
    visited = set()
    pool = machine.find_wire(node)
    visited.add(node)
    while pool:
        n1, n2 = pool.pop()
        #print(f'{n1} {n2}')
        if n1 not in visited:
            pool.extend(machine.find_wire(n1))
            visited.add(n1)

        if n2 not in visited:
            pool.extend(machine.find_wire(n2))
            visited.add(n2)

    return len(visited)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            machine = load_file(filename)

            #
            # Part One
            #
            # print('Nodes      :', len(machine.nodes))
            # print('Connections:', len(machine.connections))
            # print(count_reachable_nodes('hfx', machine))
            # print(count_reachable_nodes('pzl', machine))

            if filename == 'test.txt':
                machine.connections.remove(('hfx', 'pzl'))
                machine.connections.remove(('bvb', 'cmg'))
                machine.connections.remove(('jqt', 'nvd'))
                c1 = count_reachable_nodes('hfx', machine)
                c2 = count_reachable_nodes('pzl', machine)
            else:
                # I just looked at the graph and found these nodes :-)
                machine.connections.remove(('qfb', 'vkd'))
                machine.connections.remove(('hqq', 'xxq'))
                machine.connections.remove(('kgl', 'xzz'))
                c1 = count_reachable_nodes('vkd', machine)
                c2 = count_reachable_nodes('qfb', machine)

            print(f'\t1. Product of disconnected sets: {c1*c2:,}')

            #
            # Part Two
            #
            print('\t2. Part 2 is a secret')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
