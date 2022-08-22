from typing import TYPE_CHECKING

if TYPE_CHECKING: from .nPerlin import NPerlin

import numpy as np

from .tools import iterable


def perlinGenerator(noise: 'NPerlin', *lineSpace: tuple[float, float, float], gradient=None):
    if gradient is None: gradient = lambda a, *_coordsMesh: a
    if not iterable(gradient): gradient = (gradient,)
    coordsBase = [np.linspace(*ls) for ls in lineSpace]
    coordsMesh: tuple['np.ndarray'] = np.meshgrid(*coordsBase)  # noqa
    coords = [c.ravel() for c in coordsMesh]
    h = noise(*coords)
    return [h := g(h.reshape(coordsMesh[0].shape), *coordsMesh) for g in gradient][-1], *coordsMesh
