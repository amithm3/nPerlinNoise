import tempfile as tf
from abc import ABCMeta, abstractmethod

import numpy as np
import numexpr as ne
from numpy.lib import format as fm

rnd = np.random


def iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False


class NumpyDataCache:
    def __new__(cls, array: "np.ndarray") -> np.memmap:
        return cls.write(array)

    @classmethod
    def write(cls, array: "np.ndarray") -> np.memmap:
        file = tf.NamedTemporaryFile(suffix='.npy')
        np.save(file, array)
        file.seek(0)
        fm.read_magic(file)
        fm.read_array_header_1_0(file)
        tell = file.tell()
        memMap = np.memmap(file, mode='r+', shape=array.shape, dtype=array.dtype, offset=tell)
        memMap.file = file
        memMap.tell = tell

        return memMap


class Perlin(metaclass=ABCMeta):
    __DIMENSION__: int

    def __init__(self, frequency: int, seed: int = None, waveLength: int = 100):
        assert type(frequency) is int and frequency > 1
        assert seed is None or (type(seed) is int and 2 ** 32 > seed > 0)
        assert type(waveLength) is int and waveLength > 1

        if seed is None:
            seed = 2 ** 16 + rnd.randint(-(2 ** 16), 2 ** 16)

        self._seed = seed
        self._frequency = frequency
        self._waveLength = waveLength

        self._fabric: np.memmap

        rnd.seed(self._seed)
        self._extendFabric(initialize=True)
        self.amp = waveLength / (self._frequency - 1)

    def noise(self, *coords, checkFormat=True):
        assert 0 < (length := len(coords)) <= self.__DIMENSION__
        coords = [*coords, *[[]] * (self.__DIMENSION__ - length)]
        if checkFormat:
            maxLength = 0
            for d in range(self.__DIMENSION__):
                if not iterable(coords[d]):
                    coords[d] = [coords[d]]
                elif not coords[d]:
                    coords[d] = [0]
                if (l := len(coords[d])) > maxLength:
                    maxLength = l
            for d in range(self.__DIMENSION__):
                stretch, left = divmod(maxLength, len(coords[d]))
                _coords = []
                for c in coords[d]:
                    _coords.extend([c] * stretch)
                _coords.extend([coords[d][-1]] * left)
                coords[d] = _coords

        coords = np.array(coords)
        normalizedCoord = coords / self.amp
        lowerIndex = np.floor(normalizedCoord).astype(np.int32)
        while lowerIndex.max() >= len(self._fabric) - 1: self._extendFabric()

        bound = tuple([tuple([slice(x := int(low), x + 2) for low in i]) for i in zip(*lowerIndex)])
        bSpace = np.array([self._fabric[b] for b in bound])
        relativeCoord = normalizedCoord - lowerIndex

        return self._interpolation(bSpace, relativeCoord)

    def _extendFabric(self, initialize=False):
        if initialize:
            self._fabric = NumpyDataCache(rnd.random([self._frequency] * self.__DIMENSION__).astype(np.float32))
        else:
            __fabric = NumpyDataCache(np.zeros(np.array(self._fabric.shape) * 2, self._fabric.dtype))
            __fabric[tuple([slice(s) for s in self._fabric.shape])] = self._fabric
            shape = self.__findShapeForExt(self._fabric.shape)
            for os, bs in zip(*shape):
                __fabric[os] = rnd.random(bs).astype(np.float32)
            __fabric.flush()
            self._fabric = __fabric

    @abstractmethod
    def _interpolation(self, bSpace, relativeCoord):
        pass

    @staticmethod
    def _smoothInterpolation(a):
        return ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a})

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


class Perlin1D(Perlin):
    __DIMENSION__ = 1

    def _interpolation(self, bSpace, relativeCoord):
        heightStretch = bSpace[:, 1] - bSpace[:, 0]

        return self._smoothInterpolation(relativeCoord) * heightStretch + bSpace[:, 0]


class Perlin2D(Perlin):
    __DIMENSION__ = 2

    def _interpolation(self, bSpace, relativeCoord):
        bSpace.resize([np.prod(bSpace.shape[:2]), 2])
        bSpace = Perlin1D._interpolation(self, bSpace, relativeCoord[1].repeat(2))
        bSpace.resize([len(relativeCoord[0]), 2])

        return Perlin1D._interpolation(self, bSpace, relativeCoord[0])


class Perlin3D(Perlin):
    __DIMENSION__ = 3

    def _interpolation(self, bSpace, relativeCoord):
        print(bSpace.shape, relativeCoord.shape)
        for d in range(self.__DIMENSION__):
            pass
