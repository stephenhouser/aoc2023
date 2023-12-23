#!/usr/bin/env python
"""
Advent of Code 2023 - Day 22: Sand Slabs
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
from multiprocessing import Pool
from functools import partial
from copy import deepcopy


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

class SandWorld:
    def __init__(self, file):
        self.load_slabs(file)

    def load_slabs(self, file):
        # put slabs in sorted order, lowest first
        self.slabs = sorted(
            map(SandSlab, file.readlines()),
            key = lambda s: s.p1[2])
        self.x = max(map(lambda s: s.p2[0], self.slabs))
        self.y = max(map(lambda s: s.p2[1], self.slabs))
        self.z = max(map(lambda s: s.p2[2], self.slabs))
        self.floor = SandSlab(f'0,0,0~{self.x},{self.y},0')

class SandSlab:
    slab_letter = 1

    """Represents a ___"""
    def __init__(self, text):
        self.name = str(SandSlab.slab_letter)
        SandSlab.slab_letter += 1

        self.p1 = None
        self.p2 = None
        self._parse_line(text)
        self.supported_by = set()
        self.supports = set()

    def is_disintegratable(self):
        """If the slabs we support have other supporters"""
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
        """Parse text description of ___"""
        match = re.match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', text)
        self.p1 = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        self.p2 = (int(match.group(4)), int(match.group(5)), int(match.group(6)))

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
        else:
            return f'{self.name} ({self.p1}, {self.p2})'

def cast_down(world, x, y, z):
    """what is the next block down from x, y, z"""
    lower_slabs = reversed(list(filter(lambda s: s.p2[2] < z, world.slabs)))
    for slab in lower_slabs:
        if slab.p1[0] <= x <= slab.p2[0] and slab.p1[1] <= y <= slab.p2[1]:
            return slab

    return world.floor

def drop_slabs(world):
    """Drop slabs into place"""

    # start at lowest level and work our way up
    for slab in world.slabs:
        cast_z = [] # slabs below us
        for y in range(slab.p1[1], slab.p2[1]+1):
            for x in range(slab.p1[0], slab.p2[0]+1):
                cast_z.append(cast_down(world, x, y, slab.p1[2]))

        # the z level just below where we can drop to
        top_z = max(map(lambda s: s.p2[2], cast_z))
        slab.supported_by = set(filter(lambda s: s.p2[2]==top_z, cast_z))
        for s in slab.supported_by:
            s.supports.add(slab)

        drop_z = slab.p1[2] - (top_z + 1) # distance fell
        slab.p1 = (slab.p1[0], slab.p1[1], slab.p1[2]-drop_z)
        slab.p2 = (slab.p2[0], slab.p2[1], slab.p2[2]-drop_z)

def cast_down_2(slabs, x, y, z):
    """what is the next block down from x, y, z"""
    lower_slabs = reversed(list(filter(lambda s: s.p2[2] < z, slabs)))
    for slab in lower_slabs:
        if slab.p1[0] <= x <= slab.p2[0] and slab.p1[1] <= y <= slab.p2[1]:
            return slab.p2[2]+1

    return 1

def drop_slabs_2(slabs, skip=None):
    """Drop slabs into place"""

    if skip != None:
        slabs = deepcopy(slabs)
        print('skip', skip, len(slabs))
        slabs.pop(skip)

    # start at lowest level and work our way up
    slabs_fell = 0
    for slab in slabs:
        cast_z = [] # slabs below us
        for y in range(slab.p1[1], slab.p2[1]+1):
            for x in range(slab.p1[0], slab.p2[0]+1):
                cast_z.append(cast_down_2(slabs, x, y, slab.p1[2]))

        # the z level just below where we can drop to
        drop_z = slab.p1[2] - max(cast_z) # distance fell
        if drop_z:
            slab.p1 = (slab.p1[0], slab.p1[1], slab.p1[2]-drop_z)
            slab.p2 = (slab.p2[0], slab.p2[1], slab.p2[2]-drop_z)
            slabs_fell += 1

    return slabs_fell

def print_slabs(world):
    print(world.x, world.y, world.z)
    for level in range(world.z, -1, -1):
        print(f'Level: {level}')
        print_level(world, level)
        print()

def print_level(world, level):
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

def print_supports(world):
    print('digraph {')
    for slab in world.slabs:
        names = ','.join(map(lambda s: s.name, slab.supports))
        print(slab.name + ' -> {' + str(names) + '}')
        # print(f'{slab.name} supported by ')
        # for support in slab.supported_by:
        #     print('\t', support)

        # print('\tsupports ')
        # for support in slab.supports:
        #     print('\t', support)
    print('}')

def find_extra(world):
    extra = set()
    for slab in world.slabs:
        print(slab, end='')
        if slab.is_disintegratable():
            print('CAN REMOVE')
            extra.add(slab)

    return extra

def load_file(filename: str):
    """Load lines from file into ___"""
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
        # print(filename)

        with Profile() as profile:
            world = load_file(filename)

            #
            # Part One
            #
            # n_things = len(world.slabs)
            # print(f'\t1. Number of things: {n_things:,}')
            # print_slabs(world)

            # drop_slabs(world)
            drop_slabs_2(world.slabs)

            print_slabs(world)
            for s in world.slabs:
                print(s.name, (s.p1[0],s.p1[1],s.p1[2],s.p2[0],s.p2[1],s.p2[2]))
            # su = []
            # for s in world.slabs:
            #     su.append((s.p1[0],s.p1[1],s.p1[2],s.p2[0],s.p2[1],s.p2[2]))
            # print(su)
            # print_slabs(world)
            # print_supports(world)

            # extra = find_extra(world)
            # print(extra)
            # print(len(extra))
            #
            # Part Two
            #
            # n_things = len(things)
            # print(f'\t2. umber of things: {n_things:,}')


            faller = partial(drop_slabs_2, world.slabs)

            # fallen = list(map(faller, range(len(world.slabs))))
            # print(drop_slabs_2(world.slabs.copy(), 0))
            # print(drop_slabs_2(world.slabs.copy(), 1))

            with Pool(processes=24) as pool:
                fallen = list(pool.map(faller, range(len(world.slabs))))

            # fallen = []
            # for s, slab in enumerate(world.slabs):
            #     slabber = world.slabs.copy()
            #     slabber.pop(s)
            #     # slabber = world.slabs[s:] + world.slabs[:s+1]
            #     falls = drop_slabs_2(slabber)
            #     print(f'remove {s} {slab.name} for {falls}')
            #     fallen.append(falls)

            print(fallen[19])
            print(sum(fallen))

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()

# 465 too high
# answer 395

# 48138