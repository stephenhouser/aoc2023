#!/usr/bin/env python
"""
Advent of Code 2023 - Day 6: Wait For It
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
from functools import reduce
import multiprocessing

def load_file(filename: str):
    """Load lines from file into a list of ITEMS
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    times = []
    distances = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            times = list(map(int, re.findall(r'(\d+)', next(file))))
            distances = list(map(int, re.findall(r'(\d+)', next(file))))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return list(zip(distances, times))

def load_race_2(filename: str):
    """Load lines from file into a list of ITEMS
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    times = []
    distances = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            times = list(map(int, re.findall(r'(\d+)', next(file).replace(' ', ''))))
            distances = list(map(int, re.findall(r'(\d+)', next(file).replace(' ', ''))))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return list(zip(distances, times))

#
# The naive solution to map out all the times and see which ones are
# larger than the distance needed
def race_times_o1(race):
    """Returns a list of (distance, hold times) to beat the 
        passed race (distance, current_winner)
    """
    # First order function version
    (race_distance, race_time) = race
    winners = []

    for hold_time in range(race_time+1):
        speed = hold_time
        run_time = race_time - hold_time
        distance = speed * run_time
        if distance > race_distance:
            winners.append((distance, hold_time))

    return len(winners)

def race_times(race):
    """Returns a list of (distance, hold times) to beat the 
        passed race (distance, current_winner)
    """
    # Higher Order function version
    distances = map(lambda h: h*(race[1]-h), range(race[1]+1))
    winners = filter(lambda x: x > race[0], distances)
    return len(list(winners))

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        #
        # Part One
        #
        races = load_file(filename)
        print(f'1. Races: {races}')
        winners_product = reduce(lambda a, c: c * a, map(race_times, races), 1)
        print(f'\t1. The product of winning race combinations is: {winners_product}')

        #
        # Part Two
        # I thought there would need to be a better solution to this,
        # a maximization function (calculus)...
        races = load_race_2(filename)
        print(f'2. Races: {races}')

        with multiprocessing.Pool(processes=4) as pool:
            #winners_product = reduce(lambda a, c: c * a, pool.map(race_times, races), 1)
            winners_product = reduce(lambda a, c: c * a, pool.map(race_times, races), 1)

        print(f'\t2. The product of winning race combinations is: {winners_product}')

        print()

if __name__ == '__main__':
    main()
