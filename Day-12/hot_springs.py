#!/usr/bin/env python
"""
Advent of Code 2023 - Day 12: Hot Springs
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from itertools import repeat
from functools import reduce

from performance import memoized

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
    def test_part2_example(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(count_records('test.txt', 5), 525152)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        self.assertEqual(count_records('input.txt', 5), 3920437278260)

#
# Cache results by memoizing the function
#
@memoized
def matches_for(observations, sequence):
    """Return the number of possible sequence matches for observations
    """
    #print(observations, sequence)

    # Base case: ran out of sequences to match
    if len(sequence) == 0:
        remaining = observations.replace('.', '').replace('?', '')
        return len(remaining) == 0  # Good sequence if observations ran out

    # Base case: ran out of observations to match, but still have sequences
    if len(observations) == 0:
        return 0

    # Recursive case: the next chararcter is ., skip it
    if observations[0] == '.':
        return matches_for(observations[1:], sequence)

    # Recursive case: the next character is #, there *must* be a sequence here
    if re.match('#[?#]{' + str(sequence[0]-1) + '}', observations):
        remaining = observations[sequence[0]:]  # keep what's left

        # this path fails if '#' is next
        if len(remaining) and remaining[0] == '#':
            return 0

        # if next is ? make . to be a valid as we just ended a sequence
        if len(remaining) and remaining[0] == '?':
            remaining = '.' + remaining[1:]

        # find out if the rest matches as well...
        return matches_for(remaining, sequence[1:])

    # Recursive case: the next character wildcard, track down both options
    if observations[0] == '?':
        return matches_for('#'+observations[1:], sequence) + \
               matches_for('.'+observations[1:], sequence)

    return 0

def expand_records(records, expansion):
    """Unfold each record in the list by the given expansion factor.
    """
    expanded = []
    for record in records:
        (obs, seq) = record
        exp_obs = '?'.join(repeat(obs, expansion))
        exp_seq = tuple(seq * expansion)
        expanded.append((exp_obs, exp_seq))

    return expanded

def count_matches(record):
    """Return the number of possible sequences that are possible
       from the given record = (observations, sequences)
    """
    (observations, sequences) = record
    return matches_for(observations, sequences)

#@perf_timer
def count_records(filename, expansion=1):
    """Return the count of possible"""
    records = expand_records(load_file(filename), expansion)
    return reduce(lambda a, c: a + count_matches(c), records, 0)

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
        print(f'File {filename} not found.')

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
    #main()
    unittest.main()
