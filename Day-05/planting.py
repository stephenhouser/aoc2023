#!/usr/bin/env python
"""
Advent of Code 2023 - Day 5: If You Give A Seed A Fertilizer
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
from functools import partial
from locale import format_string

from performance import timer

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
            # each entry in the planting_map is: map_domain, map_range, offset
            # if the seed value is in source range, we can just add offset to
            # then place it in the output range
            plant_map.planting_map.append( ((map_domain, map_domain+length),
                                           (map_range, map_range+length),
                                             offset) )

        return plant_map

    # map() would be a better name, but avoiding built-in names
    def convert(self, input_value):
        """Return the mapped input value. If no ranges match, return input"""
        for mapping in self.planting_map:
            domain = mapping[0]                 # mapping[0] is the domain
            #range = mapping[1]                 # mapping[1] is the range
            if domain[0] <= input_value <= domain[1]:
                return input_value + mapping[2] # mapping[1] is offset

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
# These are brute-force methods. They work well for a single seed mapping
# but take a ton of time in the case of mapping a large range of seed values
#
# There must be a better way to "project" the map through the mappings
#
@timer
def plant_iterative(seed, seed_type, almanac):
    """Return the location where a seed should be planted by consulting 
       the almanac.        
    """
    while seed_type != 'location':
        plant_map = almanac[seed_type]
        seed = plant_map.convert(seed)
        seed_type = plant_map.destination

    return seed

@timer
def plant_recursive(seed, seed_type, almanac):
    """Return the location where a seed should be planted by consulting 
       the almanac.        
    """
    if seed_type == 'location':
        return seed

    # get the planting map and recurse...
    plant_map = almanac[seed_type]
    return plant_recursive(plant_map.convert(seed), plant_map.destination, almanac)

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
        # Ugly brute-force method, maps *every* seed through the maps
        #
        min_location = None
        for (seed, length) in pairwise(seeds):
            print(format_string("%15d seeds", length, grouping=True))
            locations = map(
                partial(plant_iterative, seed_type='seed', almanac=almanac),
                range(seed, seed+length))

            local_minimum = min(list(locations))
            min_location = local_minimum if not min_location else min(min_location, local_minimum)

        print(f'\tPart 2: The minimim location for planting is {min_location}')


if __name__ == '__main__':
    main()
