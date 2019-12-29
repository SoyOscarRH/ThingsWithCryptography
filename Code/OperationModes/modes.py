import base64
from Cryptodome.Cipher import AES, DES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad

from PIL import Image
import sys

def get_BMP_bytes(original_image):
    result = bytearray()
    original_data = original_image.getdata()
    for pixel in original_data:
        result.append(pixel[0])
        result.append(pixel[1])
        result.append(pixel[2])

    return result, len(original_data)


def get_pixels(bytes, original_size):
    pixels = []
    current, original_size = 0, original_size * 3

    while current + 2 < original_size:
        pixels.append((bytes[current], bytes[current + 1], bytes[current + 2]))
        current += 3

    return pixels


iv = b'\xd8r\x15\xdc|y6\xbbs\xf2\x7f:\x0b\xcb#t'
key = b'\xef\xd2\xba\xd8\x91\x9aW\xa7\x1c^\xfdO\xe1)?#'

iv_mini = b'-8B key-'
key_mini = b'-8B key-'

class Helper:
    def __init__(self, algo, mode):
        if mode != AES.MODE_ECB:
            if algo == AES:
                self.cipher = algo.new(key_mini, mode, iv_mini)
            else:
                self.cipher = algo.new(key, mode, iv)
        else:
            self.cipher = algo.new(key, mode)

    def encrypt(self, plaintext):
        plaintext = pad(plaintext, AES.block_size)
        return self.cipher.encrypt(plaintext)


    def decrypt(self, encoded):
        encoded = pad(encoded, AES.block_size)
        return self.cipher.decrypt(encoded)

class Helper:
    def __init__(self, algo, mode):
        self.not_needs_padding = AES.MODE_OFB == mode or DES.MODE_OFB  == mode

        if mode == AES.MODE_ECB or mode == DES.MODE_ECB:
            self.cipher = algo.new(key, mode)
        else:
            self.cipher = algo.new(key, mode, iv)


    def encrypt(self, plaintext):
        if self.not_needs_padding:
            return self.cipher.encrypt(plaintext)
        else:
            plaintext = pad(plaintext, 16)
            return self.cipher.encrypt(plaintext)


    def decrypt(self, encoded):
        if self.not_needs_padding:
            return self.cipher.decrypt(encoded)
        else:
            encoded = pad(encoded, 16)
            return self.cipher.decrypt(encoded)


def create_encoded_image(algo, mode, path_plain, path_encoded):
    x = Helper(algo, mode)
    original_image = Image.open(path_plain)

    plain, size = get_BMP_bytes(original_image)
    encoded = x.encrypt(plain)[:len(plain)]

    encoded_array = bytearray(encoded)
    print(len(plain))
    print(len(encoded))

    pixels = get_pixels(encoded_array, size)


    edited = original_image.copy()
    edited.putdata(pixels)

    edited.save(path_encoded)


def recover_image(algo, mode, path_encoded, path_plain):
    x = Helper(algo, mode)

    encoded_image = Image.open(path_encoded)

    encoded, size = get_BMP_bytes(encoded_image)
    plain = x.decrypt(encoded)

    plain_array = bytearray(plain)
    print(len(encoded))
    print(len(plain))

    pixels = get_pixels(plain_array, size)


    recovered = encoded_image.copy()
    recovered.putdata(pixels)

    recovered.save(path_plain)

create_encoded_image(AES, AES.MODE_CBC, "./Uploads/Japan.bmp", "./Uploads/Japan2.bmp")
recover_image(AES, AES.MODE_CBC, "./Uploads/Japan2.bmp", "./Uploads/Japan3.bmp")
