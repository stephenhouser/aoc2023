# Day 13: Point of Incidence

[Advent of Code 2023 -- Day 13](https://adventofcode.com/2023/day/13)

## Part One

- input is a list of 2d maps
- looking for reflection lines (horizontal and vertical) in the map
- 1st map has reflection after column 5 and before 6 (reflection_col)
- 2nd map has reflection after row 4 and before 5 (reflection_row)
- the summary for each map is reflection_col + reflection_row * 100
- the summary for the input file is the sum of all the map summaries

Example:

```
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
```

Example answer: _405_ (`5` for the first map + `400` for the second)

## Part Two

- each map has an error (smudge) that must be "corrected"
- when the single error is corrected there is a new (single) reflection that is different than the first
- summarize the same way but with the new mirrors/reflection points

- Example if you change (1,1) (top, left) in the first map a "new" reflection appears between columns 3 and 4.
- Example if you change (5,2) a new reflection between rows 1 and 2

Example answer: _400_ (0 + (1 + 3) * 100)


