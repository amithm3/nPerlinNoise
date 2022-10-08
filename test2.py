import numpy as np
# from matplotlib import pyplot
from src import *

mul, res = 1, 8
x, y = 128 * mul, 128 * mul
n = Noise(696969, 32)
mesh = np.meshgrid(np.linspace(0, x, x * res), np.linspace(0, y, y * res))


def getH():
    return n(*mesh, checkFormat=True).reshape(x * res, y * res)


h = getH()
try:
    fig, ax = pyplot.subplots()
    ax.imshow(h, cmap="gray")
    pyplot.show()
except NameError:
    pass
