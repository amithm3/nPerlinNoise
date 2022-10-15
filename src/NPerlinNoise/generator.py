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
    todo: docs

    :param ls:
    :return:
    """
    assert all([len(sl) in (2, 3) for sl in ls]), \
        "*lineSpace must be 'tuple' of float as (start, stop) or (start, stop, resolution)"
    a = np.mgrid[tuple(slice(*(sl[0],
                               sl[1] + (step := (sl[1] - sl[0]) / ((sl[2] if len(sl) == 3 else sl[1] - sl[0]) - 1)),
                               step)) for sl in ls)]
    return a.transpose(0, *range(1, a.ndim))[::-1]


def applyGrads(h, coordsMesh, gradients: Union[tuple["Gradient", ...], "Gradient"] = None):
    """
    todo: docs

    :param h:
    :param coordsMesh:
    :param gradients:
    :return:
    """
    if gradients is None: gradients = ()
    if not iterable(gradients): gradients = (gradients,)
    for g in gradients: h = g(h, coordsMesh)
    return h


def perlinGenerator(noise: 'NPerlin', *lineSpace: lineSpaceHint) -> tuple['np.ndarray', 'np.ndarray']:
    """
    generates noise values from given noise instance for given line space

    :param noise: the noise instance to use for generating noise values
    :param lineSpace: (start, stop) | (start, stop, resolution) for each dimension,
        start: minimum value for nth dimension coordinate
        stop: maximum value for nth dimension coordinate
        resolution: number of coordinates between start and stop (both included)
    :return: tuple of noise values and coordinate mesh for each nth dimension of n-dimension depth
    """
    coordsMesh = meshgrid(*lineSpace)
    h = noise(*coordsMesh)
    return h, coordsMesh
