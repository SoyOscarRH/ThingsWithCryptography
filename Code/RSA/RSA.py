from Crypto.Util.number import getPrime, GCD, inverse
from math import log2

big_length = int(log2(1e100))


class RSA:
    def __init__(self):
        p = getPrime(big_length)
        q = getPrime(big_length)

        self.n = p * q

        phi_n = (p - 1) * (q - 1)
        public_key = phi_n - 2

        while GCD(phi_n, public_key) != 1:
            public_key -= 1

        self.private_key = inverse(public_key, phi_n)
        self.public_key = public_key

    def get_keys(self):
        return self.n, public_key

    def encrypt(self, plaintext):
        return [pow(ord(char), self.public_key, self.n) for char in plaintext]

    def dencrypt(self, cipher):
        plain = [pow(char, self.private_key, self.n) for char in cipher]

        plain = [m % 26 for m in plain]
        plain = [m + ord("a") for m in plain]
        plain = [chr(m) for m in plain]

        return "".join(plain)


solver = RSA()
solver.n = 87463
solver.private_key = 50485
solver.public_key = 15157

cipher = [
    21347, 41185, 31564, 41185, 76237, 73700, 53597, 21347, 31564, 73700,
    21347, 73700, 53597, 14144, 42561, 73700, 53597, 73593, 14420, 76237,
    41185, 76237, 23637, 14420, 1, 31564, 41185, 14420, 76237, 2136,
    41185, 22481, 21347, 73700, 73593, 14420, 76237, 73700, 53597, 82282,
    19930, 22481, 14420, 31564, 73700, 53597, 31564, 14420, 41185, 76237,
    14420, 53597, 82282, 73700, 14420, 53597, 53597, 19930, 67024, 14144,
    2136, 14144, 14420, 82282, 42561, 14420,
]

message = solver.dencrypt(cipher)

print(message)
