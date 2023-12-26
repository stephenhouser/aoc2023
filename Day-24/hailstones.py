#!/usr/bin/env python
"""
Advent of Code 2023 - Day 24: Never Tell Me The Odds
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse
import unittest
from cProfile import Profile
from itertools import combinations
import z3

class TestAOC(unittest.TestCase):
    """Test Advent of Code"""

    #
    # Part One
    #
    def test_part1_example(self):
        """Part 1 solution for test.txt"""
        test_area = ((7, 7, 0), (27, 27, 0))
        intersections = intersections_in_area(load_file('test.txt'), test_area)
        self.assertEqual(len(intersections), 2)

    def test_part1_solution(self):
        """Part 1 solution for input.txt"""
        test_area = ((200_000_000_000_000, 200_000_000_000_000, 0),
                        (400_000_000_000_000, 400_000_000_000_000, 0))
        intersections = intersections_in_area(load_file('input.txt'), test_area)
        self.assertEqual(len(intersections), 13_910)

    #
    # Part Two
    #
    def test_part2_example(self):
        """Part 2 solution for test.txt"""
        rock = find_rock_z3(load_file('test.txt'))
        self.assertEqual(sum(rock.position), 47)

    def test_part2_solution(self):
        """Part 2 solution for input.txt"""
        rock = find_rock_z3(load_file('input.txt'))
        self.assertEqual(sum(rock.position), 618_534_564_836_937)


def c_str(cplx):
    """Pretty print a complex number as (i,j)"""
    return f'({int(cplx.real)}, {int(cplx.imag)})'

def c_tup(cplx):
    """Return a tuple(x,y) from a complex(x,y)"""
    return (int(cplx.real), int(cplx.imag))


class Hailstone:
    """Represents a ___"""
    def __init__(self, text, velocity=None):
        self.position = None
        self.velocity = None
        if velocity:
            self.position = text
            self.velocity = velocity
        elif isinstance(text, Hailstone):
            self.position = text.position
            self.velocity = text.velocity
        elif isinstance(text, str):
            self._parse_line(text)

    def _parse_line(self, text):
        """Parse text description of ___"""
        # 19, 13, 30 @ -2,  1, -2
        match = list(map(int, re.findall(r'-?\d+', text)))
        self.position = (match[0], match[1], match[2])
        self.velocity = (match[3], match[4], match[5])

    def __repr__(self):
        """Return REPL representation"""
        return str(self)

    def __str__(self):
        """Return string representation"""
        return f'{self.position}, {self.velocity}'

def load_file(filename: str):
    """Load lines from file into ___"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return list(map(Hailstone, file.readlines()))

    except FileNotFoundError:
        print('File %s not found.', filename)

    return []

def add_tuple(a, b):
    """Returns a+b: a[0]+b[0], ..."""
    # return tuple(map(lambda x, y: x + y, point, delta))
    return tuple((i+j for (i, j) in zip(a, b)))

def sub_tuple(a, b):
    """Returns a-b: a[0]-b[0], ..."""
    # return tuple(map(lambda x, y: x - y, a, b))
    return tuple((i-j for (i, j) in zip(a, b)))

def cross_tuple(a, b):
    """Returns cross product of two 3d vectors
        https://en.wikipedia.org/wiki/Cross_product
    """
    x = a[1]*b[2] - a[2]*b[1]
    y = a[2]*b[0] - a[0]*b[2]
    z = a[0]*b[1] - a[1]*b[0]
    return (x, y, z)

def dot_tuple(a, b):
    """Returns dot product of two tuples
        https://en.wikipedia.org/wiki/Dot_product
    """
    return sum(i*j for (i, j) in zip(a, b))

def vector2d_intersection(s1, s2):
    """Returns the point at which vectors s1 and s2 intersect, or None"""
    ax, ay = s1.position[0], s1.position[1]
    bx, by = s1.velocity[0], s1.velocity[1]

    cx, cy = s2.position[0], s2.position[1]
    dx, dy = s2.velocity[0], s2.velocity[1]

    det = dx*by - dy*bx
    if det == 0:
        return None

    u = (bx*(cy-ay) + by*(ax-cx)) / det
    t = (dx*(cy-ay) + dy*(ax-cx)) / det

    x = ax + bx * t
    y = ay + by * t

    if u < 0 or t < 0:
        return None

    return (x, y, 0)

def in_test_area(point, area):
    """Returns True if point is within the given area"""
    if point[0] < area[0][0] or area[1][0] < point[0]:
        return False

    if point[1] < area[0][1] or area[1][1] < point[1]:
        return False

    return True

def intersections_in_area(stones, test_area):
    """Return list of intersections that happen within test_area"""
    intersections = []
    for s1, s2 in combinations(stones, 2):
        i_point = vector2d_intersection(s1, s2)
        # print(f'{s1} and {s2} -> {i_point}')
        if i_point and in_test_area(i_point, test_area):
            # print(f'{s1} and {s2} -> {i_point}')
            intersections.append((s1, s2, i_point))

    return intersections

def print_stones(stones):
    """Pretty print list of hailstones"""
    for stone in stones:
        print(stone)

# *** Unused ***

# def intersection_2d_a(s1, rock):
#     fix_s1 = Hailstone(s1)
#     fix_s1.velocity = sub_tuple(s1.velocity, rock.velocity)

#     print('\tcheck', rock, s1, ' -> ', fix_s1)
#     return vector2d_intersection(fix_s1, rock)

# def brute_check(stones, rock):
#     intersection = intersection_2d_a(stones[0], rock)
#     print(intersection)
#     for stone in stones[1:]:
#         i_point = intersection_2d_a(stone, rock)
#         print('check', rock, stone, i_point)
#         if not i_point or i_point != intersection:
#             return False

#     return True

# def brute_check(stones, rock_velocity):
#     #arrangements = combinations(stones, 2)
#     intersection = intersection_2d_a(*(next(arrangements)), rock_velocity)
#     for s1, s2 in arrangements:
#         i_point = intersection_2d_a(s1, s2, rock_velocity)
#         print('check', s1, s2, i_point)
#         if not i_point or i_point != intersection:
#             return False

#     return True

# *** Plot things
# import matplotlib.pyplot as plt

# def project(point, delta, multiple):
#     return tuple(map(lambda x, y: x + y*multiple, point, delta))

# def plotter(stones):
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     for s in stones:
#         end = project(s.position, s.velocity, 250_000_000_000)
#         ax.plot([s.position[0]], [s.position[1]], zs=[s.position[2]], marker='o')
#         ax.plot([s.position[0], end[0]],
#                 [s.position[1], end[1]],
#                 zs=[s.position[2], end[2]])
#     plt.show()

# *** Unused ***

def find_plane(stone1, stone2):
    """Returns a normal and plane that these two stones lie on"""
    # general eq of plane: ax + by +cz + d = 0
    # need three points not on a single line
    vector1 = sub_tuple(stone1.position, stone2.position)
    vector2 = sub_tuple(stone1.velocity, stone2.velocity)
    normal = cross_tuple(vector1, vector2)
    velocity_cross = cross_tuple(stone1.velocity, stone2.velocity)
    return (normal, dot_tuple(vector1, velocity_cross))

def solve_linear(r, a, s, b, t, c):
    """Return x, y, z, that satisfies the linear equation"""
    x = r*a[0] + s*b[0] + t*c[0]
    y = r*a[1] + s*b[1] + t*c[1]
    z = r*a[2] + s*b[2] + t*c[2]
    return (x, y, z)

def find_rock_geometric(stones):
    """Return position and velocity of a rock that will intercept all
        the position and velocities of the stones.
        Using geometric formula from [Quantris](https://www.reddit.com/user/Quantris/)
    """
    # p1 = stones[0], p2 = stones[1], p3 = stones[2]
    a, plane_A = find_plane(stones[0], stones[1])
    b, plane_B = find_plane(stones[0], stones[2])
    c, plane_C = find_plane(stones[1], stones[2])

    w = solve_linear(plane_A, cross_tuple(b, c), 
                     plane_B, cross_tuple(c, a), 
                     plane_C, cross_tuple(a, b))
    t = dot_tuple(a, cross_tuple(b, c))

    # `w` is the velocity for the rock
    # given that w is integer, so force it here to avoid carrying through
    # imprecision
    w = (round(w[0] / t), round(w[1] / t), round(w[2] / t))

    # rest of the computation is integer except the final division
    w1 = sub_tuple(stones[0].velocity, w)
    w2 = sub_tuple(stones[1].velocity, w)
    ww = cross_tuple(w1, w2)

    E = dot_tuple(ww, cross_tuple(stones[1].position, w2))
    F = dot_tuple(ww, cross_tuple(stones[0].position, w1))
    G = dot_tuple(stones[0].position, ww)
    S = dot_tuple(ww, ww)

    rock = solve_linear(E, w1, -F, w2, G, ww)

    return Hailstone((int(rock[0]/S), int(rock[1]/S), int(rock[2]/S)), w)

def find_rock_z3(stones):
    """Solve using z3-solver
        Z3 is a state-of-the art theorem prover from Microsoft Research
    """
    # solve for rock and it's velocity across time
    rock = z3.RealVector('r', 3)
    velo = z3.RealVector('v', 3)
    time = z3.RealVector('t', 3)

    solver = z3.Solver()

    # add three times and stones to the solver
    for t, stone in zip(time, stones):
        # add rules to the solver, for each stone...
        # we are looking for the rock and stone to have the same position
        # at some time `t`
        solver.add(rock[0]+velo[0]*t == stone.position[0]+stone.velocity[0]*t)
        solver.add(rock[1]+velo[1]*t == stone.position[1]+stone.velocity[1]*t)
        solver.add(rock[2]+velo[2]*t == stone.position[2]+stone.velocity[2]*t)

    if solver.check():
        model = solver.model()

        rock_start = (model[rock[0]].as_long(),
                    model[rock[1]].as_long(),
                    model[rock[2]].as_long())

        rock_velocity = (model[velo[0]].as_long(),
                        model[velo[1]].as_long(),
                        model[velo[2]].as_long())

        # print(f'rock = {rock_start}, {rock_velocity}')
        return Hailstone(rock_start, rock_velocity)

    return None

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)

        with Profile() as profile:
            stones = load_file(filename)
            # print_stones(stones)

            #
            # Part One
            #
            if filename == 'test.txt':
                test_area = ((7, 7, 0), (27, 27, 0))
            else:
                test_area = ((200_000_000_000_000, 200_000_000_000_000, 0),
                             (400_000_000_000_000, 400_000_000_000_000, 0))
            intersections = intersections_in_area(stones, test_area)
            intersection_count = len(intersections)
            print(f'\t1. Number of intersections: {intersection_count:,}') # 13,910

            #
            # Part Two
            #
            #plotter(stones)
            # rock = find_rock_geometric(stones)
            # print(f'\t2. The rock {rock} gives answer: {sum(rock.position):,}')

            rock = find_rock_z3(stones)
            print(f'\t2. The rock {rock} gives answer: {sum(rock.position):,}')

        print()

    if args.profile:
        profile.print_stats('cumtime')

if __name__ == '__main__':
    main()
    #unittest.main()
