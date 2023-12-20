#!/usr/bin/env python
"""
Advent of Code 2023 - Day 20: Pulse Propagation
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from collections import deque
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

class LogicNode:
    """Represents a ___"""
    def __init__(self, text):
        self.name = None
        self.gate = None
        self.state = False
        self.inputs = {}
        self.outputs = []
        self._parse_line(text)

    node_re = re.compile(r'^([%&]?)([a-z]+)\s+->\s+(.*)$')
    output_re = re.compile(r'[a-z]+')
    def _parse_line(self, text):
        match = LogicNode.node_re.match(text)
        self.gate = match.group(1)
        self.name = match.group(2).strip()
        self.outputs = LogicNode.output_re.findall(match.group(3))

    def add_input(self, who_from, initial_value=False):
        self.inputs[who_from] = initial_value

    def input(self, who_from, pulse):
        match self.gate:
            case '%':   # flip flop
                # trigger change on low
                if not pulse:
                    self.state = not self.state
                    return self.state
            case '&':   # nand
                # trigger low if all inputs are high
                self.inputs[who_from] = pulse
                self.state = not all(self.inputs.values())
                return self.state
            case '':  # broadcaster
                # send low on "press"
                return pulse

        return None

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'{self.gate}{self.name}:{self.state} in={self.inputs} out={self.outputs}'

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            circuit = {}
            for line in file.readlines():
                node = LogicNode(line)
                circuit[node.name] = node

            # wire up inputs based on outputs
            gates = list(circuit.values())
            for gate in gates:
                for output_gate in gate.outputs:
                    if output_gate in circuit:
                        circuit[output_gate].add_input(gate.name)
                    else:
                        circuit[output_gate] = LogicNode(f'{output_gate} -> ')

            return circuit

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def print_circuit(circuit):
    for gate in circuit:
        print(circuit[gate])

def press_button(circuit, press_times=1):
    low_pulses = 0
    high_pulses = 0

    for _ in range(press_times):
        pulses = deque([('button', 'broadcaster', False)])
        while pulses:
            from_gate, to_gate, pulse = pulses.pop()
            #print(f'{from_gate} : {pulse} -> {to_gate}')
            if pulse:
                high_pulses += 1
            else:
                low_pulses += 1

            gate = circuit[to_gate]
            output_pulse = gate.input(from_gate, pulse)

            if output_pulse is not None:
                for output_gate in gate.outputs:
                    pulses.appendleft((to_gate, output_gate, output_pulse))


    print(f'low={low_pulses}, high={high_pulses}')
    return low_pulses * high_pulses

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            circuit = load_file(filename)

            #
            # Part One
            #
            pulse_count = press_button(circuit, 1000)
            print(f'\t1. The number of high * low pulses is: {pulse_count}')

            #
            # Part Two
            #

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
