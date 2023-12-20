# Day 20: Pulse Propagation

## Part One

- <type><node> -> <node>, <node>, ...
- `%` flip flop; initally `off`, 'low' triggers state change and send
- `&` conjunction; initially 'low', send 'high' unless all inputs are 'high' then send low
- `broadcaster` - sends low to all destinations on 'press'
- Button press triggers low pulse to `broadcaster`


Example 1 answer: _32000000_ (8000 low, 4000 high)

Example 2 answer: _11687500_ (4250 low, 2650 high)


## Part Two