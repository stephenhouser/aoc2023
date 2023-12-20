#!/usr/bin/env python
"""
Advent of Code 2023 - Day 19: Aplenty
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
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
        # print(f'\t\t{self}:', end='')
        if self.condition:  # ('a', '>')
            match self.condition:
                case '>':
                    if part[self.variable] > self.value:
                        # print(f'-> {self.destination} >')
                        return self.destination
                    
                    # print(f'None')
                    return None
                case '<':
                    if part[self.variable] < self.value:
                        # print(f'-> {self.destination} <')
                        return self.destination
                    
                    # print(f'None')
                    return None
        
        # print(f'-> {self.destination} NA')
        return self.destination


def get_accepted(workflows, start):
    start_range = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}

    rejected = []
    accepted = []
    open = [(workflows[start], start_range)]

    while open:
        workflow, counts = open.pop()
        # print(f'{workflow}')

        for rule in workflow:
            if rule.condition:
                rule_counts = counts.copy()
                if rule.condition == '<':
                    rule_counts[rule.variable] = (rule_counts[rule.variable][0], rule.value-1)
                    counts[rule.variable] = (rule.value, counts[rule.variable][1])

                if rule.condition == '>':
                    rule_counts[rule.variable] = (rule.value+1, rule_counts[rule.variable][1])
                    counts[rule.variable] = (counts[rule.variable][0], rule.value)

                if rule.destination == 'A':
                    accepted.append(rule_counts)
                elif rule.destination == 'R':
                    rejected.append(rule_counts)
                else:
                    next_flow = workflows[rule.destination]
                    open.append((next_flow, rule_counts))
            elif rule.destination == 'A':
                accepted.append(counts)
            elif rule.destination == 'R':
                rejected.append(counts)
            else:
                next_flow = workflows[rule.destination]
                open.append((next_flow, counts))

    return accepted

def accepted_combinations(workflows):
    accepted = get_accepted(workflows, 'in')
    product = lambda a, c: a * (c[1]-c[0]+1)
    return sum(reduce(product, xmas.values(), 1) for xmas in accepted)

# returns the next workflow to apply
def apply_workflow(workflow, part):
    # print(f'\tApply {workflow}:')
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
        # print(part.values())
        return sum(part.values())
    
    return 0

    


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

def parse_workflow_two(text):
    match = workflow_re.match(text)
    workflow_name = match.group(1)

    rules = match.group(2).split(',')
    return (workflow_name, rules)

    # pop in
    #     add s<1351:px
    #     add s>1350:qqz
    
    # pop s<1351:px
    #     add s<1351:a<2006:qkg
    #     add s<1351:a>2005:m>2090:A
    #     add s<1351:a>2005:m<2091:rfg

class Node:
    def __init__(self, rule):
        self.rule = rule
        self.left = None
        self.right = None

        self.op = None
        self.value = None
        self.variable = None

    def __repr__(self):
        return str(self)

    # def __str__(self):
    #     return f'{self.rule}'

    def mstr(self, level=0):
        # ret = "\t"*level + repr(self.rule) + "\n"
        if self.rule in ('A', 'R'):
            return self.rule + '\n'
        
        ret =  f'{self.variable} {self.op} {self.value} -> ' + self.left.mstr(level+1)
        ret += '  '*level + f'{self.variable} !{self.op} {self.value} -> ' + self.right.mstr(level+1)
        return ret
        # ret = "\t"*level + self.variable + ' < ' + str(self.value) + "\n"
        # if self.lt:
        #     ret += 'LT:' + self.lt.mstr(level+1)
        # if self.ge:
        #     ret += 'GE:' + self.ge.mstr(level+1)
        # return ret

# vals = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
# def traverse(node, values):
#     if node.rule == 'A':
#         print(values)
#     elif node.rule != 'R':
#         if node.op == '<':
#         traverse(node.left, values)
#         traverse(node.right, values)


# condition_re = re.compile(r'([asmx])([><])(\d+):([a-zAR]+)')
def make_tree(workflows, rules):
    # print(f'make_tree: {rules}')

    if len(rules) == 1:
        if rules[0] in ('A', 'R'):
            return Node(rules[0])
        else:
            return make_tree(workflows, workflows[rules[0]])

    #rule_parts = rules[0].split(':')
    match = condition_re.match(rules[0])
    node = Node(rules[0])

    node.variable = match.group(1)
    node.value = int(match.group(3))
    node.op = match.group(2)
    destination = match.group(4)

    node.left = make_tree(workflows, [destination])
    node.right = make_tree(workflows, rules[1:])
    # if comparison == '<':
    #     node.lt = make_tree(workflows, [destination])
    #     node.ge = make_tree(workflows, rules[1:])
    # else:
    #     node.value += 1
    #     node.lt = make_tree(workflows, rules[1:])
    #     node.ge = make_tree(workflows, [destination])

    return node


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
            #print('workflows:', workflows)
            #print('Parts:', parts)
            
            p = []
            for part in parts:
                p.append(process_part(workflows, part))

            print(p)
            print(sum(p))

            #
            # Part Two
            #
            print(accepted_combinations(workflows))
            # t = make_tree(workflows, ['in'])
            # print(t.mstr())

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
