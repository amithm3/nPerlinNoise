import collections
from typing import Union

import numpy as np

from .tools import NTuple, NPrng, iterable, maxLen, findCorners
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

    # multiplier for converting coords into fabric region based on frequency and wavelength
    @property
    def amp(self) -> "NTuple[float]":
        mF, mW = self.mFrequency, self.mWaveLength
        length = max(len(mF), len(mW))
        return NTuple(f / w for f, w in zip(mF[:length], mW[:length]))

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

    # todo: implement checkFormat
    def __call__(self, *coords: "collections.Iterable", _format: str = "fill" or "expand" or "none"):
        fCoords, shape = self.formatCoords(coords, _format)
        bIndex, bCoords = self.findBounds(fCoords)
        fab = self.findFab(bIndex)
        bSpace = fab[tuple(bIndex)]
        return self.applyRange(self.bNoise(bSpace.T, bCoords.T)).reshape(shape)

    def bNoise(self, bSpace, bCoords):
        dims = bCoords.shape[1]
        pairs = bSpace.reshape(-1, 2)
        # collapse dimensions
        for d in range(dims - 1):
            coords = bCoords[:, d].repeat(2 ** (dims - 1 - d))
            pairs = self.__interpolation(pairs, coords, d).reshape(-1, 2)
        return self.__interpolation(pairs, bCoords[:, -1], -1)

    def __interpolation(self, pairs, coords, d):
        heightStretch = pairs[:, 1] - pairs[:, 0]
        return self.__warp[d](coords) * heightStretch + pairs[:, 0]

    # bottleneck: takes a lot of time for higher dims
    def findBounds(self, fCoords):
        bCoords = (fCoords[::-1] * [[a] for a in self.amp[:len(fCoords)]]).astype(np.float32)  # unitized coords
        lowerIndex = np.floor(bCoords).astype(np.uint16)
        bCoords -= lowerIndex  # relative unitized coords [0, 1]
        # bounding box indexes for the coords
        bIndex = (lowerIndex + np.array(findCorners(len(bCoords)))[..., None]).transpose((1, 0, 2))
        bIndex %= [[[f]] for f in self.mFrequency[:len(bIndex)]]  # wrapping indices under the valid range
        return bIndex, bCoords[::-1]

    def findFab(self, bIndex: "np.ndarray"):
        bFab = bIndex.min((1, 2)), bIndex.max((1, 2))  # noqa
        return self.__prng.shaped((bFab[1] - bFab[0]) + 1, bFab[0], dtype=np.float32)

    def applyRange(self, noise):
        return noise * (self.range[1] - self.range[0]) + self.range[0]

    @staticmethod
    def formatCoords(coords, _format: str = "fill" or "expand" or "none") -> tuple["np.ndarray", tuple[int, ...]]:
        """
        todo: docs
        :param coords:
        :param _format:
        :return:
        """
        # the highest length amongst the elements of coords
        maxLength = maxLen(coords, key=lambda x: x if iterable(x) else (x,))
        if _format == "fill":
            # pre-allocation of required array
            __coords = np.zeros((len(coords), maxLength), dtype=np.float32)
            for d in range(len(coords)):
                if not iterable(coords[d]): coords[d] = [coords[d]]  # convert non-iterable to iterable of length 1
                stretch, left = divmod(maxLength, max(1, len(coords[d])))
                __coords[d, :maxLength - left], __coords[d, maxLength - left:] = \
                    np.repeat(coords[d], stretch), np.repeat(coords[d][-1], left)
            coords = __coords
        elif _format == "expand":
            for d in range(len(coords)):
                if not iterable(coords[d]): coords[d] = [coords[d]]  # convert non-iterable to iterable of length 1
            __coords = (coords := np.array(np.meshgrid(*coords), dtype=np.float32)).reshape(len(coords), -1)
        elif _format == "none":
            __coords = (coords := np.array(coords, dtype=np.float32)).reshape(len(coords), -1)
        else:
            raise ValueError(f"param _format can be 'fill' or 'expand' or 'none', not {_format}")
        assert (depth := len(__coords.shape)) == 2, \
            f"coords must be a 2D Matrix of nth row representing nth dimension, but given Matrix of depth {depth}"
        return __coords.__abs__(), coords.shape[1:]

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
