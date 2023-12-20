#!/usr/bin/env python
"""
Advent of Code 2023 - Day 19: Aplenty
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
from functools import reduce, partial

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Test example 1 data from test.txt"""
        workflows, parts = load_file('test.txt')
        self.assertEqual(rating_sum(workflows, parts), 19114)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        workflows, parts = load_file('input.txt')
        self.assertEqual(rating_sum(workflows, parts), 331208)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Test example 1 data from test.txt"""
        workflows, _ = load_file('test.txt')
        self.assertEqual(accepted_combinations(workflows), 167_409_079_868_000)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        workflows, _ = load_file('input.txt')
        self.assertEqual(accepted_combinations(workflows), 121_464_316_215_623)


class Rule:
    """Class to represent rules in the sorting of parts on Gear Island"""

    def __init__(self, destination, variable, condition, value):
        self.destination = destination  # Accept, Reject, or next workflow
        self.variable = variable        # 'x', 'm', 'a', or 's'
        self.condition = condition      # '>' or '<'
        self.value = value              # value to compare against

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.variable:
            return f'Rule:{self.variable}{self.condition}{self.value}:{self.destination}'

        return f'Rule:{self.destination}'

    # returns the name of the next rule to execute, including A, R
    def execute(self, part):
        """Returns the next workflow if rule matched, or None if it did not."""
        if self.condition and self.condition == '>':
            if part[self.variable] > self.value:
                return self.destination

            return None

        if self.condition and self.condition == '<':
            if part[self.variable] < self.value:
                return self.destination

            return None

        return self.destination

workflow_re = re.compile(r'([a-z]+){(.*)}')
condition_re = re.compile(r'([asmx])([><])(\d+):([a-zAR]+)')
def parse_workflow(text):
    """Return a parsed "workflow" which is a list of Rules"""
    match = workflow_re.match(text)
    workflow_name = match.group(1)

    rules = []
    conditions = match.group(2).split(',')
    for condition in conditions:
        cond_match = condition_re.match(condition)
        if cond_match:
            variable = cond_match.group(1)
            comparison = cond_match.group(2)
            value = int(cond_match.group(3))
            destination = cond_match.group(4)
            rules.append(Rule(destination, variable, comparison, value))
        else:
            rules.append(Rule(condition, None, None, None))

    return (workflow_name, rules)

part_re = re.compile(r'([asmx])=(\d+)')
def parse_part(text):
    """Return a "part" parsed from text"""
    return {x : int(y) for x, y in part_re.findall(text)}

def load_file(filename: str):
    """Load lines from file into workflows(rules) and parts"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            (workflow_text, instructions_text) = file.read().split('\n\n')
            # don't have to use comprehension here, R1721
            #workflows = {x: y for x, y in map(parse_workflow, workflow_text.split('\n'))}
            workflows = dict(map(parse_workflow, workflow_text.split('\n')))
            parts = map(parse_part, instructions_text.split('\n'))
            return (workflows, list(parts))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

# Part One
def process_part(workflows, part):
    """Return the "rating number" of the part for accepted parts.
        Returns 0 for rejected parts.
    """
    destination = 'in'
    while destination not in ('A', 'R'):
        workflow = workflows[destination]
        for rule in workflow:
            if result := rule.execute(part):
                destination = result
                break

    if destination == 'A':
        # rating number is sum of part values
        return sum(part.values())

    return 0

def rating_sum(workflows, parts):
    """Return the rating sum for all parts in through the workflows"""
    return sum(map(partial(process_part, workflows), parts))

# Part Two
def get_accepted(workflows, start_workflow):
    """Returns list of accepted ranges of values for x, m, a, and s"""

    xmas = {'x':0, 'm':1, 'a':2, 's':3} # for indexing into the ranges
    start_range = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]

    rejected = []   # rejected ranges (don't really need to track these)
    accepted = []   # accepted ranges (this is what we want)

    open_l = [(workflows[start_workflow], start_range)] # rules to process

    while open_l:
        workflow, ranges = open_l.pop()     # remove item from open list

        for rule in workflow:               # run it's rules
            if rule.condition:
                v_idx = xmas[rule.variable] # index of variable into counts
                split_ranges = ranges[:]    # copy so we can modify

                if rule.condition == '<':
                    split_ranges[v_idx] = (split_ranges[v_idx][0], rule.value-1)
                    ranges[v_idx] = (rule.value, ranges[v_idx][1])

                if rule.condition == '>':
                    split_ranges[v_idx] = (rule.value+1, split_ranges[v_idx][1])
                    ranges[v_idx] = (ranges[v_idx][0], rule.value)

            if rule.destination == 'A':
                accepted.append(split_ranges if rule.condition else ranges)
            elif rule.destination == 'R':
                rejected.append(split_ranges if rule.condition else ranges)
            else:
                next_flow = workflows[rule.destination]
                open_l.append((next_flow, split_ranges if rule.condition else ranges))

    return accepted

def accepted_combinations(workflows):
    """Return the sum of the products of the accepted range combinations"""
    def product(a, c):
        """Product for reduce"""
        return a * (c[1]-c[0]+1)

    accepted = get_accepted(workflows, 'in')
    return sum(reduce(product, xmas, 1) for xmas in accepted)


def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            (workflows, parts) = load_file(filename)
            #print('workflows:', workflows)
            #print('Parts:', parts)

            #
            # Part One
            #
            overall_rating = rating_sum(workflows, parts)
            print(f'\t1. Sum of all accepted ratings: {overall_rating}')

            #
            # Part Two
            #
            accepted_parts = accepted_combinations(workflows)
            print(f'\t2. Accepted combinations: {accepted_parts}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
