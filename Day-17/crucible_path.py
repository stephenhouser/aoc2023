#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('test.txt', 2), 0)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        self.assertEqual(test_function('input.txt', 200), 0)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('test.txt', 10), 0)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(test_function('input.txt', 1000000), 0)


def test_function(filename, *args):
    """Loads sample data and calculates answer...
    """
    stuff = load_file(filename)
    return len(stuff) * args[0]

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # returns a dictionary indexed by i,j with c as the value
            return {complex(x,y): int(c) for y, r in enumerate(file)
                                         for x, c in enumerate(r.strip())}
    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def print_grid(grid, path=None):
    """Pretty print 2D grid in readable form"""
    rows = set([int(n.imag) for n in grid])
    cols = set([int(n.real) for n in grid])

    print('  :', end='')
    _ = [print(f'{x:2}', end='') for x in cols] # header
    print('\n  :', end='')
    _ = [print(f'--', end='') for x in cols] # header
    for y in rows:
        print(f'\n{y:2}:', end='')
        for x in cols:
            if path and complex(x, y) in path:
                print(f' #', end='')
            else:
                print(f'{grid.get(complex(x, y)):2}', end='')

    print()

def c_str(cplx):
    return f'({int(cplx.real)}, {int(cplx.imag)})'


class ComplexPriQueue(PriorityQueue):
    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: Any=field(compare=False)

    def get(self):
        inner = super().get()
        return inner.item, inner.priority

    def put(self, item, priority):
        inner = ComplexPriQueue.PrioritizedItem(priority, item)
        super().put(inner)

    def show_queue(self):
        d = self.queue
        for entry in d:
            item = entry.item
            print(f'{entry.priority}:{item[1]}, pos={c_str(item[2])}, dir={c_str(item[3])}')


def get_neighbors(grid, current, neighbor_count=3):
    neighbors = []
    for n in range(1, neighbor_count+1):
        for direction in (-1, 1, -1j, 1j):
            neighbor = current + (direction * n)
            if grid.get(neighbor):
                neighbors.append(neighbor)

    return neighbors

def find_path_dj(grid):
    rows = set([int(n.imag) for n in grid])
    cols = set([int(n.real) for n in grid])

    start = complex(0, 0)
    goal = complex(max(cols), max(rows))

    print(f'start={c_str(start)}')
    print(f'goal={c_str(goal)}')

    open_l = ComplexPriQueue()  # nodes to consider

    # closed list and reached is set of keys
    parents = dict()
    costs = dict()

    open_l.put(complex(0, 0), 0)
    parents[start] = None
    costs[start] = 0

    visited = set()

    while not open_l.empty():
        current, direction = open_l.get()

        print(f'Eval: {c_str(current)} cost={costs[current]}')

        if current == goal:
            break

        if (current, direction) in visited:
            continue

        visited.add((current, direction))

        for neighbor in get_neighbors(grid, current):
            neighbor_cost = costs[current] + grid.get(neighbor)
            if neighbor not in costs or neighbor_cost < costs[neighbor]:
                print(f'\tAdd: {c_str(neighbor)} @{grid.get(neighbor)} = {neighbor_cost}')
                costs[neighbor] = neighbor_cost
                open_l.put(neighbor, neighbor_cost)
                parents[neighbor] = current
            else:
                print(f'\tSki: {c_str(neighbor)}={neighbor_cost}')

    # print the path
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()

    print_grid(grid, path)



def find_path(grid):
    rows = set([int(n.imag) for n in grid])
    cols = set([int(n.real) for n in grid])

    start = complex(0, 0)
    goal = complex(max(cols), max(rows))

    print(f'start={c_str(start)}')
    print(f'goal={c_str(goal)}')

    search_counter = 0
    open_l = ComplexPriQueue()  # nodes to consider
    open_l.put((0, search_counter, complex(0, 0), complex(1, 0)))
    open_l.put((0, search_counter, complex(0, 0), complex(0, 1)))

    closed_l = set()            # visited nodes

    while not open_l.empty():
        cost, _, pos, dir = open_l.get()

        if pos == goal:
            return cost
        
        if (pos, dir) in closed_l:
            continue

        left = complex(0, 1) / dir
        right = -complex(0, 1) / dir
        for cast in (left, right):
            for length in range(1, 3):  # look out 1 to 3 steps
                check_pos = pos + (dir * length)
                if grid.get(check_pos): # is it on the map?
                                        # cost is sum of all costs along the way                    
                    check_cost = cost + sum()


    open_l.show_queue()
    return 0


def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        city = load_file(filename)

        #
        # Part One
        #
        print_grid(city)
        ans = find_path_dj(city)

        #
        # Part Two
        #

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
