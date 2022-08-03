from matplotlib import pyplot

from src import *

noise = NPerlin(frequency=8, dims=3)
h = perlinGenerator(noise, (0, 198, 1000), (0, 198, 1000))

fig, ax = pyplot.subplots()
ax.imshow(h * 255, cmap='gray')
fig.show()
pyplot.show()
