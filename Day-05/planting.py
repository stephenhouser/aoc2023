#!/usr/bin/env python
"""
Advent of Code 2023 - Day 5: If You Give A Seed A Fertilizer
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse

class PlantingMap:
    def __init__(self, source, destination):
        """Initialize a PlantingMap with source and destination"""
        self.source = source
        self.destination = destination
        self.planting_map = []

    @classmethod
    def from_text(clss, map_text):
        """Return a new PlantingMap object parsed from the text specification.
        """
        match = re.match(r'(\w+)-to-(\w+)\s+map:', map_text)
        plant_map = PlantingMap(match.group(1), match.group(2))

        for match in re.finditer(r'(\d+)\s+(\d+)\s+(\d+)', map_text):
            destination = int(match.group(1))
            source = int(match.group(2))
            length = int(match.group(3)) + 1 # +1 to include endpoint in range
            offset = destination - source
            # each entry in the planting_map is: source_range, offset
            # if the seed value is in source range, we can just add offset to
            # then place it in the output range
            plant_map.planting_map.append( (range(source, source+length), offset) )

        return plant_map

    # map() would be a better name, but avoiding built-in names
    def convert(self, input_value):
        """Return the mapped input value. If no ranges match, return input"""
        for mapping in self.planting_map:
            if input_value in mapping[0]:       # mapping[0] is the range
                return input_value + mapping[1] # mapping[1] is offset

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

def plant(seed, seed_type, almanac):
    """Return the location where a seed should be planted by consulting 
       the almanac.        
    """
    if seed_type == 'location':
        return seed

    # get the planting map and recurse...
    plant_map = almanac[seed_type]
    return plant(plant_map.convert(seed), plant_map.destination, almanac)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='test.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        (seeds, almanac) = load_almanac(filename)

        locations = list(map(lambda x: plant(x, 'seed', almanac), seeds))
        print(f'\tThe minimim location for planting is {min(locations)}')


if __name__ == '__main__':
    main()



"""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35."""
