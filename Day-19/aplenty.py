#!/usr/bin/env python
"""
Advent of Code 2023 - Day 19: Aplenty
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile


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

class Thing:
    """Represents a ___"""
    def __init__(self, text):
        self._parse_line(text)

    def _parse_line(self, text):
        """Parse text description of ___"""
        match = re.match(r'\d+', text)

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'Empty'


class Rule:
    FORWARD = 'F'
    REJECT  = 'R'
    ACCEPT  = 'A'

    def __init__(self, destination, variable, condition, value):
        self.destination = destination # Accept, Reject, next rule
        self.variable = variable
        self.condition = condition
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.variable:
            return f'Rule:{self.variable}{self.condition}{self.value}:{self.destination}'
        
        return f'Rule:{self.destination}'

    # returns the name of the next rule to execute, including A, R
    def execute(self, part):
        print(f'\t\t{self}:', end='')
        if self.condition:  # ('a', '>')
            match self.condition:
                case '>':
                    if part[self.variable] > self.value:
                        print(f'-> {self.destination} >')
                        return self.destination
                    
                    print(f'None')
                    return None
                case '<':
                    if part[self.variable] < self.value:
                        print(f'-> {self.destination} <')
                        return self.destination
                    
                    print(f'None')
                    return None
        
        print(f'-> {self.destination} NA')
        return self.destination
            
# returns the next workflow to apply
def apply_workflow(workflow, part):
    print(f'\tApply {workflow}:')
    for rule in workflow:
        result = rule.execute(part)
        if result:
            return result
        
    print('ERROR: should not get here')
    return None
        
def process_part(workflows, part):
    destination = 'in'
    while destination not in ('A', 'R'):
        workflow = workflows[destination]
        destination = apply_workflow(workflow, part)

    if destination == 'A':
        print(part.values())
        return sum(part.values())
    
    return 0

# Rules

# condition    var <>
# accept if
# reject if
# forward if

workflow_re = re.compile(r'([a-z]+){(.*)}')
condition_re = re.compile(r'([asmx])([><])(\d+):([a-zAR]+)')
def parse_workflow(text):
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
    return {x : int(y) for x, y in part_re.findall(text)}

def load_file(filename: str):
    """Load lines from file into ___
        
       filename: the file to read game descriptions from.
       returns: ...
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # read a grid of text into 2D grid
            (workflow_text, instructions_text) = file.read().split('\n\n')
            workflows = {x: y for x, y in map(parse_workflow, workflow_text.split('\n'))}
            parts = map(parse_part, instructions_text.split('\n'))

            return (workflows, list(parts))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

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

            #
            # Part One
            #
            print('workflows:', workflows)
            print('Parts:', parts)
            
            p = []
            for part in parts:
                p.append(process_part(workflows, part))

            print(p)
            print(sum(p))

            #
            # Part Two
            #

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
