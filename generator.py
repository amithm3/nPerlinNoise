from typing import *
if TYPE_CHECKING:
    from perlin import Perlin

import numpy as np


def perlinGenerator(noise: 'Perlin', lineSpace: list[tuple[float, float, float]], gradient=None):
    if gradient is None: gradient = lambda h: h
    coordsBase = (np.linspace(*ls) for ls in lineSpace)
    # noinspection PyTypeChecker
    coordsMesh: tuple['np.ndarray'] = np.meshgrid(*coordsBase)
    coords = (c.ravel() for c in coordsMesh)

    return gradient(noise(*coords).reshape(coordsMesh[0].shape))
