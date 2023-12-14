# Day 14: Parabolic Reflector Dish

[Advent of Code 2023 -- Day 14](https://adventofcode.com/2023/day/14)

## Part One

- input is fixed items '#', movable rocks 'O' and empty space '.'
- "tilt" the platform and all the 'O' rocks move that direction
- calculate load as sum of
- number of rocks in row * (row index) from bottom to top
- Answer is total load

Example:
```
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
```

All rocks moved north, and row weights

```
OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
```

Example answer: _136_

## Part Two

- Roll the platform through 1_000_000_000 cycles of N,W,S,E
- The answer is the `weight` at the end (same as part 1)

- NOTE: find when we loop, then calculate remainder based on mod (%)

After 1 cycle:
```
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
```

After 2 cycles:
```
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
```

After 3 cycles:
```
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
```

Example answer: _64_
