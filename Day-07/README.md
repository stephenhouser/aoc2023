# Day 7: Camel Cards

## Part One

Each line represents a poker _hand_ and a _bid_.

- `rank` each hand according to regular poker rules; 5-kind, ... high card
- `score` each hand by card value (in the order shown); 1=1, 2=2, ... A=13
- Order the hands by their `(rank, score)`, lowest to highest (1, 2, ...)
- Each hand is valued at its `bid` * its position in the ordered list
- Compute the sum of all values

Example: 

```
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
```

Example answer: _6440_

## Part Two

The `J` card acts as a joker. Its value is `0` but can duplicate any existing
card in the hand to make a better `rank`

Example answer _5905_