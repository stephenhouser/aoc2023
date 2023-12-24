#!/usr/bin/env python
"""
Advent of Code 2023 - Day 22: Sand Slabs
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Part 1 solution for test.txt"""
        world = drop_slabs(load_file('test.txt'))
        disintegratable_slabs = len(find_disintigratable(world))
        self.assertEqual(disintegratable_slabs, 5)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        world = drop_slabs(load_file('input.txt'))
        disintegratable_slabs = len(find_disintigratable(world))
        self.assertEqual(disintegratable_slabs, 395)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Part 2 solution for test.txt"""
        world = drop_slabs(load_file('test.txt'))
        fallen_slabs = sum(map(count_supported, world.slabs))
        self.assertEqual(fallen_slabs, 7)

    def test_part2_solution(self):
        """Part 2 solution for input.txt"""
        world = drop_slabs(load_file('input.txt'))
        fallen_slabs = sum(map(count_supported, world.slabs))
        self.assertEqual(fallen_slabs, 64_714)


class SandWorld:
    """Represents the 3D world of Sand Slabs"""

    def __init__(self, file):
        self.load_slabs(file)

    def load_slabs(self, file):
        """Load Sand Slabs from file iterator"""
        # put slabs in sorted order, lowest first
        self.slabs = sorted(
            map(SandSlab, file.readlines()),
            key = lambda s: s.p1[2])
        self.x = max(map(lambda s: s.p2[0], self.slabs))
        self.y = max(map(lambda s: s.p2[1], self.slabs))
        self.z = max(map(lambda s: s.p2[2], self.slabs))
        self.floor = SandSlab(f'0,0,0~{self.x},{self.y},0')

class SandSlab:
    """Represents Sand Slabs"""

    slab_letter = 1 # for giving a unique name to every Sand Slab

    def __init__(self, text):
        self.name = str(SandSlab.slab_letter)
        SandSlab.slab_letter += 1

        self.p1 = None
        self.p2 = None
        self._parse_line(text)
        self.supported_by = set()
        self.supports = set()

    def is_disintegratable(self):
        """Returns True if this slab can be disintegrated with no effects.
            e.g. if the above slabs have other supporters
        """

        if len(self.supports) == 0:
            #print(f'{self.name}: does not support anything')
            return True

        # for each thing I support, are there other supporters
        for support in self.supports:
            if len(support.supported_by) == 1 and list(support.supported_by)[0] == self:
                #print(f'{self.name}: {support.name} still supported by {others}')
                return False

        #print(f'{self.name}: supports {self.supports} which have no other supporters')
        return True

    def _parse_line(self, text):
        """Parse text description of a SandSlab"""
        match = re.match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', text)
        self.p1 = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        self.p2 = (int(match.group(4)), int(match.group(5)), int(match.group(6)))

        # assert the points are in the oritentation I expect
        assert self.p1[0] <= self.p2[0]
        assert self.p1[1] <= self.p2[1]
        assert self.p1[2] <= self.p2[2]

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        if self.p1[2] == 0:
            return 'Floor'

        return f'{self.name} ({self.p1}, {self.p2})'

def cast_down(world, x, y, z):
    """what is the next slab down from x, y, z along the z axis"""
    lower_slabs = reversed(list(filter(lambda s: s.p2[2] < z, world.slabs)))
    for slab in lower_slabs:
        if slab.p1[0] <= x <= slab.p2[0] and slab.p1[1] <= y <= slab.p2[1]:
            return slab

    return world.floor

def drop_slabs(world):
    """Drop slabs into place, collapsing any empty spaces"""

    # start at lowest level and work our way up
    for slab in world.slabs:
        peaks = [] # slabs below us
        for y in range(slab.p1[1], slab.p2[1]+1):
            for x in range(slab.p1[0], slab.p2[0]+1):
                # look down from this Z, what slab is below me?
                peaks.append(cast_down(world, x, y, slab.p1[2]))

        # the highest z level just below where we can drop to
        highest_peak = max(map(lambda s: s.p2[2], peaks))

        # save what supports us and who they support
        slab.supported_by = set(filter(lambda s: s.p2[2]==highest_peak, peaks))
        for s in slab.supported_by:
            s.supports.add(slab)

        fall_down_z = slab.p1[2] - (highest_peak + 1) # distance to fall
        slab.p1 = (slab.p1[0], slab.p1[1], slab.p1[2]-fall_down_z)
        slab.p2 = (slab.p2[0], slab.p2[1], slab.p2[2]-fall_down_z)

    return world

def find_disintigratable(world):
    """Return list of expendable Sand Slabs
        Ones that can be remove and the tower won't change
    """
    disintigratable = set()
    for slab in world.slabs:
        if slab.is_disintegratable():
            disintigratable.add(slab)

    return disintigratable

def count_supported(slab):
    """Return a list of how many tiles are supported by the given tile."""
    dropped = set()

    if not slab.is_disintegratable():   # only if we support things
        todo = set(slab.supports)       # who we supoort

        while todo:
            s = todo.pop()
            if len(s.supported_by - ({slab} |dropped)) == 0:
                dropped.add(s)
                todo |= s.supports

    return len(dropped)

def print_slabs(world):
    """Pretty print the slab world"""
    print(world.x, world.y, world.z)
    for level in range(world.z, -1, -1):
        print(f'Level: {level}')
        print_level(world, level)
        print()

def print_level(world, level):
    """Pretty print one level of the slab world"""
    level_row = ['.' for x in range(world.x+1)]
    level_map = [level_row[:] for y in range(world.y+1)]

    for slab in world.slabs:
        if slab.p1[2] <= level <= slab.p2[2]:
            for y in range(slab.p1[1], slab.p2[1]+1):
                for x in range(slab.p1[0], slab.p2[0]+1):
                    level_map[y][x] = slab.name

    for y in range(world.y+1):
        for x in range(world.x+1):
            print(level_map[y][x], end='')
        print()

def print_support_dot(world):
    """Print a .dot format for GraphViz"""
    print('digraph {')
    for slab in world.slabs:
        names = ','.join(map(lambda s: s.name, slab.supports))
        print(slab.name + ' -> {' + str(names) + '}')
    print('}')

def load_file(filename: str):
    """Load lines from file into SandSlabs in a SandWorld"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return SandWorld(file)

    except FileNotFoundError:
        print('File %s not found.', filename)

    return None

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            world = load_file(filename)
            drop_slabs(world)

            #
            # Part One
            #
            disintegratable_slabs = len(find_disintigratable(world))
            print(f'\t1. Disentegratable sand slabs: {disintegratable_slabs:,}')

            #
            # Part Two
            #
            fallen_slabs = sum(map(count_supported, world.slabs))
            print(f'\t2. Sum of fallen san slabs: {fallen_slabs:,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
