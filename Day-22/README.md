# Day 22: Sand Slabs

[Advent of Code 2023 -- Day 22](https://adventofcode.com/2023/day/22)

## Part One

- jenga
- blocks start spaced out and "drop" into place at t0
- count how many blocks are "expendable" that if they were removed, nothing in the tower would shift

## Part Two

- for each block, simulate removing it and count how many blocks would shift down.
- answer is sum of those block counts

- use graph of supporters and supported built in part 1 to count how many blocks would drop if the block were removed