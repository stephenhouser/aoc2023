#!/usr/bin/env python
"""
Advent of Code 2023 - Day X: ...
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from functools import reduce

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

def e_hash(item):
    return reduce(lambda a, c: ((a+ord(c))*17)%256, item, 0)
    # ans = 0
    # for i in item:
    #     ans = ((ans +ord(i)) * 17) % 256

    # return ans

label_re = re.compile('[a-z]+')
def label_hash(item):
    label = label_re.findall(item)[0]
    return reduce(lambda a, c: ((a+ord(c))*17)%256, label, 0)

step_re = re.compile(r'([a-z]+)([-=])(\d*)')
def parse_step(step):
    match = step_re.match(step)
    if match.group(2) == '=':
        return (match.group(1), match.group(3))

    return (match.group(1), None)


def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        sequence = load_file(filename)

        #
        # Part One
        #
        n_things = len(sequence)
        #print(f'\tNumber of things: {sequence}')

        e_hash('HASH')
        ans = reduce(lambda a, c: a+e_hash(c), sequence, 0)
        print(ans)
        #
        # Part Two
        #
        boxes = [{} for _ in range(256)]
        for step in sequence:
            label, op = parse_step(step)
            box = e_hash(label)
            #print(step, ' --> ', label, op, e_hash(label))

            if op:
                boxes[box][label] = int(op)
            elif label in boxes[box]: # -
                del boxes[box][label]

            #print(boxes[:5])    

        ans = 0
        for box, cont in enumerate(boxes):
            if cont:
                sub = 0
                for s, l in enumerate(cont.values()):
                    sub += (1 + box) * (s+1) * l
                    print(f'\t (1+{box}) * {s+1} * {l} = {sub}')

                ans += sub

        print(ans)

if __name__ == '__main__':
    main()
    #unittest.main()
