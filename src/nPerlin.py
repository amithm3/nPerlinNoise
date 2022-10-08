from typing import Union

import numpy as np

from .tools import NTuple, NPrng, iterable, maxLen, findCorners
from .selectionTools import Warp


class NPerlin:
    @property
    def seed(self):
        return self.__prng.seed()

    def setSeed(self, val):
        self.__prng.seed(val)

    @property
    def frequency(self):
        return NTuple(*self.__frequency)

    def setFrequency(self, val):
        self.__frequency = self.__getFrequency(val)
        self.__amp = self.__calcAmp()

    @property
    def waveLength(self):
        return self.__waveLength

    def setWaveLength(self, val):
        self.__waveLength = self.__getWaveLength(val)
        self.__amp = self.__calcAmp()

    @property
    def warp(self):
        return self.__warp

    def setWarp(self, val):
        self.__warp = self.__getWarp(val)

    @property
    def range(self):
        return self.__range

    def setRange(self, val):
        self.__range, self.__rangeMul = self.__getRange(val)

    def fabric(self, shape, off=None):
        return self.__prng.shaped(shape, off)

    def setFWM(self, val):
        self.__fwm = val

    def __repr__(self):
        return f"<seed:{self.seed} freq:{self.frequency} wLen:{self.waveLength} warp:{self.warp} range:{self.range}>"

    def __init__(self,
                 seed: int = None,
                 frequency: Union[int, tuple[int, ...]] = None,
                 waveLength: Union[float, tuple[float]] = None,
                 warp: Union['Warp', tuple['Warp']] = None,
                 _range: tuple[float, float] = None,
                 *,
                 fwm: int = 1):
        """
        :param seed: seed for random values, default random value
        :param frequency: number of random values in one unit respect to dimension, default 8
        :param waveLength: length of one unit respect to dimension, default 128
        :param warp: the interpolation function used between random value nodes, default selectionTools.Warp.improved()
        :param _range: bound for noise values, output will be within the give range, default (0, 1)
        """
        if frequency is None: frequency = 8
        if waveLength is None: waveLength = 128
        if warp is None: warp = Warp.improved()
        if _range is None: _range = (0, 1)

        self.__fwm = fwm
        self.__frequency = self.__getFrequency(frequency)
        self.__waveLength = self.__getWaveLength(waveLength)
        self.__prng = NPrng(seed)  # matrix of random value nodes
        self.__warp = self.__getWarp(warp)
        self.__range, self.__rangeMul = self.__getRange(_range)
        self.__amp = self.__calcAmp()  # length between any 2 consecutive random values

    # todo: implement checkFormat
    def __call__(self, *coords, checkFormat: bool = True):
        if len(coords) == 0: coords = (0,)
        fCoords = self.formatCoords([np.ravel(coo) for coo in coords])
        bIndex, bCoords = self.findBounds(fCoords)
        fab = self.findFab(bIndex)
        bSpace = fab[tuple(bIndex)]
        return self.applyRange(self.bNoise(bSpace.T, bCoords.T))

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

    def findBounds(self, fCoords):
        bCoords = fCoords[::-1] / self.__amp  # unitized coords
        lowerIndex = np.floor(bCoords).astype(np.uint16)
        bCoords -= lowerIndex  # relative unitized coords [0, 1]
        # bounding box indexes for the coords
        bIndex = (lowerIndex + np.array(findCorners(len(bCoords)))[..., None]).transpose((1, 0, 2))
        bIndex %= self.__frequency  # wrapping indices under the valid range
        return bIndex, bCoords[::-1]

    def findFab(self, bIndex: "np.ndarray"):
        bFab = bIndex.min((1, 2)), bIndex.max((1, 2))
        return self.__prng.shaped((bFab[1] - bFab[0]) + 1, bFab[0])

    def applyRange(self, noise):
        return noise * self.__rangeMul + self.range[0]

    def __calcAmp(self):
        return NTuple(*[w / f for w, f in zip(self.__waveLength, self.__frequency)])

    @staticmethod
    def formatCoords(coords: list) -> "np.ndarray":
        """
        handles fancy lengths, safety of coords, proper formatting
        todo: docs
        :param coords:
        :return:
        """
        # the highest length amongst the elements of coords
        maxLength = maxLen(coords, key=lambda x: x if iterable(x) else (x,))
        coords = list(coords)
        # pre-allocation of required array
        __coords = np.zeros((len(coords), maxLength), dtype=np.float32)
        for d in range(len(coords)):
            if not iterable(coords[d]): coords[d] = [coords[d]]  # convert non-iterable to iterable of length 1
            stretch, left = divmod(maxLength, max(1, len(coords[d])))
            """
            to make all the elements of coords of equal(=maxLength) length
            stretch: each sub-element will be repeated 'stretch' times
            left: last element will be repeated 'left' times to fill the remaining gap
            """
            __coords[d, :maxLength - left] = np.repeat(coords[d], stretch)
            __coords[d, maxLength - left:] = np.repeat(coords[d][-1], left)
        assert (depth := len(__coords.shape)) == 2, \
            f"coords must be a 2D Matrix of nth row representing nth dimension, but given Matrix of depth {depth}"
        return __coords.__abs__()

    def __getFrequency(self, frequency):
        if isinstance(frequency, int): frequency = (frequency,)
        assert isinstance(frequency, tuple) and all(f > 1 and isinstance(f, int) for f in frequency), \
            "param 'frequency' must be 'int' > 1 or 'tuple' of 'int' > 1 or 'None' for default 8"
        frequency = NTuple(*[f * self.__fwm for f in frequency])
        return frequency

    def __getWaveLength(self, waveLength):
        if isinstance(waveLength, (int, float)): waveLength = (waveLength,)
        assert isinstance(waveLength, tuple) and all(w > 0 and isinstance(w, (int, float)) for w in waveLength), \
            "param 'waveLength' must be 'float'('int') > 0 or 'tuple' of 'float'('int') > 0 or 'None' for default 128"
        waveLength = NTuple(*[w * self.__fwm for w in waveLength])
        return waveLength

    @staticmethod
    def __getWarp(warp):
        if isinstance(warp, Warp): warp = (warp,)
        assert isinstance(warp, tuple) and all(isinstance(w, Warp) for w in warp), \
            "param 'warp' must be 'selectionTools.Warp' or a 'tuple' of 'selectionTools.Warp' or" \
            "'None' for default 'selectionTools.Warp.improved()'"
        warp = NTuple(*warp)
        return warp

    @staticmethod
    def __getRange(_range):
        assert len(_range) == 2 and isinstance(_range[0], (int, float)) and isinstance(_range[1], (int, float)), \
            "param '_range' must be a tuple of two 'float'('int')"
        _rangeMul = _range[1] - _range[0]
        return _range, _rangeMul
