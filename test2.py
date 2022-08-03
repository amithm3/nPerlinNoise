from matplotlib import pyplot

from src import *

noise = NPerlinNoise(frequency=8, octaves=8, dims=2)
h = perlinGenerator(noise, (0, 99, 1000), (0, 99, 1000))

fig, ax = pyplot.subplots()
ax.imshow(h * 255, cmap='gray')
fig.show()
pyplot.show()
