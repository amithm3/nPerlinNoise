from matplotlib import pyplot

from src import linearColorGradient
from src.generator import meshgrid

grad = linearColorGradient('#009', '#099', '#990', '#900')
a = meshgrid((0, 128), (0, 128))
a -= a.max(tuple(range(1, a.ndim)), keepdims=True) / 2
a *= 2
a = ((a ** 2).sum(0) / len(a)) ** .5
h = grad(a, 3)
print(h.max((0, 1)))

fig, ax = pyplot.subplots()
ax.imshow(h, cmap="gray")
pyplot.show()
