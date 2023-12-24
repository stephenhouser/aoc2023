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