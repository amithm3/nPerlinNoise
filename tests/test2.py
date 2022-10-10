import numpy as np
from src import *

mul, res = 1, 8
x, y = 128 * mul, 128 * mul
n = Noise(696969, (32,)*5)
ls = np.linspace(0, x, x * res), np.linspace(0, y, y * res)


def getH():
    return n(*ls, _format="expand")


if __name__ == '__main__':
    h = getH()
