from nPerlin import *
# from matplotlib import pyplot, cm, animation

# print(cm.cmaps_listed)

# ---1D---
# p1 = Perlin1D()
# x = np.linspace(0, 100, 1000)
# y = p1(x)
# try:
#     ax = pyplot.axes()
#     ax.plot(x, y)
#     ax.set_ylim(-.1, 1.1)
# except NameError:
#     pass
# ---1D---

# ---2D---
p2 = Perlin2D()
xBase = np.linspace(0, 100, 5000)
yBase = np.linspace(0, 100, 5000)
x2D, y2D = np.meshgrid(xBase, yBase)
x, y = x2D.ravel().astype(np.float32), y2D.ravel().astype(np.float32)
z = p2(x, y)
try:
    ax = pyplot.axes(projection="3d")
    ax.plot_surface(x2D, y2D, z.reshape((len(xBase), len(yBase))), cmap='plasma')
    ax.set_zlim(-.1, 1.1)
except NameError:
    pass
# ---2D---

# ---3D---
# p3 = Perlin3D()
# xBase = np.linspace(0, 200, 35)
# yBase = np.linspace(0, 200, 35)
# zBase = np.linspace(-100, 100, 100)
# x3D, y3D, z3D = np.meshgrid(xBase, yBase, zBase)
# x, y, z = x3D.ravel(), y3D.ravel(), z3D.ravel()
# t = p3(x, y, z).reshape((len(xBase), len(yBase), len(zBase)))
# try:
#     fig = pyplot.figure()
#     ax = pyplot.axes(projection="3d")
#     plotted = [ax.plot_surface(x3D[:, :, 0], y3D[:, :, 0], t[:, :, 0], cmap='plasma')]
#     ax.set_zlim(-.1, 1.1)
#
#
#     def timeStep(i):
#         plotted[0].remove()
#         plotted[0] = ax.plot_surface(x3D[:, :, i+1], y3D[:, :, i+1], t[:, :, i+1], cmap='plasma')
#
#
#     anim = animation.FuncAnimation(fig, timeStep, len(t[0][0])-1, interval=1)
# except NameError:
#     pass
# ---3D---


try:
    pyplot.show()
except NameError:
    pass
