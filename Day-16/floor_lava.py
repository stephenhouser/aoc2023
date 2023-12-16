#!/usr/bin/env python
"""
Advent of Code 2023 - Day 16: The Floor Will Be Lava
Stephen Houser <stephenhouser@gmail.com>
"""

import copy
import argparse
import unittest

# increase recursion limit, default is 1,000
import sys
sys.setrecursionlimit(5_000)

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Test example 1 data from test.txt"""
        floor_map = load_file('test.txt')
        energized = shoot_laser(floor_map, (0, 0, 0, 1))
        self.assertEqual(energized, 46)

    def test_part1_solution(self):
        """Live data for part 1 data from input.txt"""
        floor_map = load_file('input.txt')
        energized = shoot_laser(floor_map, (0, 0, 0, 1))
        self.assertEqual(energized, 7496)

    def test_part1_complex(self):
        """Live data for part 1 data from input.txt"""
        floor_map = load_complex_map('input.txt')
        energized = traverse_complex(floor_map, [(-1, 1)])
        self.assertEqual(energized, 7496)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Test example 1 data from test.txt"""
        floor_map = load_file('test.txt')
        max_value = maximum_beam(floor_map)
        self.assertEqual(max_value, 51)

    def test_part2_solution(self):
        """Test example 1 data from test.txt"""
        floor_map = load_file('input.txt')
        max_value = maximum_beam(floor_map)
        self.assertEqual(max_value, 7932)

    def test_part2_complex(self):
        """Test example 1 data from test.txt"""
        energized = maximum_beam_complex('input.txt')
        self.assertEqual(energized, 7932)

# beam is (y, x)
# map is (char, energized)
# start at 0, 0, going E  == (0, 0, 'E)'
# save states
# stop when hit cycle
def is_marked(grid, beam):
    """Return True if this position was visited previously"""
    return grid[beam[0]][beam[1]][1] == '#'

def is_valid(grid, y, x):
    """Returns true if this position is on the map."""
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        return True

    return False

# VISITED = set()   # keep track of where we have traversed
def shoot_laser(grid, beam, visited=None):
    """Returns the number of energized cells while traversing the map

        grid is the map
        beam is (x, y, dx, dy) location and direction of the beam
    """
    if visited is None:
        visited = set()

    y, x, dy, dx = beam

    # goes off edge of board or alreadly traversed this way
    if not is_valid(grid, y, x) or beam in visited:
        return 0

    # mark this path as traversed
    # I could use this to count the number of placed traversed!
    # See below in main()
    visited.add(beam)

    # Score when we mark it
    score = 0 if grid[y][x][1] == '#' else 1
    grid[beam[0]][beam[1]][1] = '#'
    # print(f'\t{beam} : {grid[y][x]}) {score}')

    match grid[beam[0]][beam[1]][0]:    # whats in that spot?
        case '\\':
            score += shoot_laser(grid, (y+dx, x+dy, dx, dy), visited)
        case '/':
            score += shoot_laser(grid, (y-dx, x-dy, -dx, -dy), visited)
        case '-':
            # this might "bounce back" when we approach from the pointy end
            # but, that path will end when we see it's already been traversed
            score += shoot_laser(grid, (y, x-1, 0, -1), visited) + \
                    shoot_laser(grid, (y, x+1, 0,  1), visited)
        case '|':
            # same bounce back as above
            score += shoot_laser(grid, (y-1, x, -1, 0), visited) + \
                    shoot_laser(grid, (y+1, x,  1, 0), visited)
        case _:
            score += shoot_laser(grid, (y+dy, x+dx, dy, dx), visited)

    return score

def starting_beams(grid):
    """Return list of all starting locations and directions"""
    s_beams = []        
    max_y = len(grid)
    max_x = len(grid[0])
    for y in range(max_y):
        s_beams.append((y, 0, 0, 1))
        s_beams.append((y, max_x, 0, -1))

    for x in range(max_x):
        s_beams.append((0, x, 1, 0))
        s_beams.append((max_y, x, -1, 0))

    return s_beams

def maximum_beam(grid):
    energized = []
    for beam in starting_beams(grid):
        energized.append(shoot_laser(copy.deepcopy(grid), beam))

    return max(energized)


def print_grid(grid):
    """Pretty print 2D grid in readable form"""
    for row in grid:
        for col in row:
            print(f'{col[0]}{col[1]}', end=' ')
        print()

def print_marks(grid):
    """Pretty print 2D grid in readable form"""
    for row in grid:
        for col in row:
            print(f'{col[1]}', end='')
        print()

def load_file(filename: str):
    """Load lines from file into ___
        
       filename: the file to read game descriptions from.
       returns: ...
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # read a grid of text into 2D grid
            #return list(map(list, map(str.strip, file.readlines())))
            grid = []
            for line in file.readlines():
                row = []
                for ch in list(line.strip()):
                    row.append([ch, '.'])
                grid.append(row)

            return grid
            # read a list of Thing
            #return list(map(Thing, file.readlines()))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

#
# This is an alternate solution from reddit user 4HbQ in the 
# solutions thread. The key learning from this is the ability 
# to use complex numbers for this type of navigation
# 
# 1. (x, y) -> complex(x, y).  1 -> (1, 0), 1j -> (0, 1)
# 2. You can do math if you also have direction as an imaginary
#    number... and transforms (turns, etc)
# 3. create the map as a dictionary keyed by imaginary numbers
#    then indexing is easy as well tiles[pos]
# 4. use tiles.get(pos) which will return None if pos is not in the map.
#
def traverse_complex(complex_map, todo):
    done = set()    # keep track of where we have been
    while todo:     # process each item in list
        pos, dir = todo.pop()
        while not (pos, dir) in done:
            done.add((pos, dir))    # don't re-traverse in same direction
            pos += dir              # move to next
            match complex_map.get(pos):
                case '|':
                    # go south, add todo to go north
                    dir = complex(0, 1) # 1j,  currenet path
                    # split path, track this down later
                    todo.append((pos, -dir))
                case '-':
                    # go west, add todo to go east
                    dir = complex(-1, 0) # -1, current path
                    # split path, track this down later
                    todo.append((pos, -dir))
                case '/':
                    # flip and negate imag and real
                    # dir = (-dy, -dx))
                    # (dx, dy) -> (-dy, -dx)
                    #dir = -complex(dir.imag, dir.real)
                    dir = -1j / dir
                case '\\':
                    # flip dx and dy
                    # dir = (dy, dx)
                    # dir = complex(dir.imag, dir.real)
                    dir = 1j/dir
                case None:
                    break
                # left off case '.' do nothing

    return len(set(pos for pos, _ in done)) - 1

def load_complex_map(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        # returns a dictionary indexed by i,j with c as the value
        return {complex(i,j): c for j, r in enumerate(file) 
                                for i, c in enumerate(r.strip())}

def maximum_beam_complex(filename):
    c_map = load_complex_map(filename)
    starts = (
        [(pos-dir, dir)] for dir in (1,1j,-1,-1j)
                             for pos in c_map if pos-dir not in c_map
        )
    energized = []
    for start in starts:
        energized.append(traverse_complex(c_map, start))

    return max(energized)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        floor_map = load_file(filename)

        #
        # Part One
        #
        visited = set()
        energized = shoot_laser(copy.deepcopy(floor_map), (0, 0, 0, 1), visited)
        # print unique nodes that were visited, ignore direction
        print(f'\t1. Energized tiles (def): {energized}')

        energized = len(set((x,y) for x, y, _, _ in visited))
        print(f'\t1. Energized tiles (alt): {energized}')

        #
        # Part Two
        #
        max_value = maximum_beam(floor_map)
        print(f'\t1. Max Energized tiles: {max_value}')

        max_value = maximum_beam_complex(filename)
        print(f'\t1. Max Energized tiles (complex): {max_value}')
        print()

if __name__ == '__main__':
    main()
    #unittest.main()
