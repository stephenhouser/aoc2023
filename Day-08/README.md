# Day 8: Haunted Wasteland

## Part One

- left right instructions `RL`
- network of nodes
- start at `AAA` and end at `ZZZ`
- use instructions to navigate node, e.g. `AAA`'s right, then `CCC`s Left
- if not at `ZZZ` repeat

```
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
```

- takes 2 steps

```
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
```

Example answer: _6_

Answer: _20569_

## Part Two

- run through multiple nodes at the same time.
- start at all nodes ending with `A`
- end when all current path nodes end with `Z`
- how many steps to when they all end at the same time.

Example answer _6_

Answer: _21366921060721_