from abc import ABCMeta

import numpy as np
import numexpr as ne

rnd = np.random


def iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False


class NPerlin(metaclass=ABCMeta):
    __DIMENSION__: int
    __APPENDER__: np.ndarray  # todo: auto generate for n-dims

    def __init__(self, frequency: int = None, seed: int = None, waveLength: int = None):
        if frequency is None: frequency = 4
        if seed is None: seed = 2 ** 16 + rnd.randint(-(2 ** 16), 2 ** 16)
        if waveLength is None: waveLength = 100
        assert isinstance(frequency, int) and frequency > 1
        assert isinstance(seed, int) and 2 ** 32 > seed >= 0
        assert isinstance(waveLength, (float, int)) and waveLength > 0
        self._seed = seed
        rnd.seed(self._seed)
        self._frequency = frequency
        self._waveLength = waveLength

        self._fabric = self._fabric = rnd.random([self._frequency] * self.__DIMENSION__).astype(np.float32)
        self._amp = waveLength / (self._frequency - 1)

    def __call__(self, *coords, checkFormat=True):
        return self.__noise(*coords, checkFormat=checkFormat)

    def __noise(self, *coords, checkFormat=True):
        assert 0 < (length := len(coords)) <= self.__DIMENSION__
        coords = [*coords, *[[]] * (self.__DIMENSION__ - length)]
        if checkFormat:
            maxLength = 0
            for d in range(self.__DIMENSION__):
                if not iterable(coords[d]):
                    coords[d] = [coords[d]]
                elif len(coords[d]) == 0:
                    coords[d] = [0]
                if (l := len(coords[d])) > maxLength:
                    maxLength = l
            for d in range(self.__DIMENSION__):
                stretch, left = divmod(maxLength, len(coords[d]))
                if stretch != 1 or left != 0:  # todo: improve, is bottleneck for large arrays, use numpy
                    _coords = []
                    for c in coords[d]:
                        _coords.extend([c] * stretch)
                    _coords.extend([coords[d][-1]] * left)
                    coords[d] = _coords

        coords = np.array(coords)
        normalizedCoord = coords / self._amp
        lowerIndex = np.floor(normalizedCoord).astype(np.int32)
        while lowerIndex.max() >= len(self._fabric) - 1: self.extendFabric()

        bound = (lowerIndex + self.__APPENDER__).transpose()
        bSpace = self._fabric[tuple(bound[:, d] for d in range(self.__DIMENSION__))]
        bSpace = bSpace.reshape((-1, *[2] * self.__DIMENSION__))
        relativeCoord = normalizedCoord - lowerIndex

        return self.__interpolation(bSpace, relativeCoord)

    def __interpolation(self, bSpace, relativeCoord):
        if len(bSpace.shape) == 2:
            heightStretch = bSpace[:, 1] - bSpace[:, 0]
            return self.__smoothInterpolation(relativeCoord.flatten()) * heightStretch + bSpace[:, 0]
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
    def __smoothInterpolation(a):
        # return ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a})
        return ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': np.pi})

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
    __APPENDER__ = [[[0]],
                    [[1]]]


class Perlin2D(NPerlin):
    __DIMENSION__ = 2
    __APPENDER__ = np.array([[[0], [0]], [[0], [1]],
                             [[1], [0]], [[1], [1]]])


class Perlin3D(NPerlin):
    __DIMENSION__ = 3
    __APPENDER__ = np.array([[[0], [0], [0]], [[0], [0], [1]], [[0], [1], [0]], [[0], [1], [1]],
                             [[1], [0], [0]], [[1], [0], [1]], [[1], [1], [0]], [[1], [1], [1]]])
