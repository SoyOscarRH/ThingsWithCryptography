from PIL import Image
import sys

FILE_NAME = input("Give me a bmp file: ")
DECRYPTING = False
try:
    DECRYPTING = str(sys.argv[1]) == "ENCRYPT"
except IndexError:
    DECRYPTING = False

try:
    original_image = Image.open(FILE_NAME + ".bmp")
except FileNotFoundError:
    print("Error: file not found")
    exit(0)


try:
    global RED_KEY, GREEN_KEY, BLUE_KEY
    RED_KEY = int(input("Give key value for RED: ")) % 256
    GREEN_KEY = int(input("Give key value for GREEN: ")) % 256
    BLUE_KEY = int(input("Give key value for BLUE: ")) % 256
except ValueError:
    print("No valid key")
    exit(0)
except TypeError:
    print("No valid key")
    exit(0)

edited = original_image.copy()
size_x, size_y = edited.size

keys = {'R': RED_KEY, 'G': GREEN_KEY, 'B': BLUE_KEY}

loading = 0
NUMBER_OF_PIXELS = size_x * size_y
MOD = 256

for x in range(size_x):
    for y in range(size_y):
        if (loading % 23456 == 0): print(f"loading: {loading} / {NUMBER_OF_PIXELS}")
        coordinate = (x, y)

        R, G, B = edited.getpixel(coordinate)

        if DECRYPTING:
            new_color = (
                (R + keys['R']) % MOD, 
                (G + keys['G']) % MOD, 
                (B + keys['B']) % MOD
            )
        else:
            new_color = (
                (R + MOD - keys['R']) % MOD, 
                (G + MOD - keys['G']) % MOD, 
                (B + MOD - keys['B']) % MOD
            )

        edited.putpixel(coordinate, new_color)

        loading += 1

print(f"loading: {NUMBER_OF_PIXELS} / {NUMBER_OF_PIXELS}\nComplete :D")
edited.save( ("c_" if DECRYPTING else "d_") + FILE_NAME + ".bmp")
