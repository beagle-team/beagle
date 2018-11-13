
## Individual

4 actions in 4 configurations

* T C C C 
* C T C C 
* C C T C
* C C C T

C actions are Clicks

T actions are Types, strings of N chars.

## Crossover



### 

## Mutation

### Generic

1. Swap with individual+1 mod len(chromosome)

### Click

1. 0.5 => choose x or y
1. 0.5 => choose + or -
1. Add or remove 10

### String

1. 1/len(s) => choose a char
1. replace char at random (in printable)
