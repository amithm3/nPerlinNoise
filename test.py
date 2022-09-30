import numpy as np
from matplotlib import pyplot
from src import Noise

mul, res = 1, 8
x, y = 128 * mul, 128 * mul
n = Noise()
mesh = np.meshgrid(np.linspace(0, x, x * res), np.linspace(0, y, y * res))


def getH():
    return n(*mesh, checkFormat=True)


h = getH()
try:
    fig, ax = pyplot.subplots()
    ax.imshow(h, cmap='Blues')
    pyplot.show()
except NameError:
    pass
