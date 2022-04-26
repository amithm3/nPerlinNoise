from matplotlib import pyplot
import numpy as np

from generator import perlinGenerator
from perlin import PerlinNoise

noise = PerlinNoise(2, octaves=8, _range=(0, 100))
def marbleGrad(a):
    w = np.sum(np.where(a == a), axis=0).reshape(a.shape)
    return np.sin(w / 10 + a)
h = perlinGenerator(noise, [(0, 100, 1000)] * 2, gradient=marbleGrad)

try:
    fig, ax = pyplot.subplots()
    if len(h.shape) > 1:
        ax.imshow(h, cmap='gray')
    else:
        ax.plot(h)
        ax.set_ylim(-.1, 1.1)
    pyplot.show()
except NameError:
    pass
