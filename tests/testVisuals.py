from matplotlib import pyplot

from testProfile import getH

h = getH()

fig, ax = pyplot.subplots()
ax.imshow(h, cmap='gray')
pyplot.show()
