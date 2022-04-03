import warnings
from abc import ABCMeta

import numpy as np
import numexpr as ne

from tools import *

rnd = np.random


class NPerlin(metaclass=ABCMeta):
    __DIMENSION__: int
    __SPACER__: np.ndarray  # todo: improvable?

    @property
    def seed(self):
        return self.__seed

    @property
    def frequency(self):
        return self.__frequency

    @property
    def waveLength(self):
        return self.__waveLength

    def __init__(self, frequency: int = None, seed: int = None, waveLength: int = None):
        if frequency is None: frequency = 4
        if seed is None: seed = 2 ** 16 + rnd.randint(-(2 ** 16), 2 ** 16)
        if waveLength is None: waveLength = 100
        assert isinstance(frequency, int) and frequency > 1
        assert isinstance(seed, int) and 2 ** 32 > seed >= 0
        assert isinstance(waveLength, (float, int)) and waveLength > 0
        self.__seed = seed
        rnd.seed(self.__seed)
        self.__frequency = frequency
        self.__waveLength = waveLength

        self._fabric = rnd.random([self.__frequency] * self.__DIMENSION__).astype(np.float32)
        self._amp = waveLength / (self.__frequency - 1)

    def __call__(self, *coords, checkFormat=True):
        return self.__noise(*coords, checkFormat=checkFormat)

    def __noise(self, *coords, checkFormat=True):
        assert 0 < (length := len(coords)) <= self.__DIMENSION__
        coords = [*coords, *[[0]] * (self.__DIMENSION__ - length)]
        if checkFormat:
            maxLength = maxlen(coords, key=lambda x: x if iterable(x) else (x,))
            for d in range(self.__DIMENSION__):
                if not iterable(coords[d]): coords[d] = [coords[d]]
                stretch, left = divmod(maxLength, max(1, len(coords[d])))
                coords[d] = np.repeat(coords[d], stretch)
                coords[d] = np.concatenate([coords[d], np.repeat(coords[d][-1], left)], dtype=np.float32).__abs__()
        else:
            warnings.warn(
                            "Using 'checkFormat=False' is unsafe"
                            "\n     Can't guarantee safety of arguments(*coords),"                            
                            "\n     Can't use fancy parameter,"
                            "\n     May face performance uncertainty(can be slower or faster for different cases),"
                            "\n     Unexpected results and/or errors may be raised"
                            "\n Use only if you know what it does",
                            RuntimeWarning)
        coords = RefNDArray(coords)
        # coords = np.array(coords)
        assert len(coords) == self.__DIMENSION__ and len(np.shape(coords)) == 2
        coords /= self._amp
        lowerIndex = np.floor(coords).astype(np.uint16)
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
        __fabric = np.zeros(np.array(self._fabric.shape) * 2, self._fabric.dtype)
        __fabric[tuple([slice(s) for s in self._fabric.shape])] = self._fabric
        shape = self.__findShapeForExt(self._fabric.shape)
        for os, bs in zip(*shape):
            __fabric[os] = rnd.random(bs).astype(np.float32)
        self._fabric = __fabric

    @staticmethod
    def __warp(a):
        # return ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a})
        return ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': np.float32(np.pi)})

    @staticmethod
    def __findShapeForExt(shape):
        outShape = []
        baseShape = []
        for i, s in enumerate(shape):
            bS = (np.array(shape[:i]) * 2).tolist() + list(shape[i:])
            outShape.append(tuple([slice(*sorted((start, stop)))
                                   for start, stop in zip(bS, [*[0] * i, bS[i] * 2, *[0] * (s - i)])]))
            baseShape.append(bS)

        return outShape, baseShape


class Perlin1D(NPerlin):
    __DIMENSION__ = 1
    __SPACER__ = np.array(findCorners(__DIMENSION__))[:, :, None]


class Perlin2D(NPerlin):
    __DIMENSION__ = 2
    __SPACER__ = np.array(findCorners(__DIMENSION__))[:, :, None]


class Perlin3D(NPerlin):
    __DIMENSION__ = 3
    __SPACER__ = np.array(findCorners(__DIMENSION__))[:, :, None]
