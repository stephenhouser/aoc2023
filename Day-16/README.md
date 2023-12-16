

- input is `.` empty, '\` '/' reflectors and `|`, `-` splitters




## Notes

You can use complex numbers for x, y and direction.
`pos = (r, i) ==> (x, y)`

create a dictionary indexed by a complex number
- `tile_map[complex(i,j)] = 'thing'`
- if direction `(dx, dy)` is a complex number `complex(-1, 0)` you can just add them and get the new position

