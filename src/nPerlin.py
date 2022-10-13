import collections
from typing import Union

import numpy as np

from .tools import NTuple, NPrng, findCorners
from .selectionTools import Warp

frequencyHint = Union[int, tuple[int, ...]]
waveLengthHint = Union[float, tuple[float]]
warpHint = Union['Warp', tuple['Warp']]
rangeHint = tuple[float, float]


class NPerlin:
    @property
    def seed(self) -> int:
        return self.__prng.seed()

    def setSeed(self, seed: int):
        self.__prng.seed(seed)

    @property
    def frequency(self) -> "NTuple[int]":
        return self.__frequency

    @property
    def mFrequency(self) -> "NTuple[int]":
        return self.__frequency * self.fwm

    def setFrequency(self, frequency: frequencyHint):
        self.__frequency = self.__getFrequency(frequency)

    @property
    def waveLength(self) -> "NTuple[float]":
        return self.__waveLength

    @property
    def mWaveLength(self) -> "NTuple[float]":
        return self.__waveLength * self.fwm

    def setWaveLength(self, waveLength: waveLengthHint):
        self.__waveLength = self.__getWaveLength(waveLength)

    @property
    def warp(self) -> "NTuple[Warp]":
        return self.__warp

    def setWarp(self, warp: warpHint):
        self.__warp = self.__getWarp(warp)

    @property
    def range(self) -> tuple[float, float]:
        return self.__range

    def setRange(self, _range: rangeHint):
        self.__range = self.__getRange(_range)

    # matrix of desired shape and offset
    def fabric(self, shape: tuple[int, ...], off: tuple[int, ...] = None) -> "np.ndarray":
        return self.__prng.shaped(shape, off)

    # multiplier for converting coords into fabric index region based on frequency and wavelength
    @property
    def amp(self) -> "NTuple[float]":
        mF, mW = self.mFrequency, self.mWaveLength
        length = max(len(mF), len(mW))
        return NTuple((f - 1) / w for f, w in zip(mF[:length], mW[:length]))

    def __repr__(self):
        return f"<seed={self.seed} freq={self.frequency} wLen={self.waveLength} warp={self.warp} range={self.range}" \
               f" fwm={self.fwm}>"

    def __init__(self,
                 seed: int = None,
                 frequency: frequencyHint = 8,
                 waveLength: waveLengthHint = 128,
                 warp: warpHint = None,
                 _range: rangeHint = None,
                 *,
                 fwm: int = 1):
        """
        :param seed: seed for prng values, default random value
        :param frequency: number of random values in one unit respect to dimension, default 8
        :param waveLength: length of one unit respect to dimension, default 128
        :param warp: the interpolation function used between random value nodes, default selectionTools.Warp.improved()
        :param _range: bound for noise values, output will be within the give range, default (0, 1)
        :param fwm: key word only - frequency, waveLength multiplier
        """
        if warp is None: warp = Warp.improved()
        if _range is None: _range = (0, 1)

        assert isinstance(fwm, int) and fwm > 0, \
            "kew word only param fwm must be 'int' > 0"

        self.__prng = NPrng(seed)  # matrix generator of random value nodes
        self.__frequency = self.__getFrequency(frequency)
        self.__waveLength = self.__getWaveLength(waveLength)
        self.__warp = self.__getWarp(warp)
        self.__range = self.__getRange(_range)
        self.fwm = fwm

    def __call__(self, *coords: Union["collections.Iterable", float]) -> "np.ndarray":
        fCoords, shape = self.formatCoords(coords)
        bIndex, rCoords = self.findBounds(fCoords)
        fab = self.findFab(bIndex)
        bSpace = fab[tuple(bIndex - bIndex.min((1, 2), keepdims=True))]
        return self.applyRange(self.bNoise(bSpace.T, rCoords.T)).reshape(shape)

    def bNoise(self, bSpace, rCoords):
        dims = rCoords.shape[1]
        pairs = bSpace.reshape(-1, 2)
        # collapse dimensions
        for d in range(dims - 1, 0, -1):
            coords = rCoords[:, d].repeat(2 ** d)
            pairs = self.__interpolation(pairs, coords, d).reshape(-1, 2)
        return self.__interpolation(pairs, rCoords[:, 0], 0)

    def __interpolation(self, pairs, coords, d):
        heightStretch = pairs[:, 1] - pairs[:, 0]
        return self.__warp[d](coords) * heightStretch + pairs[:, 0]

    # bottleneck: takes a lot of time for higher dims
    def findBounds(self, fCoords):
        bCoords = (fCoords * [[a] for a in self.amp[:len(fCoords)]]).astype(np.float32)  # unitized coords
        lowerIndex = np.floor(bCoords).astype(np.uint16)
        rCoords = bCoords - lowerIndex  # relative unitized coords [0, 1]
        # bounding box indexes for the coords
        bIndex = (lowerIndex + np.array(findCorners(len(bCoords)))[..., None]).transpose((1, 0, 2))
        bIndex %= [[[f]] for f in self.mFrequency[:len(bIndex)]]  # wrapping indices under the valid range
        return bIndex[::-1], rCoords

    def findFab(self, bIndex: "np.ndarray"):
        bFab = bIndex.min((1, 2)), bIndex.max((1, 2))  # noqa
        return self.__prng.shaped((bFab[1] - bFab[0]) + 1, bFab[0], dtype=np.float32)

    def applyRange(self, noise):
        return noise * (self.range[1] - self.range[0]) + self.range[0]

    @staticmethod
    def formatCoords(coords: tuple) -> tuple["np.ndarray[np.float32]", tuple[int]]:
        coords = np.array(coords, dtype=np.float32)
        shape = coords.shape
        coords = coords.reshape(len(coords), -1)
        return coords.__abs__(), shape[1:]

    @staticmethod
    def __getFrequency(frequency):
        if isinstance(frequency, int): frequency = (frequency,)
        assert isinstance(frequency, tuple) and all(f > 1 and isinstance(f, int) for f in frequency), \
            "param 'frequency' must be 'int' > 1 or 'tuple' of 'int' > 1 or 'None' for default 8"
        frequency = NTuple(frequency)
        return frequency

    @staticmethod
    def __getWaveLength(waveLength):
        if isinstance(waveLength, (int, float)): waveLength = (waveLength,)
        assert isinstance(waveLength, tuple) and all(w > 0 and isinstance(w, (int, float)) for w in waveLength), \
            "param 'waveLength' must be 'float'('int') > 0 or 'tuple' of 'float'('int') > 0 or 'None' for default 128"
        waveLength = NTuple(waveLength)
        return waveLength

    @staticmethod
    def __getWarp(warp):
        if isinstance(warp, Warp): warp = (warp,)
        assert isinstance(warp, tuple) and all(isinstance(w, Warp) for w in warp), \
            "param 'warp' must be 'selectionTools.Warp' or a 'tuple' of 'selectionTools.Warp' or" \
            "'None' for default 'selectionTools.Warp.improved()'"
        warp = NTuple(warp)
        return warp

    @staticmethod
    def __getRange(_range):
        assert len(_range) == 2 and isinstance(_range[0], (int, float)) and isinstance(_range[1], (int, float)), \
            "param '_range' must be a tuple of two 'float'('int')"
        return _range
