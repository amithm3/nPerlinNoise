from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .nPerlin import NPerlin
    from .selectionTools import Gradient

import numpy as np

from .tools import iterable


def perlinGenerator(noise: 'NPerlin',
                    *lineSpace: tuple[float, float, float],
                    gradient: Union[tuple["Gradient", ...], "Gradient"] = None):
    if gradient is None: gradient = ()
    if not iterable(gradient): gradient = (gradient,)
    coordsBase = [np.linspace(*ls) for ls in lineSpace]
    coordsMesh = np.meshgrid(*coordsBase)
    h = noise(*coordsMesh)
    for g in gradient: h = g(h, *coordsMesh)
    return h, *coordsMesh
