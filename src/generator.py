from typing import TYPE_CHECKING, Union
from functools import cache

if TYPE_CHECKING:
    from .nPerlinOld import NPerlin
    from .selectionTools import Gradient

import numpy as np

from .tools import iterable


@cache
def getMesh(lineSpace):
    coordsBase = [np.linspace(*ls) for ls in lineSpace]
    return np.meshgrid(*coordsBase)


def perlinGenerator(noise: 'NPerlin',
                    *lineSpace: tuple[float, float, float],
                    gradient: Union[tuple["Gradient", ...], "Gradient"] = None):
    if gradient is None: gradient = ()
    if not iterable(gradient): gradient = (gradient,)
    coordsMesh = getMesh(lineSpace)
    print("\33[32m Ignore Below Warning, using perlinGenerator \33[0m")
    h = noise(*coordsMesh, checkFormat=False)
    for g in gradient: h = g(h, *coordsMesh)
    return h, *coordsMesh
