#!/usr/bin/env python
"""
Advent of Code 2023 - Day 17: Clumsy Crucible
Stephen Houser <stephenhouser@gmail.com>
"""

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
        city = load_file('test.txt')
        self.assertEqual(crucible_path(city, 1, 3), 102)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        city = load_file('input.txt')
        self.assertEqual(crucible_path(city, 1, 3), 843)

    #
    # Part Two
    #
    def test_part2_example1(self):
        """Test example 1 data from test.txt"""
        city = load_file('test.txt')
        self.assertEqual(crucible_path(city, 4, 10), 94)

    def test_part2_example2(self):
        """Test example 1 data from test.txt"""
        city = load_file('test-2.txt')
        self.assertEqual(crucible_path(city, 4, 10), 71)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        city = load_file('input.txt')
        self.assertEqual(crucible_path(city, 4, 10), 1017)


def load_file(filename: str):
    """Load lines from file into dictionary keyed by complex(x,y)"""
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
    _ = [print('--', end='') for x in cols] # header
    for y in rows:
        print(f'\n{y:2}:', end='')
        for x in cols:
            if path and complex(x, y) in path:
                print(' #', end='')
            else:
                print(f'{grid.get(complex(x, y)):2}', end='')

    print()

def c_str(cplx):
    """Pretty print a complex number as (i,j)"""
    return f'({int(cplx.real)}, {int(cplx.imag)})'

class ComplexPriQueue(PriorityQueue):
    """Priority Queue that wraps the items and uses explicit priority"""
    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: Any=field(compare=False)

    def get(self):
        """Return the priority and item contents"""
        inner = super().get()
        return inner.priority, inner.item[0], inner.item[1], inner.item[2]

    def put(self, cost, pos, direction, steps):
        """Add item with priority"""
        inner = ComplexPriQueue.PrioritizedItem(cost, (pos, direction, steps))
        super().put(inner)

    def show_queue(self):
        """Print the items in the queue -- This is broken"""
        d = self.queue
        for entry in d:
            item = entry.item
            print(f'{entry.priority}:{item[1]}, pos={c_str(item[2])}, dir={c_str(item[3])}')

def find_path(grid, start, goal, min_length, max_length):
    """Returns the cost of the path with the lowest cost through the grid.
        starts at start, ends at goal, will force to take steps that
        are at least min_length and at most max_length long
    """
    #
    # A seriously hacked Dijkstra algorithm.
    #
    # Lots of help from:
    #   https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #
    # Dijkstra (nor A*) does not handle the max segment length or min segment
    # length that the problem calls for. So, I store a bit more in the
    # `tentative` and `confirmed` lists than those algorithms would.
    #

    #print(f'start={c_str(start)}')
    #print(f'goal={c_str(goal)}')

    tenatative = ComplexPriQueue()  # nodes to consider
    confirmed = set()               # nodes we visited already

    # put our immediate neighbors on the tentative list, and the direction
    for direction in (complex(0,1), complex(1,0)):
        current = start + direction
        tenatative.put(grid.get(current), current, direction, 0)

    while not tenatative.empty():
        # Take lowest cost entry from tentative list
        cost, current, direction, steps = tenatative.get()

        # check if it's the goal
        if current == goal and steps >= (min_length - 1):
            return cost

        # check it's not already on confirmed list
        if (current, direction, steps) not in confirmed:
            # Add node to confirmed list
            confirmed.add((current, direction, steps))
            #print(f'Confirm {c_str(current)}->{c_str(direction)} cost={cost}')

            # Add neighbors to the tentative list

            # going straight as long as we don't run out of steps
            next_pos = current + direction
            if grid.get(next_pos) and (max_length - 1) > steps:
                next_cost = cost + grid.get(next_pos)
                tenatative.put(next_cost, next_pos, direction, steps+1)
                #print(f'\tadd: {c_str(current+direction)}->{c_str(direction)} cost={n_cost}')

            # going left and right if we have gone the minimum number of steps
            if steps >= (min_length - 1):
                for next_dir in (-1j/direction, 1j/direction):
                    next_pos  = current + next_dir
                    if grid.get(next_pos):
                        next_cost = cost + grid.get(next_pos)
                        tenatative.put(next_cost, next_pos, next_dir, 0)
                        #print(f'\tadd: {c_str(next_pos)}->{c_str(next_dir)} cost={next_cost}')

    # should not get here
    return -1

def crucible_path(city, min_length=1, max_length=3):
    rows = set([int(n.imag) for n in city])
    cols = set([int(n.real) for n in city])

    start = complex(0, 0)
    goal = complex(max(cols), max(rows))

    return find_path(city, start, goal, min_length, max_length)

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
        #print_grid(city)
        path_cost = crucible_path(city, 1, 3)
        print(f'\t1. The minimum heat loss (regular crucible): {path_cost}')

        #
        # Part Two
        #
        path_cost = crucible_path(city, 4, 10)
        print(f'\t2. The minimum heat loss (ultra crucible)  : {path_cost}')

        print()

if __name__ == '__main__':
    main()
    #unittest.main()
