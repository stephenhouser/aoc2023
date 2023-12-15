#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from functools import reduce
from cProfile import Profile

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_sample(self):
        """Part 1: Test text in problem description"""
        self.assertEqual(hash_text('HASH'), 52)

    def test_part1_example(self):
        """Part 1: Test example data from test.txt"""
        sequence = load_file('test.txt')
        self.assertEqual(hash_summary(sequence), 1320)

    def test_part1_solution(self):
        """Part 1: Solution from input.txt"""
        sequence = load_file('input.txt')
        self.assertEqual(hash_summary(sequence), 495972)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Part 2: Test example data from test.txt"""
        sequence = load_file('test.txt')
        power = focus_power(initialize_mirrors(sequence))
        self.assertEqual(power, 145)

    def test_part2_solution(self):
        """Part 2: Solution from input.txt"""
        sequence = load_file('input.txt')
        power = focus_power(initialize_mirrors(sequence))
        self.assertEqual(power, 245223)


def load_file(filename: str):
    """Load lines from file into ___
        
       filename: the file to read game descriptions from.
       returns: ...
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip().split(',')

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def hash_text(text):
    """Return the HASH value for `text`
    """
    return reduce(lambda a, c: ((a+ord(c))*17)%256, text, 0)

def hash_summary(sequence):
    """Return the sum of the HASH algorithm across steps in sequence
    """
    return reduce(lambda a, c: a+hash_text(c), sequence, 0)


step_re = re.compile(r'([a-z]+)([-=])(\d*)')
def initialization_step(boxes, step):
    """Perform `step` in the initializtion sequence and update `boxes`
    """
    match = step_re.match(step)
    label = match.group(1)
    box_n = hash_text(label)

    if match.group(2) == '=':
        boxes[box_n][label] = int(match.group(3))
    elif label in boxes[box_n]:
        #assert match.group(2) == '-'
        del boxes[box_n][label]

def initialize_mirrors(sequence):
    """Return list of boxes from following initialization sequence"""
    boxes = [{} for _ in range(256)]

    for step in sequence:
        initialization_step(boxes, step)

    return boxes

def focus_power_single(box_index, lenses):
    """Return the focusing power of box with `box_index` and `lenses`"""
    summary = 0
    for slot, focal_length in enumerate(lenses.values()):
        summary += (box_index+1) * (slot+1) * focal_length

    return summary

def focus_power(boxes):
    """Returns the focusing power of the lens configuration.
        The sum of the focusing power of all boxes.
    """
    return reduce(lambda a, c: a+focus_power_single(c[0], c[1]),
                  enumerate(boxes),
                  0)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    example = hash_text('HASH')
    print(f'The example string "HASH" hashes to {example}')

    for filename in args.filename:
        print(filename)
        sequence = load_file(filename)

        with Profile() as profile:
            #
            # Part One
            #
            solution = hash_summary(sequence)
            print(f'\t1. The hash summary is: {solution}')

            #
            # Part Two
            #
            boxes = initialize_mirrors(sequence)
            power = focus_power(boxes)
            print(f'\t2. The focusing power of the configuration is: {power}')

            profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
