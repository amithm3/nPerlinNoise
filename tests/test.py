from matplotlib import pyplot

from test2 import getH

h = getH()

fig, ax = pyplot.subplots()
ax.imshow(h, cmap='gray')
pyplot.show()
