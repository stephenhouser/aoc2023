# Day 7: Camel Cards

[Advent of Code 2023 -- Day 7](https://adventofcode.com/2023/day/7)

## Part One

Each line represents a poker _hand_ and a _bid_.

- `rank` each hand according to regular poker rules; 5-kind, ... high card
- `score` each hand by card value (in the order shown); 1=1, 2=2, ... A=13
- Sort the hands lowest to highest by their `(rank, score)`
- Each hand is valued at its `bid * position`. where `position` is its position in the ordered list.
- Answer is sum of all values

Example:

```
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
```

Example answer: _6440_

Answer: _250232501_

## Part Two

- The `J` card acts as a joker. Its value is `0` but can duplicate any existing card in the hand to make a better `rank`
- Choose the best hand for the hand's value, use same `bid` * `position`
- Answer is sum of all values

Example answer _5905_

Answer: _249138943_