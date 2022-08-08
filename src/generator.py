from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nPerlin import NPerlin

import numpy as np


def recMemFeed(noise, *coords):
    return noise(*coords)
    try:
        h = noise(*coords)
    except MemoryError:
        c1, c2 = [], []
        [(c1.append(c[:(semiLen := len(c) // 2)]), c2.append(c[semiLen:])) for c in coords]
        h1 = recMemFeed(noise, *c1)
        h2 = recMemFeed(noise, *c2)
        h = np.concatenate((h1, h2), axis=0)
    return h


def perlinGenerator(noise: 'NPerlin', *lineSpace: tuple[float, float, float], gradient=None):
    if gradient is None: gradient = lambda a, *_coordsMesh: a
    coordsBase = [np.linspace(*ls) for ls in lineSpace]
    # noinspection PyTypeChecker
    coordsMesh: tuple['np.ndarray'] = np.meshgrid(*coordsBase)
    coords = [c.ravel() for c in coordsMesh]
    h = recMemFeed(noise, *coords)
    return gradient(h.reshape(coordsMesh[0].shape), *coordsMesh), *coordsMesh
