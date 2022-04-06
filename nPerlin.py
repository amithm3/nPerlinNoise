import warnings
from typing import *

import numexpr as ne

from tools import *


class NPerlin:
    import numpy as __np
    __rnd = __np.random
    # todo: make as property
    __DIMENSION__: int
    __SPACER__: __np.ndarray

    @property
    def seed(self):
        return self.__seed

    @property
    def frequency(self):
        return self.__frequency

    @property
    def waveLength(self):
        return self.__waveLength

    def __init__(self,
                 frequency: Union[int, tuple] = None,
                 seed: int = None,
                 waveLength: float = None):
        if frequency is None: frequency = 4
        if isinstance(frequency, int): frequency = (frequency,) * self.__DIMENSION__
        if seed is None: seed = 2 ** 16 + self.__rnd.randint(-(2 ** 16), 2 ** 16)
        if waveLength is None: waveLength = 100
        assert isinstance(frequency, tuple) and all(f > 1 and isinstance(f, int) for f in frequency)
        assert len(frequency) == self.__DIMENSION__
        assert isinstance(seed, int) and 2 ** 32 > seed >= 0
        assert isinstance(waveLength, (float, int)) and waveLength > 0
        self.__seed = seed
        self.__rnd.seed(self.__seed)
        self.__frequency = frequency
        self.__waveLength = waveLength

        self._fabric = self.__rnd.random(self.__frequency).astype(self.__np.float32)
        self.__amp = [waveLength / (f - 1) for f in self.__frequency]

    def __new__(cls, *args, **kwargs):
        cls.__SPACER__ = cls.__np.array(findCorners(cls.__DIMENSION__))[:, :, None]
        return super(NPerlin, cls).__new__(cls)

    def __call__(self, *coords, checkFormat=True):
        return self.__noise(*coords, checkFormat=checkFormat)

    def __noise(self, *coords, checkFormat=True):
        assert 0 < (length := len(coords)) <= self.__DIMENSION__
        coords = [*coords, *[[0]] * (self.__DIMENSION__ - length)]
        if checkFormat:
            maxLength = maxlen(coords, key=lambda x: x if iterable(x) else (x,))
            __coords = self.__np.zeros((self.__DIMENSION__, maxLength), dtype=self.__np.float32)
            for d in range(self.__DIMENSION__):
                if not iterable(coords[d]): coords[d] = [coords[d]]
                stretch, left = divmod(maxLength, max(1, len(coords[d])))
                __coords[d, :maxLength - left] = self.__np.repeat(coords[d], stretch)
                __coords[d, maxLength - left:] = self.__np.repeat(coords[d][-1], left)
            coords = __coords.__abs__()
        else:
            warnings.warn(
                "Using 'checkFormat' as not True is unsafe"
                "\n     Can't guarantee safety of arguments(*coords),"
                "\n     Can't use fancy parameter,"
                "\n     May face performance uncertainty(can be slower or faster for different cases),"
                "\n     Unexpected results and/or errors may be raised"
                "\n Use only if you know what it does",
                RuntimeWarning)
        coords = RefNDArray(coords)
        # coords = __np.array(coords)
        assert len(coords) == self.__DIMENSION__ and len(self.__np.shape(coords)) == 2
        coords /= self.__amp
        lowerIndex = self.__np.floor(coords).astype(self.__np.uint16)
        while lowerIndex.max() >= len(self._fabric) - 1: self.extendFabric()

        bound = (lowerIndex + self.__SPACER__).transpose()
        bSpace = self._fabric[tuple(bound[:, d] for d in range(self.__DIMENSION__))]
        bSpace = bSpace.reshape((-1, *[2] * self.__DIMENSION__))
        coords -= lowerIndex

        return self.__interpolation(bSpace, coords)

    def __interpolation(self, bSpace, relativeCoord):
        if len(bSpace.shape) == 2:
            heightStretch = bSpace[:, 1] - bSpace[:, 0]
            return (self.__warp(relativeCoord) * heightStretch + bSpace[:, 0]).ravel()
        bSpace = bSpace.reshape([-1, *bSpace.shape[2:]])
        bSpace = self.__interpolation(bSpace, relativeCoord[1:].repeat(2, axis=1))
        bSpace = bSpace.reshape((-1, 2))

        return self.__interpolation(bSpace, relativeCoord[0])

    def extendFabric(self):
        __fabric = self.__np.zeros(self.__np.array(self._fabric.shape) * 2, self._fabric.dtype)
        __fabric[tuple([slice(s) for s in self._fabric.shape])] = self._fabric
        shape = self.__findShapeForExt(self._fabric.shape)
        for os, bs in zip(*shape):
            __fabric[os] = self.__rnd.random(bs).astype(self.__np.float32)
        self._fabric = __fabric

    def __warp(self, a):
        # return ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a})
        return ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': self.__np.float32(self.__np.pi)})
        # return ne.evaluate("a", local_dict={'a': a})
        # return ne.evaluate("a * a", local_dict={'a': a})
        # return ne.evaluate("a * a * a", local_dict={'a': a})
        # return ne.evaluate("where(a < .5, 0, 1)", local_dict={'a': a})

    def __findShapeForExt(self, shape):
        outShape = []
        baseShape = []
        for i, s in enumerate(shape):
            bs = (self.__np.array(shape[:i]) * 2).tolist() + list(shape[i:])  # extends each axis till 'i'
            os = tuple(slice(*sorted((start, stop)))
                       for start, stop in
                       zip(bs, [*[0] * i, bs[i] * 2, *[0] * (s - i)]))  # translates base along axis 'i'
            outShape.append(os)
            baseShape.append(bs)

        return outShape, baseShape
