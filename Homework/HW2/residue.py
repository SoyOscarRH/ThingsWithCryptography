
from sympy.ntheory import legendre_symbol

def is_prime(n):
    if (n <= 1):
        return False
    if (n <= 3):
        return True

    if (n % 2 == 0 or n % 3 == 0):
        return False

    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6

    return True


n = 87463
for i in range(3, 50):
    if is_prime(i) and legendre_symbol(n, i) == 1:
        print(i)
