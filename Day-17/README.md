# Day 17: Clumsy Crucible

[Advent of Code 2023 -- Day 17](https://adventofcode.com/2023/day/17)

## Part One

- input is 2d map of numbers
- find lowest cost path from upper right to lower left (0,0) (12,12)
- can only move max 3 times in same direction before you must turn

Example:

```
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
```

Example best path:

```
2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
```

Example answer: _102_

- use dijkstra's but heavily modified to stop when a path goes 3 steps in same direction


## Part Two

- same input, now *must* go at least 4 steps but not more than 10 steps in any one direction without a turn.

```
2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
```

Example answer: _94_

Another example

```
111111111111
999999999991
999999999991
999999999991
999999999991
```

```
1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
```

Example answer: _71_