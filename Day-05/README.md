# Day 5: If You Give A Seed A Fertilizer

[Advent of Code 2023 -- Day 5](https://adventofcode.com/2023/day/5)

## Part One

- `seeds` are starting numbers we need to trace through a series of maps
- `maps` are a mapping from an input to output, e.g. `seed-to-soil` and specifies a `destination`, `source`, and `length` of the mapping.
- `humidity-to-location` is the final mapping
- translate each `seed` through all the maps to get their `locations`
- The answer is the lowest `location` value for all the seeds

Example:

```
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
```

- `seed-to-soil` defines 98-99 maps to 50-51 and 50-98 to 52-99
- seed `79` will then translate via `seed-to-soil` to `81`

Example answer: _35_ (seed `13` -> soil `13` -> fertilizer `52` -> water `41` -> light `34` -> temperature `34` -> humidity `35` -> location `35`)

Answer: _214922730_

## Part Two

- Treat the seed numbers as pairs that are `start`, `length`, e.g. `79` `14` is the range `79-92`
- from all the seeds in the described seed ranges, what is the lowest `location` result possible

Example answer: _46_ (seed `82` -> soil `84` -> fertilizer `84` -> water `84` -> light `77` -> temperature `45` -> humidity `46` -> location `46`)

Answer: _148041808_