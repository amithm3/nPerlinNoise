from src.generator import meshgrid
from src import *

mul, res = 1, 8
x, y = 128 * mul, 128 * mul
n = Noise()


def getH():
    return n(*meshgrid((0, x, x * res), (0, y, y * res)))


if __name__ == '__main__':
    h = getH()
