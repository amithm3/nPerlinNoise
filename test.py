import numpy as np
from matplotlib import pyplot
from src2.tools import NFabric

x, y = 1000, 1000
n = NFabric()
mesh = np.meshgrid(np.linspace(0, x, x), np.linspace(0, y, y))


def getH():
    return n[mesh]


h = getH()
fig, ax = pyplot.subplots()
ax.imshow(h, cmap='gray')
pyplot.show()
