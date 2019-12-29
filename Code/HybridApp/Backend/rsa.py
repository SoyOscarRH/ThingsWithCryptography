from Crypto.Util.number import GCD, getPrime, inverse
from math import log2
from typing import List

class RSA:
    @staticmethod
    def int_to_bytes(x: int) -> bytes:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    @staticmethod
    def to_number(text: str) -> int:
        return int.from_bytes(text.encode(), "big", signed=False)

    @staticmethod
    def to_chunks(text: str, size=40) -> List[int]:
        sizes = range(size, len(text) + size, size)
        return [RSA.to_number(text[x - size:x]) for x in sizes]

    @staticmethod
    def from_chunks(chunks: List[bytes]) -> str:
        data = [RSA.int_to_bytes(chunk) for chunk in chunks]
        text = [str(raw_bytes, "utf-8") for raw_bytes in data]
        return "".join(text)

    def __init__(self, empty_value=False):
        if empty_value:
            self.n, self.private_key, self.public_key = None, None, None
            return

        big_length = 1024
        p, q = getPrime(big_length), getPrime(big_length)
        self.n = p * q

        phi_n = (p - 1) * (q - 1)
        self.public_key = phi_n - 2

        while GCD(phi_n, self.public_key) != 1:
            self.public_key -= 1

        self.private_key = inverse(self.public_key, phi_n)

    def encrypt(self, plaintext: str):
        chunks = RSA.to_chunks(plaintext)
        return [pow(chunk, self.public_key, self.n) for chunk in chunks]

    def decrypt(self, cipher: List[int]):
        almost_plain = [pow(chunk, self.private_key, self.n)
                        for chunk in cipher]
        return RSA.from_chunks(almost_plain)
