# Day 6: Wait For It

[Advent of Code 2023 -- Day 6](https://adventofcode.com/2023/day/6)

## Part One

- file contains `time` and `distance` for several races
- `time` is the race time in milliseconds
- `distance` is the distance your boat needs to travel to win the race (more than)
- `time` can be divided between `charging time` and `running_time`
- for each `x` ms you charge you get speed, and go `x` mm/ms for the remainder of the race time
- `your_distance = charge * (race_time - charge)` (quadratic ==> `charge^2 + race_time * charge + distance = 0`)
- `charge_time` needs to be a whole number of ms
- Answer is product of how many ways can you win the race (how many charge_times will go > distance)

Example:
```
Time:      7  15   30
Distance:  9  40  200
```

Example answer: _288_ (`4 * 8 * 9`)

Answer:  _6209190_

## Part Two

- Ignore spaces in the time and distance lines, treat as one race `71550` ms and `940200` mm

Example answer: _71503_

Answer:  _28545089_