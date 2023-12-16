# Day 15: Lens Library

[Advent of Code 2023 -- Day 15](https://adventofcode.com/2023/day/15)

## Part One

- input is series of comma separated strings
- write a hash() function and hash each string
-   hash = (current + ascii(letter))*17 % 256
- answer is sum of all hash values

Example: 'HASH'
 - H -> (0 + 72) * 17 % 256 == 200
 - A -> (200 + 65) * 17 % 256 == 153
 - S -> (153 + 83) * 17 % 256 == 172
 - H -> (172 + 72) * 17 % 256 == 52

Example input:

```rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7```

Example annswer: _1320_

## Part Two

- comma separated strings are a sequence of operations on 256 "boxes"
- <label> <operation> <number>
- `box` number is `hash(label)`
- operation '-' means to remove `label` from `box` preserving current order
- operation '=' means to add `label` with value `number` to box (at end).
- The solution is the sum of the `focal power` of each lens across all boxes
- `(box_index+1) * (lens_index+1) * (lens_value)`

Example:

```rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6```

Ends with:

```
0: [{rn 1},{cm 2}]
1: []
3: [{[ot 7},{ab 5},{pc 6}]
4: ... empty here on down
```

This equates to...

- rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1
- cm: 1 (box 0) * 2 (second slot) * 2 (focal length) = 4
- ot: 4 (box 3) * 1 (first slot) * 7 (focal length) = 28
- ab: 4 (box 3) * 2 (second slot) * 5 (focal length) = 40
- pc: 4 (box 3) * 3 (third slot) * 6 (focal length) = 72

Example answer: _145_