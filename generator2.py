import perlin2 as prl

import numpy as np


def classic_noise_3d(*args, gradient=None, noise=None, **kwargs):
    if gradient is None:
        gradient = lambda x, y, z, w: w
    if noise is None:
        noise = prl.PerlinNoise3D

    def generator():
        perlin_noise = noise(*args, **kwargs)
        x_range, y_range, z_range = yield perlin_noise
        while 1:
            x, y, z = np.meshgrid(np.arange(*x_range), np.arange(*y_range), np.arange(*z_range))
            x, y, z = x.transpose(), y.transpose(), z.transpose()
            w = gradient(x, y, z, perlin_noise.noise(x.ravel(), y.ravel(), z.ravel()))
            w.resize(z.shape)
            x_range, y_range, z_range = yield x, y, z, w

    gen = generator()
    perlin_noise = gen.send(None)
    perlin_noise.eval = lambda x, y, z: gen.send((x, y, z))

    return perlin_noise


def classic_noise_2d(*args, gradient=None, noise=None, **kwargs):
    if gradient is None:
        gradient = lambda x, y, z: z
    if noise is None:
        noise = prl.PerlinNoise2D

    def generator():
        perlin_noise = noise(*args, **kwargs)
        x_range, y_range = yield perlin_noise
        while 1:
            x, y = np.meshgrid(np.arange(*x_range), np.arange(*y_range))
            x, y = x.transpose(), y.transpose()
            z = gradient(x, y, perlin_noise.noise(x.ravel(), y.ravel()))
            z.resize(x.shape)
            x_range, y_range = yield x, y, z

    gen = generator()
    perlin_noise = gen.send(None)
    perlin_noise.eval = lambda x, y: gen.send((x, y))

    return perlin_noise


def classic_noise_1d(*args, gradient=None, noise=None, **kwargs):
    if gradient is None:
        gradient = lambda x, y: y
    if noise is None:
        noise = prl.PerlinNoise1D

    def generator():
        perlin_noise = noise(*args, **kwargs)
        x_range = yield perlin_noise
        while 1:
            x = np.arange(*x_range)
            x = x.transpose()
            y = gradient(x, perlin_noise.noise(x.ravel()))
            y.resize(x.shape)
            x_range = yield x, y

    gen = generator()
    perlin_noise = gen.send(None)
    perlin_noise.eval = lambda x: gen.send(x)

    return perlin_noise
