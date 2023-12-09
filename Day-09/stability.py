#!/usr/bin/env python
"""
Advent of Code 2023 - Day 9: Mirage Maintenance
Stephen Houser <stephenhouser@gmail.com>
"""

import argparse
from functools import reduce, partial

def load_file(filename: str):
    """Load lines from file into a list of ITEMS
        
       filename: the file to read descriptions from.
       return: list of lists of integers (sensor data)
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            integers = partial(lambda x: list(map(int, x.split())))
            return list(map(integers, file.readlines()))


    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def predict_forward(sequence):
    """Return sequence with backward prediction added"""
    if set(sequence) == {0}:
        return sequence + [0]

    # compute the differences of each element into a new list
    differences = map(lambda i: sequence[i]-sequence[i-1], range(1,len(sequence)))
    # Recurse to get the next predicted value
    extrapolated = predict_forward(list(differences))[-1]
    # Add next predicted value to the end of the sequence and return
    return sequence + [sequence[-1] + extrapolated]

def predict_backward(sequence):
    """Return sequence with backward prediction added"""
    if set(sequence) == {0}:
        return [0] + sequence

    # compute the differences of each element into a new list
    differences = map(lambda i: sequence[i]-sequence[i-1], range(1,len(sequence)))
    # Recurse to get the previous predicted value
    extrapolated = predict_backward(list(differences))[0]
    # Add previous predicted value to the start of the sequence and return
    return [sequence[0] - extrapolated] + sequence


def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        sensors = load_file(filename)
        print(f'\tThere are {len(sensors)} sensors')

        #
        # Part One
        #
        forward_sum = reduce(lambda a, c: a + predict_forward(c)[-1], sensors, 0)
        print(f'\tThe sum of forward predictions is {forward_sum}')

        #
        # Part Two
        #
        backward_sum = reduce(lambda a, c: a + predict_backward(c)[0], sensors, 0)
        print(f'\tThe sum of backward predictions is {backward_sum}')

        print()

if __name__ == '__main__':
    main()
