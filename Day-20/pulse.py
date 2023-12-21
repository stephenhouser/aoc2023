#!/usr/bin/env python
"""
Advent of Code 2023 - Day 20: Pulse Propagation
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
import math
from collections import deque
from cProfile import Profile


class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example1(self):
        """Part 1 solution for test-1.txt"""
        circuit = attach_gates(load_file('test-1.txt'))
        pulses = count_pulses(circuit, 1000)
        self.assertEqual(pulses, 32_000_000)

    def test_part1_example2(self):
        """Part 1 solution for test-2.txt"""
        circuit = attach_gates(load_file('test-2.txt'))
        pulses = count_pulses(circuit, 1000)
        self.assertEqual(pulses, 11_687_500)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        circuit = attach_gates(load_file('input.txt'))
        pulses = count_pulses(circuit, 1000)
        self.assertEqual(pulses, 818_649_769)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Part 2 solution for test-1.txt"""
        # circuit = attach_gates(load_file('test.txt')) # reset
        # pulse_count = find_low_pulse(circuit, 'rx')
        # self.assertEqual(test_function('test.txt', 10), 0)

    def test_part2_solution(self):
        """Part 2 solution for input.txt"""
        circuit = attach_gates(load_file('input.txt')) # reset
        pulse_count = find_low_pulse(circuit, 'rx')
        self.assertEqual(pulse_count, 246_313_604_784_977)


class LogicNode:
    """Represents a logic gate"""

    def __init__(self, text):
        self.name = None        # name of node
        self.gate = None        # the gate tyle % &, or !
        self.state = False      # current state, True, False
        self.inputs = {}        # gates that providce input to this gate
        self.outputs = []       # gates I send output to
        self._parse_line(text)

    node_re = re.compile(r'^([%&!]?)([a-z]+)\s+->\s+(.*)$')
    output_re = re.compile(r'[a-z]+')
    def _parse_line(self, text):
        match = LogicNode.node_re.match(text)
        self.gate = match.group(1)
        self.name = match.group(2).strip()
        self.outputs = LogicNode.output_re.findall(match.group(3))

    def add_input(self, who_from, initial_value=False):
        """Add an input gate to this gate"""
        self.inputs[who_from] = initial_value

    def input(self, who_from, pulse):
        """Send a pulse to the gate, changes its state and returns
            None if no resulting pulse, True for a 'high' and False for 'low'
        """
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

            case '!':   # untyped gates 'output', 'rx'
                return None

            case '':  # broadcaster
                return pulse    # send low on "press"

        return None

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'{self.gate}{self.name}:{self.state} in={self.inputs} out={self.outputs}'

def attach_gates(circuit):
    """Updates circuit with outputs "wired" to inputs."""
    gates = list(circuit.values())  # can't add to dictionary while iterating

    for gate in gates:
        for output_gate in gate.outputs:
            if output_gate not in circuit:
                # Add "untyped" node, use ! as prefix. 'output' and 'rx'
                circuit[output_gate] = LogicNode(f'!{output_gate} -> ')

            # add the inputs to this gate
            circuit[output_gate].add_input(gate.name)

    return circuit

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            circuit = {}
            for line in file.readlines():
                node = LogicNode(line)
                circuit[node.name] = node

            return circuit

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def print_circuit(circuit):
    """Pretty print the circuit components"""
    for gate in circuit:
        print(circuit[gate])

def count_pulses(circuit, run_time=1):
    """Returns a count of the low * high pulses as a result of simulating
        the circuit for run_time clock cycles
    """
    low_pulses = 0
    high_pulses = 0

    for _ in range(run_time):
        # each clock cycle, inject a button press at the broadcaster
        pulses = deque([('button', 'broadcaster', False)])

        # then ripple the pulses through the circuit
        while pulses:
            from_gate, to_gate, pulse = pulses.popleft()
            # print(f'{from_gate} : {pulse} -> {to_gate}')

            # count the high and low pulses
            if pulse:
                high_pulses += 1
            else:
                low_pulses += 1

            # send the pulse to the gate
            gate = circuit[to_gate]
            output_pulse = gate.input(from_gate, pulse)

            # push any generated pulses onto the back of the qeueue
            if output_pulse is not None:
                for output_gate in gate.outputs:
                    pulses.append((to_gate, output_gate, output_pulse))

    return low_pulses * high_pulses

def get_input_gates(circuit, gate_name):
    """Return a list of gates that trigger gate_name
        Used to find the terminal gates that cycle
    """
    input_gates = list(circuit[gate_name].inputs.keys())
    while len(input_gates) == 1:
        # track when these send True
        input_gates = list(circuit[input_gates[0]].inputs.keys())

    return input_gates

def find_cycles(circuit, cycle_gates):
    """Returns a dict of cycle gates and which clock they repeat on.
        Only for the cycle gates passed
        { 'xc': 2034, 'kk': 4056, ...}
    """

    # where we will track the repeating cycles found
    found_cycles = {x : 0 for x in cycle_gates}


    # loop until all found_cycles have non-zero value
    clock = 0
    while any(x==0 for x in found_cycles.values()):

        # each clock cycle, inject a button press at the broadcaster
        pulses = deque([('button', 'broadcaster', False)])
        clock += 1

        # then ripple the pulses through the circuit
        while pulses:
            from_gate, to_gate, pulse = pulses.popleft()

            # track pulses to our cycle_gates, and look for a cycle
            if from_gate in cycle_gates and pulse:
                #print(f'{clock:5}:{from_gate} sending {pulse} to {to_gate}')
                if from_gate in found_cycles and found_cycles[from_gate] != clock:
                    found_cycles[from_gate] = clock - found_cycles[from_gate]

            # send the pulse to the gate
            gate = circuit[to_gate]
            output_pulse = gate.input(from_gate, pulse)

            # push any generated pulses onto the back of the qeueue
            if output_pulse is not None:
                for output_gate in gate.outputs:
                    pulses.append((to_gate, output_gate, output_pulse))

    return found_cycles

def find_low_pulse(circuit, gate_name):
    """Returns the clock cycle at which gate_name will receive a low signal"""
    cycle_gates = get_input_gates(circuit, gate_name)
    cycles = find_cycles(circuit, cycle_gates)
    lcm = math.lcm(*list(cycles.values()))
    return lcm

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            #
            # Part One
            #
            circuit = attach_gates(load_file(filename))
            pulses = count_pulses(circuit, 1000)
            print(f'\t1. The number of high * low pulses is: {pulses:,}')

            #
            # Part Two
            #
            # 246_313_604_784_977 least common multiple of vt=3943, sk=3917, kk=3931, xc=4057
            circuit = attach_gates(load_file(filename)) # reset
            pulse_count = find_low_pulse(circuit, 'rx')
            print(f'\t2. The circuit will trigger rx low at: {pulse_count:,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
