from matplotlib import pyplot

from src import *

noise = NPerlinNoise(seed=0, frequency=8, octaves=8, lacunarity=2, persistence=.6, dims=2)
h = perlinGenerator(noise, *[(0, 127, 1000)] * 2)

fig, ax = pyplot.subplots()
ax.imshow(h * 255, cmap='gray')
fig.show()
pyplot.show()
