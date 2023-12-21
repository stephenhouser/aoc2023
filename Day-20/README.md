# Day 20: Pulse Propagation

## Part One

- <type><node> -> <node>, <node>, ...
- `%` flip flop; initally `off`, 'low' triggers state change and send
- `&` conjunction; initially 'low', send 'high' unless all inputs are 'high' then send low
- `broadcaster` - sends low to all destinations on 'press'
- Button press triggers low pulse to `broadcaster`

Example 1 answer: _32000000_ (8000 low, 4000 high)

Example 2 answer: _11687500_ (4250 low, 2650 high)

The easy part
- build LogicGate class
- assemble gates into circuit
- wire up inputs and outputs, account for untyped nodes
- "run" simulation for 1,000 cycles
- track high and low pulses

## Part Two

- find the clock cyle that the final `rx` node gets sent a `low` pulse.
- turns out this is a long way into the future.
- definitely see cycles and groups in the input. Several nodes are related to each other.
- looks like a counter.
- broadcaster sends to `gh` which sends to `jd` which is in a 12 or so node cluster
- it counts up and pulses into `xc` then `tj` and finally `rx`
- `rx` only has `tj` as input.
- `tj` has only `xc`, `vt`, `sk`, and `kk` as inputs. those connect to four groups
- look for cycles in those terminating nodes
- yup. least common multiple is bang-on
- trace back from `rx` to multiple nodes, look for when each one cycles, report that
- compute lcm.
- lot of drawing. was off by one for each node on first guess, I can't count