# Day 12 : Hot Springs

[Advent of Code 2023 -- Day 12](https://adventofcode.com/2023/day/12)

## Part One

- input is sequence of `[.?#]+` and comma delimited numbers
- `.` represents empty, `#` reading, `?` unknown (wild)
- numbers represent sequences of `#` readings
- how many different arrangements of sequences fit each row
- answer is sum of all possible arrangements

Example:

```
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
```

`???.### 1,1,3` replacing `?` with `#` or `.` we could only get a valid 1, 1, 3 sequence if the first and third `?` were replaced -> `#.#.###` = sequence of 1, 1, and 3

- `???.### 1,1,3` - 1 arrangement
- ``.??..??...?##. 1,1,3` - 4 arrangements
- `?#?#?#?#?#?#?#? 1,3,1,6` - 1 arrangement
- `????.#...#... 4,1,1` - 1 arrangement
- `????.######..#####.` 1,6,5 - 4 arrangements
- `?###???????? 3,2,1` - 10 arrangements

Last example with 10 arrangements

```
?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#
```

Example answer: _21_ possible arrangements

Answer: _6935_ possible arrangements

## Part Two

- each string is `5x` the original with `?` to join them
- each sequence is `5x` the original
- `.# 1` --> `.#?.#?.#?.#?.# 1,1,1,1,1`

Example:

- `???.### 1,1,3` - 1 arrangement
- `.??..??...?##. 1,1,3` - 16384 arrangements
- `?#?#?#?#?#?#?#? 1,3,1,6` - 1 arrangement
- `????.#...#... 4,1,1` - 16 arrangements
- `????.######..#####. 1,6,5` - 2500 arrangements
- `?###???????? 3,2,1` - 506250 arrangements

Example answer: _525152_

Answer: _3920437278260_