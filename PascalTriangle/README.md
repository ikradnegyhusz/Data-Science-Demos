# Pascal Triangle Multiples

## The goal
Which numbers in Pascal’s triangle, without its outermost 2 layers in each row, appear more than
3 times?
The script demonstrates the importance of code optimization in Python
by comparing the runtime of a slow, and an optimized implementation for answering the proposed question.

## What I've learnt
- Avoiding nested for loops is a definite improvement.
- Thinking of the problem mathematically first
will allow for improvements such as halving the runtime (like in this case).
- List comprehension, list slicing, and using optimized Python modules not only
improve runtime, they also make the code more concise and readable.

## What it does
The script first runs the calculation using the slow algorithm (it might take
some time), and then the fast one. Output is the results for each of the
calculations (which should be the same), and how many times faster the
quick implementation is.

## Conclusion
It's easy to write unoptimized code that works, but actually taking the
time to improve on it can save enormous time in the grand scheme of things.
In this case my optimized code is 1000 to 4500 times faster than the slow one.