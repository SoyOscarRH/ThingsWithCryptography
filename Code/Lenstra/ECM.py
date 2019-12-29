
from secrets import randbelow
from math import gcd
from typing import *


def sieve_of_eratosthenes(limit: int) -> List[int]:
    ''' get me a list of primes to factor numbers until limit '''
    is_prime: List[bool] = [True for _ in range(limit + 1)]
    primes: List[int] = [2]

    current = 3
    while (current * current <= limit):
        if is_prime[current]:
            primes.append(current)
            multiple = current * 2
            while (multiple <= limit):
                is_prime[multiple] = False
                multiple += current

        current += 2

    return primes


def modular_inverse(a: int, b: int) -> Tuple[int, int, int]:
    ''' modular inverse of [a] mod [b] using gcd '''
    if b == 0:
        return (1, 0, a)

    q, r = a // b, a % b
    x, y, g = modular_inverse(b, r)

    return (y, x - q * y, g)


point = Tuple[int, int, int]


def add_point_eliptic(p: point, q: point, a: int, b: int, m: int) -> point:
    """ Add point from equation: y^2 = x^3 + [a]x + [b] mod [m] """

    if p[0] == 0:
        return q
    if q[2] == 0:
        return p

    num, denom = 0, 0

    if p[0] == q[0]:
        if (p[1] + q[1]) % m == 0:
            return (0, 1, 0)

        num = (3 * p[0] * p[0] + a) % m
        denom = (2 * p[1]) % m
    else:
        num = (q[1] - p[1]) % m
        denom = (q[0] - p[0]) % m

    inverse, _, gcd = modular_inverse(denom, m)
    if (gcd > 1):
        return (0, 0, denom)

    z = (num * inverse * num * inverse - p[0] - q[0]) % m

    return (z, (num * inverse * (p[0] - z) - p[1]) % m, 1)


def multiply_point_eliptic(k: int, p: point, a: int, b: int, m: int) -> point:
    """ Multiply point from equation: y^2 = x^3 + [a]x + [b] mod [m] (using binary exp tecnique)"""
    r: point = (0, 1, 0)

    while k > 0:
        if p[2] > 1:
            return p
        if k % 2 == 1:
            r = add_point_eliptic(p, r, a, b, m)

        k = k // 2
        p = add_point_eliptic(p, p, a, b, m)

    return r


def lenstra(composite_number: int, prime_upper_count: int) -> int:
    ''' Lenstra elliptic-curve factorization (ECM) for n=pq'''

    n = composite_number
    g = n
    q = (0, 0, 0)
    a, b = 0, 0

    while (g == n):
        q = (randbelow(n), randbelow(n), 1)
        a = randbelow(n)
        b = (q[1] * q[1] - q[0] * q[0] * q[0] - a * q[0]) % n
        g = gcd(n, 4 * a * a * a + 27 * b * b)

    if g > 1:
        return g

    for p in sieve_of_eratosthenes(prime_upper_count):
        p2 = p
        while p2 < prime_upper_count:
            q = multiply_point_eliptic(p, q, a, b, n)
            if (q[2] > 1):
                return gcd(n, q[2])

            p2 *= p

    return -1


def ECM(composite_number: int, prime_upper_count: int) -> Tuple[int, int]:
    "Factors a number using lenstra"
    p = lenstra(composite_number, prime_upper_count)
    while p == -1:
        p = lenstra(composite_number, prime_upper_count)

    return (p, composite_number // p)


if __name__ == "__main__":
    ''' 
    @author Garcia De Santiago Jorge Luis
    @author Rosas Hernandez Oscar Andres
    '''
    composite_number = int(input("A composite number n = pq: "))
    prime_upper_count = int(input("A prime to serve as a limit: "))

    factors = ECM(composite_number, prime_upper_count)

    print(f"Factors are: {factors}")
