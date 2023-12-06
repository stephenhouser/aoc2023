#!/usr/bin/env python
"""
Advent of Code 2023 - Day 6: Wait For It
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import time
import math
from functools import reduce, wraps
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



def timer(func):
    """Wrap function and report on timing"""
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        time_start = time.perf_counter()
        value = func(*args, **kwargs)

        time_end = time.perf_counter()
        elapsed_time = time_end - time_start
        print(f"timer -> {elapsed_time:.4f}s")
        return value

    return wrapper_timer

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

#@timer
def race_times_brute(race):
    """Returns a list of (distance, hold times) to beat the 
        passed race (distance, current_winner)
    """
    # Higher Order function version
    distances = map(lambda h: h*(race[1]-h), range(race[1]+1))
    winners = list(filter(lambda x: x > race[0], distances))
    #print(f'brute {len(winners)}')
    return len(winners)

#@timer
def race_times_quadratic(race):
    """Return the number of "hold times" that would allow the boat to
       get to distance in the alloted race_time (the previous winning time).

       Solve the quadratic and return the number of integers above the x axis
            distance = hold_time * (race_time - hold_time)
        Rewrite:
            distance = hold_time*race*time - hold_time^2
            hold_time^2 + distance = hold_time*race_time
            hold_time^2 - race_time*hold_time + distance  = 0
            ax^2        - bx                   + c        = 0

            a = 1, b = race_time, c = distance, x = hold_time
    """
    (distance, race_time) = race
    d1 = (race_time-math.sqrt(race_time**2 - 4*distance))/2.0
    d2 = (race_time+math.sqrt(race_time**2 - 4*distance))/2.0
    nums = round(d2-d1-1) if d2 == int(d2) else round(d2-d1)
    #print(f'math d1={d1:.2f}, d2={d2:.2f} a={nums}')
    return nums

def race_times_disc(race):
    """descriminant of a quadratic trinomial"""
    (distance, race_time) = race
    ans = math.sqrt(race_time**2 - 4 * distance)
    #print(f'disc a={round(ans)}')
    return round(ans)

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

        winners_product = reduce(lambda a, c: c * a, map(race_times_brute, races), 1)
        print(f'\t1. (brute) The product of winning race combinations is: {winners_product}')

        winners_product = reduce(lambda a, c: c * a, map(race_times_quadratic, races), 1)
        print(f'\t1. (quad)  The product of winning race combinations is: {winners_product}')

        winners_product = reduce(lambda a, c: c * a, map(race_times_disc, races), 1)
        print(f'\t1. (disc)  The product of winning race combinations is: {winners_product}')
        #
        # Part Two
        #
        races = load_race_2(filename)
        print(f'2. Races: {races}')

        with multiprocessing.Pool(processes=4) as pool:
            winners_product = reduce(lambda a, c: c * a, pool.map(race_times_brute, races), 1)
            print(f'\t2. (brute) The product of winning race combinations is: {winners_product}')

        winners_product = reduce(lambda a, c: c * a, map(race_times_quadratic, races), 1)
        print(f'\t2. (quad)  The product of winning race combinations is: {winners_product}*')

        winners_product = reduce(lambda a, c: c * a, map(race_times_disc, races), 1)
        print(f'\t2. (disc)  The product of winning race combinations is: {winners_product}*')
        print()

if __name__ == '__main__':
    main()
