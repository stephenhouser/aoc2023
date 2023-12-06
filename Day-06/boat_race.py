#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
from functools import reduce

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

#
# The naive solution to map out all the times and see which ones are
# larger than the distance needed
def race_times(race):
    """Returns a list of (distance, hold times) to beat the 
        passed race (distance, current_winner)
    """
    (race_distance, race_time) = race
    winners = []

    for hold_time in range(race_time+1):
        speed = hold_time
        run_time = race_time - hold_time
        distance = speed * run_time
        if distance > race_distance:
            winners.append((distance, hold_time))

    return len(winners)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        races = load_file(filename)
        print(f'Races: {races}')

        #
        # Part One
        #
        winners_product = reduce(lambda a, c: c * a, map(race_times, races), 1)
        print(f'\tThe product of winning race combinations is: {winners_product}')

        # race_1 = races[0]
        # print(race_times(race_1[0], race_1[1]))
        #
        # Part Two
        #
        #n_chars = sum(map(len, map(Thing.get_line, things)))
        #print(f'\tTotal number of characters: {n_chars}')

        print()

if __name__ == '__main__':
    main()
