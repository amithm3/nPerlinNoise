from matplotlib import pyplot

from nPerlinNoise import LinearColorGradient, meshgrid

grad = LinearColorGradient("#4d8204", "#006994")
a = meshgrid((0, 128), (0, 128))
a -= a.max(tuple(range(1, a.ndim)), keepdims=True) / 2
a *= 2
a = ((a ** 2).sum(0) / len(a)) ** .5
h = grad(a)
print(h.max((0, 1)))

fig, ax = pyplot.subplots()
ax.imshow(h, cmap="gray")
pyplot.show()
