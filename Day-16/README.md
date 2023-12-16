# Day 16: The Floor Will Be Lava

## Part One

- input is 2d map of `.` empty, '\` '/' reflectors and `|`, `-` beam splitters
- you trace the path 'energizing' tiles along the way, splitting and reflecting
- beam ends if it goes off end of map
- enter from top, left goting eastward
- answer is how many tiles were energized (don't count things twice)

Example:
```
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
```

Here is what is energized from this..

```
######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
```

Example answer: _46_

## Part Two

- if you enter from every row (front and back) and every column (top and bottom)
- what is the maximum energized tiles, e.g. where could you enter from and get the max.
- answer is the max number of energized tiles.

Example answer: _51_ (entering from (5,0) "fourth tile from the left in the top row")

## Notes

You can use complex numbers for x, y and direction. There are a number of nifty properties of doing this.

`pos = (r, i) ==> (x, y)`

See the code for these details

create a dictionary indexed by a complex number
- `tile_map[complex(i,j)] = 'thing'`
- if direction `(dx, dy)` is a complex number `complex(-1, 0)` you can just add them and get the new position
- complex(0, 0) + complex(0, 1) == complex(0, 1)
- complex(0, -1) = -1j

