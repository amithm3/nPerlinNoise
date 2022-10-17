from typing import TYPE_CHECKING, Union
from functools import cache

if TYPE_CHECKING:
    from .nPerlin import NPerlin
    from .selectionTools import Gradient

import numpy as np

from .tools import iterable

lineSpaceHint = Union[tuple[float, float, float], tuple[float, float]]


@cache
def meshgrid(*ls: lineSpaceHint) -> "np.ndarray":
    """
    :param ls: (start, stop) | (start, stop, resolution) for each dimension,<br>
        start: minimum value for nth dimension coordinate<br>
        stop: maximum value for nth dimension coordinate<br>
        resolution: number of coordinates between start and stop (both included)
    :return: coordinate mesh for each nth dimension of n-dimension depth
    """
    assert all([len(sl) in (2, 3) for sl in ls]), \
        "*lineSpace must be 'tuple' of float as (start, stop) or (start, stop, resolution)"
    a = np.mgrid[tuple(slice(*(sl[0],
                               sl[1] + (step := (sl[1] - sl[0]) / ((sl[2] if len(sl) == 3 else sl[1] - sl[0]) - 1)),
                               step)) for sl in ls)]
    return a.transpose(0, *range(1, a.ndim))[::-1]


# todo: deprecate coordsMesh
def applyGrads(h: 'np.ndarray',
               coordsMesh: 'np.ndarray',
               gradients: Union[tuple["Gradient", ...], "Gradient"] = None) -> 'np.ndarray':
    """
    :param h: noise values
    :param coordsMesh: meshgrid of h
    :param gradients: gradient to be applied to h respect to dimension
    :return: gradient noise
    """
    if gradients is None: gradients = ()
    if not iterable(gradients): gradients = (gradients,)
    for g in gradients: h = g(h, coordsMesh)
    return h


def perlinGenerator(noise: 'NPerlin', *lineSpace: lineSpaceHint) -> tuple['np.ndarray', 'np.ndarray']:
    """
    generates noise values from given noise instance for given line-space

    :param noise: the noise instance to use for generating noise values
    :param lineSpace: (start, stop) | (start, stop, resolution) for each dimension,<br>
        start: minimum value for nth dimension coordinate<br>
        stop: maximum value for nth dimension coordinate<br>
        resolution: number of coordinates between start and stop (both included)<br>
    :return: tuple of noise values and coordinate mesh for each nth dimension of n-dimension depth
    """
    coordsMesh = meshgrid(*lineSpace)
    h = noise(*coordsMesh)
    return h, coordsMesh
