# 24-game
24 game solver in Python, fast for tuples of up to 8 numbers (although duplicate entries can allow for larger lengths).

Allowed operations are +, -, *, /, **. Fractional exponentiation is not allowed (technically not a well-defined function). Intermediate non-integer numbers within 0.005 of an integer are not allowed (due to floating point imprecision). Note that floating point imprecision can still occur.

Usage: solve(a,t,m=None)

a = array of initial values

t = target value

m = number of layers built upwards. Increase if reverse searching is taking too long, decrease if building is taking too long. For arrays of length < 9, this parameter can be left untouched.

Examples of runnable programs:
- solve([5],5)
- solve([3,3,7,7],24)
- solve([1,2,3,4,5,6,7,8],123456)
- solve([1,2,3,4,5,6,7,8],1234567)
- solve([1]*25,123456789,15)
- solve([1,2,3,4,5,6,7,8,9],123456789,6) # takes a few minutes
