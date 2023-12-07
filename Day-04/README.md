# Day 4: Scratchcards

[Advent of Code 2023 -- Day 4](https://adventofcode.com/2023/day/4)

- Each line of the file is a scratchcard and contains the `winning_numbers` and `picks`
- The value of a card is the 2 raised to number of `picks` that match `winning_numbers`, e.g. 1, 2, 4, 8, ...
- The answer is the sum of all the card values

Example:

```
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
```

Example answer: _13_ (8 + 2 + 2 + 1 + 0 + 0)

Answer:  _32609_

# Part Two

- The number of matches on a card creates additional copies of future cards
- The answer is the number of total number of scratchcards after creating copies

Example answer: _30_ (1 x card-1, 2 x card-2, 4 x card-3, 8 x card-4, 14 x card-5, 1 x card-6)

Answer: _14624680_