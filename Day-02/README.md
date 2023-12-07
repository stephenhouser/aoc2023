# Day 2: Cube Conundrum

## Part One

- Each line contains a `game` of pulling colored cubes from a bag split into multiple `trials`.
- Determine which `game`s are valid for a bag with 12 red, 13 green, and 14 blue cubes.
- The answer is the sum of the `game` numbers.

Example:

```
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
```

Example answer: _8_

Your puzzle answer was _2727_

## Part Two

- Determine the minimum number of cubes needed to play each `game`.
- Compute the `power` of a game as the product of the minimum cubes needed
- The answer is the sum of the `power`s

Game 1 power is 48, and 12, 1560, 630, 36 in the remaining games

Example answer: _2286_

Your puzzle answer was _56580_
