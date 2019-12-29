from typing import *
point = Tuple[int, int]


def get_points(A: int, B: int, p: int) -> List[point]:
    '''y^2 = x^3 + Ax + B'''

    points: List[point] = []

    for x in range(p):
        lhs = (pow(x, 3, p) + (A * x) + B) % p

        for y in range(p):
            rhs = pow(y, 2, p)

            if lhs == rhs:
                points.append((x, y))

    return points


points = get_points(A=13, B=16, p=17)
print(points)
print(len(points))
