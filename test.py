from nPerlin import *
from matplotlib import pyplot, cm, animation

# print(cm.cmaps_listed)

# ---1D---
# p1 = Perlin1D(4, 1)
# x = np.linspace(0, 100, 1000)
# y = p1(x)
# ax = pyplot.axes()
# ax.plot(x, y)
# ax.set_ylim(-.1, 1.1)
# ---1D---

# ---2D---
# p2 = Perlin2D(4)
# xBase = np.linspace(0, 100, 1000)
# yBase = np.linspace(0, 100, 1000)
# x2D, y2D = np.meshgrid(xBase, yBase)
# x, y = x2D.ravel(), y2D.ravel()
# z = p2(x, y, checkFormat=1).reshape((len(xBase), len(yBase)))
# ax = pyplot.axes(projection="3d")
# ax.plot_surface(x2D, y2D, z, cmap='plasma')
# ax.set_zlim(-.1, 1.1)
# ---2D---

# ---3D---
# p3 = Perlin3D(4)
# xBase = np.linspace(0, 200, 100)
# yBase = np.linspace(0, 200, 100)
# zBase = np.linspace(0, 200, 200)
# x3D, y3D, z3D = np.meshgrid(xBase, yBase, zBase)
# x, y, z = x3D.ravel(), y3D.ravel(), z3D.ravel()
# t = p3(x, y, z).reshape((len(xBase), len(yBase), len(zBase)))
# fig = pyplot.figure()
# ax = pyplot.axes(projection="3d")
# plotted = [ax.plot_surface(x3D[:, :, 0], y3D[:, :, 0], t[:, :, 0], cmap='plasma')]
# ax.set_zlim(-.1, 1.1)
#
#
# def timeStep(i):
#     plotted[0].remove()
#     plotted[0] = ax.plot_surface(x3D[:, :, i+1], y3D[:, :, i+1], t[:, :, i+1], cmap='plasma')
#
#
# anim = animation.FuncAnimation(fig, timeStep, len(t[0][0])-1, interval=100)
# ---3D---


# pyplot.show()
