# Day 24: Never Tell Me The Odds

[Advent of Code 2023 -- Day 24](https://adventofcode.com/2023/day/24)

## Part One

- each line is position and velocity (x,y,z) (dx, dy, dz)
- move velocity each nanosecond
- consider only x and y axis
- how many intersections are the in test area

Example:
- test area of (7, 7) (27, 27)

```
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
```

Example answer: _2_

Actual test area (200_000_000_000_000, 200_000_000_000_000) to (400_000_000_000_000, 400_000_000_000_000)

## Part Two

- need to find where you could throw a rock and hit all hailstones
- searching for a 3d vector that will intersect all the other vectors... oh crap.
- answer is sum of x, y, z starting position (time 0) of that vector


Resorted to looking for hints on this one. Found three approaches

 1. [Brute force](https://www.reddit.com/r/adventofcode/comments/18pptor/comment/keps780/?utm_source=share&utm_medium=web2x&context=3) by [xiaowuc1](https://www.reddit.com/user/xiaowuc1/)

 2. [Algebraic/Geometric solution](https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kersplf/) by [Quantris](https://www.reddit.com/user/Quantris/)

 3. [Z3](https://microsoft.github.io/z3guide/docs/logic/intro) "...a state-of-the art theorem prover from Microsoft Research. It can be used to check the satisfiability of logical formulas over one or more theories. Z3 offers a compelling match for software analysis and verification tools, since several common software constructs map directly into supported theories."

I'm intrigued by the `z3-solver` from Microsoft Research. This could be useful in the future. It however has a language, like tensor-flow that I'll have to learn more about.

## NOTES

- Look up "Vec3 = collections.namedtuple("Vec3", "x,y,z", defaults = (0, 0, 0))"
