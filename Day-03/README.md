#  Day 3: Gear Ratios

## Part One

- `symbols` are any non-numeric and non `.` character
- `parts` are strings of numbers adjacent to a `symbol` (including diagonal)
- The answer is the sum of all the part numbers

Example engine schematic:

```
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
```

Example answer: _4361_ ()`114` and `58` are not parts as they are not adjacent to a symbol)
Answer: _527446_

## Part Two

- `gears` are `*` symbols with exactly two (2) parts adjacent to them.
- gear `ratio` is the product of parts connected to a gear
- The answer is the sum of all gear ratios

Example answer: _467835_ (gears are `467`*`35` and `755`*`598`)
Answer:  _73201705_