from perlin import PerlinNoise
from matplotlib import pyplot, cm, animation
import numpy as np

# print(cm.cmaps_listed)

# ---1D---
# p1 = PerlinNoise(1)
# x = __np.linspace(0, 100, 1000)
# y = p1(x)
# try:
#     ax = pyplot.axes()
#     ax.plot(x, y)
#     ax.set_ylim(-.1, 1.1)
# except NameError:
#     pass
# ---1D---

# ---2D---
# p2 = PerlinNoise(2)
# xBase = __np.linspace(0, 200, 200)
# yBase = __np.linspace(0, 200, 200)
# x2D, y2D = __np.meshgrid(xBase, yBase)
# x, y = x2D.ravel().astype(__np.float32), y2D.ravel().astype(__np.float32)
# z = p2(x, y)
# try:
#     ax = pyplot.axes(projection="3d")
#     ax.plot_surface(x2D, y2D, z.reshape((len(xBase), len(yBase))), cmap='plasma')
#     ax.set_zlim(-.1, 1.1)
# except NameError:
#     pass
# ---2D---

# ---3D---
p3 = PerlinNoise(3, 8)
xBase = np.linspace(0, 100, 35)
yBase = np.linspace(0, 100, 35)
# zBase = __np.linspace(-49, 49, 100)
x3D, y3D = np.meshgrid(xBase, yBase)
x, y = x3D.ravel(), y3D.ravel()
# t = p3(x, y, z).reshape((len(xBase), len(yBase), len(zBase)))
try:
    fig = pyplot.figure()
    ax = pyplot.axes(projection="3d")
    tt = p3(x, y, 0).reshape((len(xBase), len(yBase)))
    plotted = [ax.plot_surface(x3D, y3D, tt, cmap='plasma')]
    ax.set_zlim(-.1, 1.1)


    def timeStep(i):
        global tt
        tt = p3(x, y, i-50).reshape((len(xBase), len(yBase)))
        plotted[0].remove()
        plotted[0] = ax.plot_surface(x3D, y3D, tt, cmap='plasma')


    anim = animation.FuncAnimation(fig, timeStep, 100, interval=10)
except NameError:
    pass
# ---3D---


try:
    pyplot.show()
except NameError:
    pass
