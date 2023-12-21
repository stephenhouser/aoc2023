#!/usr/bin/env python
"""
Advent of Code 2023 - Day 5: If You Give A Seed A Fertilizer
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
from functools import partial

class PlantingMap:
    """Map of plantings from domain->range"""

    def __init__(self, source, destination):
        """Initialize a PlantingMap with source and destination"""
        self.source = source
        self.destination = destination
        self.planting_map = []

    @classmethod
    def from_text(cls, map_text):
        """Return a new PlantingMap object parsed from the text specification.
        """
        match = re.match(r'(\w+)-to-(\w+)\s+map:', map_text)
        plant_map = PlantingMap(match.group(1), match.group(2))

        for match in re.finditer(r'(\d+)\s+(\d+)\s+(\d+)', map_text):
            map_range = int(match.group(1))
            map_domain = int(match.group(2))
            length = int(match.group(3)) + 1 # +1 to include endpoint in range
            offset = map_range - map_domain
            # each entry in the planting_map is: map_domain and offset to apply
            # if the seed value is in the domain to get it in the range
            plant_map.planting_map.append((map_domain, map_domain+length, offset))

        return plant_map

    # map() would be a better name, but avoiding built-in names
    def convert(self, input_value):
        """Return the mapped input value. If no ranges match, return input"""
        for mapping in self.planting_map:
            if mapping[0] <= input_value <= mapping[1]:
                return input_value + mapping[2]

        return input_value

    def __repr__(self):
        """Return the REPL version of object"""
        return str(self)

    def __str__(self):
        """Return the string version of object"""
        return f'PlantingMap: {self.source}->{self.destination}, {self.planting_map}'


def load_almanac(filename: str):
    """Load initial seeds to be planted and almanac from the given file
        
       filename: the file to read game descriptions from.
       returns: tuple (seeds, almanac) which is ([list], {dict})
    """
    seeds = []      # 79, 14, 55, 13
    almanac = {}    # keyed by input { input: PlantingMap(), ... }
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            almanac_text = file.read().split('\n\n')
            seeds = list(map(int, re.findall(r'\d+', almanac_text[0])))
            for plant_map_text in almanac_text[1:]:
                plant_map = PlantingMap.from_text(plant_map_text)
                almanac[plant_map.source] = plant_map

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return (seeds, almanac)

#
# This is a brute-force methods. It works well for a single seed mapping
# but takes a ton of time in the case of mapping a large range of seed values
#
def plant_recursive(seed, seed_type, almanac):
    """Return the location where a seed should be planted by consulting 
       the almanac.        
    """
    if seed_type == 'location':
        return seed

    # get the planting map and recurse...
    plant_map = almanac[seed_type]
    return plant_recursive(plant_map.convert(seed), plant_map.destination, almanac)

def apply_mapping(block, mapping):
    """Returns a set of domains mapped onto mapping
        domain (start, end)
        mapping start, end, offset
        returns mapped, leftover

        domain either gets mapped or left over
    """
    offset = mapping[2]
    mappings = []

    if block[1] < mapping[0] or block[0] > mapping[1]:
        # outside domain, leave alone, check next range
        return (None, block)

    # completely enclosed in domain of mapping, save it as mapped
    if block[0] >= mapping[0] and block[1] <= mapping[1]:
        return (((block[0]+offset, block[1]+offset), ), None)

    # split bottom part at domain[0], map the overlap, keep trying on the extra
    if block[0] <= mapping[0] and block[1] <= mapping[1]:
        mappings.append((mapping[0]+offset, block[1]+offset))
        block = (block[0], mapping[0])

    # split top part at domain[1], map the overlap, keep trying on the extra
    if block[0] >= mapping[0] and block[1] >= mapping[1]:
        mappings.append((block[0]+offset, mapping[1]+offset-1))
        block = (mapping[1]-1, block[1])

    return (mappings, block)

def apply_mappings(p_blocks, plant_map):
    """Returns the result of applying all the mappings for a plant map

       p_blocks: blocks to map [(x1, y1), (x2, y2), ...]
       returns: all the possible ranged p_blocks might end up in
            [(x1, y1), (x2, y2), ...]
    """
    blocks = list(p_blocks)

    mapped_blocks = []
    while len(blocks) > 0:
        block = blocks.pop()

        for mapping in plant_map.planting_map:
            (mapped, block) = apply_mapping(block, mapping)
            if mapped:
                mapped_blocks.extend(mapped)

            if not block:
                break

        # append the part that did not get mapped, if any
        if block:
            mapped_blocks.append(block)

    return mapped_blocks

def locate_seeds(seed_blocks, seed_type, almanac):
    """Returns lost of locations (ranges) that seeds from seed_blocks 
       will end up
    """
    if seed_type == 'location':
        return seed_blocks

    planting_map = almanac[seed_type]
    return locate_seeds(apply_mappings(seed_blocks, planting_map),
                        planting_map.destination,
                        almanac)

def pairwise(things):
    """Return a list of pairs from list.
        [1, 2, 3, 4] -> [(1, 2), (3, 4)]
    """
    thing_iter = iter(things)
    return zip(thing_iter, thing_iter)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='test.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        (seeds, almanac) = load_almanac(filename)

        #
        # Part One
        #
        locations = map(
            partial(plant_recursive, seed_type='seed', almanac=almanac),
            seeds)
        print(f'\tPart 1: The minimim location for planting is {min(locations)}')

        #
        # Part Two
        #
        min_location = None
        for (seed, length) in list(pairwise(seeds))[2:3]:
            locations = locate_seeds([(seed, seed+length)], 'seed', almanac)
            # get first element of each range
            local_minimum = min(map(lambda x: x[0], locations))
            #print(locations)

            if min_location is None:
                min_location = local_minimum
            else:
                min_location = min(min_location, local_minimum)

        print(f'\tPart 2: The minimim location for planting is {min_location}')

if __name__ == '__main__':
    main()
