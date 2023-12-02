#!/usr/bin/env python
"""
Advent of Code 2023 - Day 1: Trebuchet?!
Stephen Houser <stephenhouser@gmail.com>
"""

import re
from functools import reduce


# Part 1
# Sum up the numbers from each line to get the calibration value.
# On each line, the calibration value can be found by combining the first
# digit and the last digit (in that order) to form a single two-digit number.
#
# Example:
#   1abc2       -> 12
#   pqr3stu8vwx -> 38
#   a1b2c3d4e5f -> 15
#   treb7uchet  -> 77
#
# Adding these together produces 142.
# Consider your entire calibration document.
# What is the sum of all of the calibration values?
def line_value1(line: str) -> int:
    """Return the line's calibration value.

       Combines the first digit and last digit (in order) to form a single 
       two-digit number.
    """
    number_re = '([1-9])'
    first_match = re.search('^.*?' + number_re + '.*$', line) # find first occurrence
    last_match  = re.search('^.*' + number_re + '.*?$', line) # find last occurrence

    first_digit = first_match.group(1)
    last_digit  = last_match.group(1)

    return int(first_digit + last_digit)

# Part 2
# Some of the digits are actually spelled out with letters:
#   one, two, three, four, five, six, seven, eight, and nine
# now count as valid "digits".
# Example:
#    two1nine           -> 29
#    eightwothree       -> 83
#    abcone2threexyz    -> 13
#    xtwone3four        -> 24
#    4nineeightseven2   -> 42
#    zoneight234        -> 14
#    7pqrstsixteen      -> 76
#
# Adding these together produces 281.
#
# NOTE: 2oneight -> 28 (not 21)
def number_str(number_name: str) -> str:
    """Return the numeric value for a number string
    
       Example: "1" -> "1", "one" -> "1", "two" -> 2, ...
    """
    number_names = ['zero', 'one', 'two', 'three', 'four',
                    'five', 'six', 'seven', 'eight', 'nine']

    if number_name in number_names:
        return str(number_names.index(number_name))

    return number_name

def line_value2(line: str) -> int:
    """Return the line's calibration value.

       Combines the first digit and last digit (in order) to form a single 
       two-digit number. Digits can also be the strings that represent the 
       digit, e.g. one = 1, two = 2, ...
    """
    number_re = '(one|two|three|four|five|six|seven|eight|nine|1|2|3|4|5|6|7|8|9)'
    first_match = re.search('^.*?' + number_re + '.*$', line) # find first occurrence
    last_match  = re.search('^.*' + number_re + '.*?$', line) # find last occurrence

    first_digit = number_str(first_match.group(1))
    last_digit  = number_str(last_match.group(1))

    return int(first_digit + last_digit)

#
# Initial version using a traditional for-loop
#
def read_calibration(filename, value_fn):
    """Read calibration file and return calibration value

       Use value_fn as function to compute calibration value for each line.
       Return the sum of all calibration values for all lines in the file.
    """
    calibration = 0
    try:
        with open(filename, 'r', encoding='utf-8') as cf:
            for line in cf.readlines():
                calibration += value_fn(line.strip())

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found!')

    return calibration

#
# Modified version that uses reduce()
#
def reduce_calibration(filename, value_fn):
    """Read calibration file and return calibration value

       Use value_fn as function to compute calibration value for each line.
       Return the sum of all calibration values for all lines in the file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as cf:
            # c = calibration value
            # l = line from file
            return reduce(lambda c,l: c + value_fn(l), cf.readlines(), 0)

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found!')

    return 0


p1 = read_calibration('test.txt', line_value1) # 142
print(f'Initial calibration value is {p1} (142)')
p2 = read_calibration('calibration.txt', line_value1) # 53386
print(f'Initial calibration value is {p2} (53386)')

p1 = reduce_calibration('test-2.txt', line_value2) # 281
print(f'Final calibration value is {p1} (281)')
p2 = reduce_calibration('calibration.txt', line_value2) # 53312
print(f'Final calibration value is {p2} (53312)')
