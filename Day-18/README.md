# Day 18: Lavaduct Lagoon

[Advent of Code 2023 -- Day 18](https://adventofcode.com/2023/day/18)

## Part One

- start at arbitrary 1 meter location (location unknown)
- input is series of directions; U=NORTH, D=SOUTH, L=WEST, R=EAST with color
- follow directions, coloring the trench as you go (1 meter cubes)
- fill (dig out) interior
- answer is how many cubic meters is removed (inside the trenches)

Trenches dug:

```
#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
```

Dug _38_ cubic meters of material

Filled Lagoon:

```
#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
```

Example answer _62_ cubic meters filled

## Part Two

- the direction and length are encoded in the hex values
- first 5 digits are hex encoded distance
- last hex digit is direction 0=EAST, 1=SOUTH, 2=WEST, 3=NORTH

Now the numbers are HUGE. Time to research the Shoelace Algorithm

## NOTES

- Started with trying to avoid flood fill and use a similar technique as [Day 10](../Day-10)
- After a few hours, I gave in. Flood-fill got the job done for Part 1.
- Actually visualized by dumping the map as `.csv` and loading in Excel. There are a few `.csv` files with these for happy viewing.
- First time I guessed wrong too many times (3) and no longer got high/low hints.
- Part 2 the numbers became huge, looked up the Shoelace Algorithim that I had seen but avoided on Day 10.
- Seemed to be off, was reporting _42_ for part 1.
- Figured it had to do with the edges not being counted. Looked at `edges/2` and it was off by 1.
- Same result worked for `test.txt` and `input.txt`. Called it good and got part 2.
- Cleaned up. Left flood-fill code in there for future reference.