#!/usr/bin/env python
"""
Advent of Code 2023 - Day 12: Hot Springs
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
import logging as log
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)
import math
import itertools

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(count_records('test.txt'), 21)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        self.assertEqual(count_records('input.txt'), 6935)

    #
    # Part Two
    #
    # def test_part2_example(self):
    #     """Test example 1 data from test.txt"""
    #     self.assertEqual(count_records('test.txt', 5), 525152)

    # def test_part2_solution(self):
    #     """Test example 1 data from test.txt"""
    #     self.assertEqual(count_records('input.txt', 5), 3920437278260)

import collections
import functools

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        # if not isinstance(args, collections.Hashable):
        #     # uncacheable. a list, for instance.
        #     # better to not cache than blow up.
        #     return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


# obs = "..#."
# seq = (1, 2, 3)
@memoized
def matches_for(observations, sequence, tabs=0, show=False):
    if show: print('\t'*tabs, f'({observations}, {sequence})', end='')

    if len(sequence) == 0:
        no = observations.replace('.', '').replace('?', '')
        if len(no) == 0:
            # only dots and ? left
            if show: print('\nONLY DOTS and ?')
            return len(no) == 0
        return 0
        
    if len(observations) == 0:
        if show: print('\nOUT OF SEQUENCES')
        return 0

    if observations[0] == '.':
        if show: print()
        ans = matches_for(observations[1:], sequence, tabs)
        #print(f'{ans}: No observations or seqences left')
        return ans

    # this chunk matches current sequence needs
    if re.match('#[?#]{' + str(sequence[0]-1) + '}', observations):
        if show: print(f' Match on #')
        next = observations[sequence[0]:]
        if len(next):
            if next[0] == '#':
                return 0
            if next[0] == '?':
                next = '.' + next[1:]

        ans = matches_for(next, sequence[1:], tabs+1)
        if show: print('\t'*tabs, f'={ans}: match on #')
        return ans

    if observations[0] == '?':
        if show: print(' Encounter ?, recurse')
        ans =  matches_for('#'+observations[1:], sequence, tabs+1) + \
               matches_for('.'+observations[1:], sequence, tabs+1)
        if show: print('\t'*tabs, f'={ans}: recursion on choice')
        return ans


    return 0

def expand_records(records, expansion):
    """Unfold the records by the given expansion factor
    """
    return map(lambda r:
        ('?'.join(itertools.repeat(r[0], expansion)), r[1] * expansion),
        records
    )
    # nr = []
    # for (o, s) in records:
    #     nr.append(('?'.join(itertools.repeat(o, expansion)), s * expansion))

    # return nr

def count_records(filename, expansion=1):
    records = expand_records(load_file(filename), expansion)
    ans = 0
    for record in records:
        result = matches_for(record[0], tuple(record[1]))
        #print(f'{result:5}: {record}')
        ans += result

    return ans

def load_file(filename: str):
    """Load lines from file into ___
        
       filename: the file to read game descriptions from.
       returns: ...
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = []
            for line in file.readlines():
                (observations, sequence) = line.split()
                sequence = list(map(int, re.findall(r'\d+', line)))
                lines.append((observations, sequence))

    except FileNotFoundError:
        log.error('File %s not found.', filename)

    return lines

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        record_count = count_records(filename)
        print(record_count)
        print()

if __name__ == '__main__':
    main()
    #unittest.main()
