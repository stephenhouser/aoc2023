# Day 9: Mirage Maintenance

## Part One

- working to predict next item in sequence based on differences of previous elements
- given a list of numbers (n numbers)
- create new list with differences (n-1 differences)
- repeat until all differences are 0
- use last difference to predict next value at end of list
- go back up the stack using differences to predict next values
- Answer is sum of predicted values

Example:

```
0 3 6 9 12 15
```

Differences are...

```
0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0
```

Build back up; A = 3 + 0, B = 15 + A

```
0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0
```


```
0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0
```

Example answer: _68_

Answer: _2075724761_

## Part Two

- Generate backward prediction for the first element of each list

```
5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0
```

- in this case, the 5

Example answer: _2_

Answer: _1072_