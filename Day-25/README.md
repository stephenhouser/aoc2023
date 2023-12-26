# Day 25: Snoverload

[Advent of Code 2023 -- Day 25](https://adventofcode.com/2023/day/25)

## Part One

- input is list of `node: neighbors`
- neighbor might be an end node and not listed as a `node:`
- other nodes might be connected but not listed in a node's neighbor list

"Find the three wires you need to disconnect in order to divide the components into two separate groups. What do you get if you multiply the sizes of these two groups together?"

Example:

```
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
```

If you cut `hfx`/`pzl`, `bvb`/`cmg`, and `nvd`/`jqt` the graph is broken into two groups of `9` and `6` nodes. The product of which is `54`

Example answer: _54_

(vkd, qfb)
(hqq, xxq)
(xzz, kgl)

- https://towardsdatascience.com/beauty-of-kargers-algorithm-6de7e923874a

## Part Two

- It's a secret