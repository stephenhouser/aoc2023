# Day 10: Pipe Maze

# Part One

- find the path starting with `S` in the map
- using characters
    - `|` north-south
    - `-` east-west
    - `F` south-east
    - `L` north-east
    - `J` north-west
    - `7` south-west
    - `.` empty, ground
- the path is a loop, find the distance to the farthest node
- 1/2 the length

Example 0:

```
.....
.S-7.
.|.|.
.L-J.
.....
```

Example answer: _4 steps_

Example 1 ([test-1.txt](test-1.txt)):

```
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
```

Example answer: _8 steps_

Answer: _6815_

# Part Two

- find number of enclosed tiles
- include ground `.` and any other symbol that is not part of the loop

Example 2 ([test-2.txt](test-2.txt)):

- `I` marks tiles enclosed by the path, `O` marks tiles not encolosed by the path

```
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
```

Example answer: _4_

Example 3 ([test-3.txt](test-3.txt)):

```
OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
```

Example answer: _8_

Example 4 ([test-4.txt](test-4.txt)):

```
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
```

Example answer: _10_

Answer: _269_