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
  

def test_function(filename, *args):
    """Loads sample data and calculates answer...
    """
    stuff = load_file(filename)
    return len(stuff) * args[0]

@memoized
def expand_observations(hand, joker='?'):
    """Return list of all possible hands with joker substitution

       Example: 'AJQ12' -> ['A2Q12', 'A1Q12', 'AQQ12', 'AAQ12']
    """
    if joker not in hand:
        return [hand]

    replacements = ('.', '#')
    hands = []
    for card in hand:
        if card == joker:
            for replacement in replacements:
                hands.extend(expand_observations(hand.replace(joker, replacement, 1)))

    return set(hands)

def count_possible(record):
    (observations, sequence) = record

    seq_regex = make_regex(sequence)
    valid = []
    for possible in expand_observations(observations):
        #print(f'\tEval: {possible} {seq_regex} ', end='')
        if re.match(seq_regex, possible):
            #print(' match', end='')
            valid.append(possible)
        #print()

    return len(valid)

def count_records(filename):
    records = load_file(filename)

    ans = 0
    for record in records:
        print(f'{record}')
        fix1 = count_possible(record)
        print(f'{record} -> {fix1}\n')
        ans += fix1

    return ans

def make_regex(matches):
    regex = '\.*'
    for n in matches:
        regex += '#{' + n + '}\.+'

    return regex[:-1] + '*$'

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
                sequence = re.findall(r'\d+', line)     
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
