from math import floor, sqrt
from sympy import primefactors, factorint

primes = [-1, 2, 3, 13, 17, 19, 29]
n = 87463
m = floor(sqrt(n))

i = 1
x = 1
while (i <= 7):
    ai = x + m
    b = ai * ai - n

    factors = factorint(b, limit=29)
    if all([f <= primes[-1] for f in factors.keys()]) and len(factors) > 1:

        print(f"i={i} \t ai={ai} \t x={x} \t", end="")
        print(f"{b} = ", end="")
        for prime, exponent in factors.items():
            print(f"{prime}^{exponent} * ", end="")
        print()

        i += 1

    x = -x + 1 if x < 0 else -x
