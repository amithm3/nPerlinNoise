from typing import TYPE_CHECKING, Union
from functools import cache

if TYPE_CHECKING:
    from .nPerlin import NPerlin
    from .selectionTools import Gradient

import numpy as np

from .tools import iterable


@cache
def meshgrid(*ls):
    a = np.mgrid[tuple(slice(*(sl[0],
                               sl[1] + (step := (sl[1] - sl[0]) / ((sl[2] if len(sl) == 3 else sl[1] - sl[0]) - 1)),
                               step)) for sl in ls)]
    return a.transpose(0, *range(1, a.ndim))


def perlinGenerator(noise: "NPerlin",
                    *lineSpace: Union[tuple[float, float, float], tuple[float, float]],
                    gradient: Union[tuple["Gradient", ...], "Gradient"] = None):
    assert all([len(sl) in (2, 3) for sl in lineSpace]), \
        "*lineSpace must be 'tuple' of float as (start, stop) or (start, stop, resolution)"
    if gradient is None: gradient = ()
    if not iterable(gradient): gradient = (gradient,)
    coordsMesh = meshgrid(*lineSpace)
    h = noise(*coordsMesh)
    for g in gradient: h = g(h, *coordsMesh)
    return h, *coordsMesh
