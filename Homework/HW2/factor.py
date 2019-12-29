#!/usr/bin/python3
# pypy python interpreter is strongly recomended

import math
import sys

# generation of new number: openssl genrsa <bits> | openssl rsa -modulus -noout

#N = 3025577890235798683543591  # 82 bit
#N = 1822370728996458306753277  # 81 bit
#N = 854626116323831524991473  # 80 bit
#N = 399066586857431823726709  # 79 bit
#N = 235311326942746619548591  # 78 bit
#N = 113576732865342496692451  # 77 bit
#N = 71346986589122957051491  # 76 bit
#N = 32621041168941237031687  # 75 bit
#N = 14838142262537816848201  # 74 bit
#N = 7574625114799379190481  # 73 bit
#N = 3541904643519702945253  # 72 bit
#N = 1753044930908746416511  # 71 bit
#N = 861256316295598761961  # 70 bit
#N = 533595842543374012417  # 69 bit
#N = 200903802201060018373  # 68 bit
#N = 93496418013679648963  # 67 bit
#N = 54570430399383971173  # 66 bit
#N = 27419891463310753159  # 65 bit
#N = 14128513504013581789  # 64 bit
#N = 6357994389398958601  # 63 bit
#N = 3191071089482212003  # 62 bit
#N = 2064846507704311861  # 61 bit
#N = 959125210334783077  # 60 bit
#N = 434686773884327407  # 59 bit
#N = 210491451967849183  # 58 bit
#N = 92092615464081619  # 57 bit
#N = 64157244473449123  # 56 bit
#N = 26408936706025597  # 55 bit
#N = 12096819068999101  # 54 bit
#N = 7875168790028311  # 53 bit
#N = 3207054426926827  # 52 bit
#N = 851821581119671  # 50 bit
#N = 832730084101
#N = 84923

sieving_array_size = 1000000

# uncomment more if not founded
primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31
]


def get_factor_base(N, primes):
    # return only values for which N is a quadratic residue
    return [prime for prime in primes if N ** ((prime - 1) // 2) % prime == 1]


def tonelli_shanks_algo(n, p):
    """ algo for solving a congruence x * x =* n by module p """

    assert p % 2 == 1

    if n ** ((p - 1) // 2) % p != 1:
        return 0

    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    #print(" = Q=%d S=%d" % (Q,S))

    # find z such as Legendre symbol (z/p) == -1
    for z in range(2, 100):
        euler_crit = z ** ((p - 1) // 2) % p
        if euler_crit == p - 1:
            break
    else:
        print(" - z not founded")
        return 0

    c = z ** Q % p
    #print(" = z=%d c=%d" % (z,c))

    R = n ** ((Q + 1) // 2) % p
    t = n ** Q % p
    M = S

    while t != 1:
        for i in range(1, M):
            if t ** (2 ** i) % p == 1:
                break
        else:
            print(" - i not founded")
        #print( " = i=%d" % (i))
        b = c ** (2 ** (M - i - 1)) % p
        R = (R * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        M = i
    return R


def is_smooth(n, factor_base):
    if n == 0:
        return False

    for factor in factor_base:
        while n % factor == 0:
            n = n / factor
    return n == 1


def gen_smooth(factor_base, max_num):
    ret = set({})
    startpoint = int(math.sqrt(N)) - sieving_array_size // 2
    endpoint = startpoint + sieving_array_size

    print(" = initializing an array for quadratic sieving")
    sieve = [x * x - N for x in range(startpoint, endpoint)]

    #print(sieve)

    for factor in factor_base:
        # tonelli shanks algo doesn't work with factor 2
        if factor == 2:
            # solving x*x=N % 2
            if N % 2 == 0:
                    R_all = [0]
            else:
                R_all = [1]
        else:
            # sqrt_N
            R = tonelli_shanks_algo(N, factor)
            assert R != 0
            R_all = [R, factor - R]

        print(" = factor %d, R_all=%s" % (factor, R_all))

        # R + faktor * k > startpoint
        # faktor * k > startpoint - R
        # k > ( startpoint - R ) // factor

        # R + faktor * k < endpoint

        for R in R_all:
            k_from = (startpoint - R + (factor - 1)) // factor
            k_to = (k_from + (endpoint - (R + factor * k_from) +
                    (factor - 1)) // factor)

            for k in range(k_from, k_to):
                x = (R + factor * k) - startpoint
                #if sieve[x]==0:
                #  continue
                val = x + startpoint

                assert sieve[x] % factor == 0

                #print("s_before[x]=%d, factor=%d"%(sieve[x],factor))
                sieve[x] //= factor
                while(sieve[x] % factor == 0):
                    sieve[x] //= factor

                if sieve[x] == 1 and x != 0:
                    ret.add(val)
                    number = val * val - N
                    assert is_smooth(number, factor_base)
                    print(" + founded %d" % (len(ret)))
                    sieve[x] = 0
                    if len(ret) > max_num:
                        return list(ret)
    return list(ret)


def generate_vector(n, factor_base):
    ret = []
    for factor in factor_base:
        times = 0
        while n % factor == 0:
            times += 1
            n /= factor
        if times % 2 == 0:
            ret.append(0)
        else:
            ret.append(1)
    return ret


def gcd(x, y):
    #print("gcd %d %d"%(x,y))
    if x < 0:
        x *= -1

    if y < 0:
        y *= -1

    if x < y:
        x, y = y, x

    while x % y != 0:
        x = x % y
        if x < y:
            x, y = y, x
    return y


def identity_matrix(height):
    return [[1 if i == j else 0 for j in range(height)] for i in range(height)]


def find_linear_combination(vector_list):
    height = len(vector_list)
    if height == 0:
        return None

    width = len(vector_list[0])
    if height < width:
        print(height, width, len(primes))
        print("failed, insufficient matrix rows. Try to uncomment more primes "
              "in source")
        return None

    # for each string: what has been multiplied
    combinations = identity_matrix(height)

    for offset in range(width):
        if vector_list[offset][offset] == 0:
            # check if all
            for x in range(width):
                if vector_list[offset][x] != 0:
                    break
            else:
                # all nulls
                return combinations[offset]
            # find a string to swap
            for y in range(offset + 1, height):
                if vector_list[y][offset] != 0:
                    vector_list[y], vector_list[offset] = vector_list[offset], vector_list[y]
                    combinations[y], combinations[offset] = combinations[offset], combinations[y]
                    break
            else:
                continue  # we didn't find a string to swap

        for y in range(offset + 1, height):
            if vector_list[y][offset] == 0:
                continue
            for x in range(width):
                vector_list[y][x] *= -1
                vector_list[y][x] += vector_list[offset][x]
                vector_list[y][x] %= 2

            # mul vector and sum two vectors
            for x in range(height):
                combinations[y][x] *= -1
                combinations[y][x] += combinations[offset][x]
                combinations[y][x] %= 2

    return combinations[-1]


def get_y(x, factor_base):
    # actually, it computes integer square root of x, x must be smooth over
    # the factor base, square root must exists
    y = 1
    for factor in factor_base:
        while x % (factor ** 2) == 0:
            #print("factor found: %d" % factor)
            x = x // (factor ** 2)
            y *= factor
    return y


def gen_dependent_subset(U, factor_base):
    print(" = finding non-trivial linear combination from vectors generated "
          "from smooth array")
    vector_list = [generate_vector(u * u - N, factor_base) for u in U]

    linear_combination = find_linear_combination(vector_list)

    if not linear_combination:
        return None

    return [u for num, u in enumerate(U) if linear_combination[num] == 1]


def factorize(N):
    factor_base = get_factor_base(N, primes)
    print("factor base: %s" % factor_base)

    print(" = generating smooth array")
    U = gen_smooth(factor_base, len(factor_base) + 20)
    # 20 is for good chance to find a non-trivial factors, probabliliy
    # of not finding ~ (1/3) ^ 20

    print(U)
    #while len(U)>num:
    #  ret.remove(random.choice(ret))

    while True:
        U_dep = gen_dependent_subset(U, factor_base)
        if not U_dep:
            print("  = bad luck")
            return 0, 0
        print("dependent subset %s" % U_dep)

        x = 1
        for u in U_dep:
            x *= u

        pre_y = 1
        for u in U_dep:
            pre_y *= u * u - N

        y = get_y(pre_y, factor_base)

        if x == y:
            print("bad dependency, removing %d from smooth array" % (U_dep[0]))
            U.remove(U_dep[0])
            continue

        f1, f2 = gcd(x + y, N), gcd(x - y, N)
        print("finished dependency: x=%d, y=%d factors: %d and %d" % (
            x, y, f1, f2))
        if f1 != N and f1 != 1 and f2 != N and f2 != 1:
            return f1, f2
        print("bad dependency, removing %d from smooth array" % (U_dep[0]))
        U.remove(U_dep[0])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage quadratic_sieve.py <N>")
        sys.exit(1)

    N = int(sys.argv[1])
    f1, f2 = factorize(N)
    print("Answer: %d and %d" % (f1, f2))