from matplotlib import pyplot

from test import getH

h = getH()

fig, ax = pyplot.subplots()
ax.imshow(h, cmap='gray')
pyplot.show()
