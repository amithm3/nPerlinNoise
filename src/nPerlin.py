import warnings
from typing import Union

import numpy as np

from .tools import NTuple, NPrng, NFabric, iterable, maxLen, findCorners
from .selectionTools import Warp


class NPerlin:
    # __chunked__ = True
    __chunked__ = False

    @property
    def seed(self):
        return self.__seed

    @property
    def frequency(self):
        return self.__frequency

    @property
    def waveLength(self):
        return self.__wavelength

    @property
    def fabric(self):
        return self.__fabric

    def __repr__(self):
        return f"<seed:{self.seed} freq:{self.frequency} wLen:{self.waveLength}>"

    def __init__(self,
                 frequency: Union[int, tuple[int, ...]] = None,
                 waveLength: Union[float, tuple[float]] = None,
                 warp: Union['Warp', tuple['Warp']] = None,
                 seed: int = None,
                 _range: tuple[float, float] = None):
        """
        :param frequency: number of random values in one unit respect to dimension, default 8
        :param waveLength: length of one unit respect to dimension, default 128
        :param warp: the interpolation function used between random value nodes, default selectionTools.Warp.improved()
        :param seed: seed for random values, default random value
        :param _range: bound for noise values, output will be within the give range, default (0, 1)
        """
        if frequency is None: frequency = 8
        if waveLength is None: waveLength = 128
        if _range is None: _range = (0, 1)
        if warp is None: warp = Warp.improved()

        if isinstance(frequency, int): frequency = (frequency,)
        assert isinstance(frequency, tuple) and all(f > 1 and isinstance(f, int) for f in frequency), \
            "param 'frequency' must be 'int' > 1 or 'tuple' of 'int' > 1 or 'None' for default 8"

        if isinstance(waveLength, (int, float)): waveLength = (waveLength,)
        assert isinstance(waveLength, tuple) and all(w > 0 and isinstance(w, (int, float)) for w in waveLength), \
            "param 'waveLength' must be 'float'('int') > 0 or 'tuple' of 'float'('int') > 0 or 'None' for default 128"

        if isinstance(warp, Warp): warp = (warp,)
        assert isinstance(warp, tuple) and all(isinstance(w, Warp) for w in warp), \
            "param 'warp' must be 'selectionTools.Warp' or a 'tuple' of 'selectionTools.Warp' or" \
            "'None' for default 'selectionTools.Warp.improved()'"

        assert len(_range) == 2 and isinstance(_range[0], (int, float)) and isinstance(_range[1], (int, float)), \
            "param '_range' must be a tuple of two 'float'('int')"

        self.__frequency = NTuple(*frequency if not self.__chunked__ else [f * self.__chunked__ for f in frequency])
        self.__wavelength = NTuple(*waveLength if not self.__chunked__ else [w * self.__chunked__ for w in waveLength])
        self.__warp = NTuple(*warp)
        self.__range = _range
        self.__rangeMul = self.__range[1] - self.__range[0]

        # matrix generator of random value nodes
        if not self.__chunked__:
            fab = self.__fabric = NFabric(seed)
        else:
            self.__fabric = self.loopifyArr((fab := NPrng(seed)).shaped(self.__frequency).astype(np.float32))
        self.__seed = fab.seed()
        # length between any 2 consecutive random values
        self.__amp = NTuple(*[w / (f - 1) for w, f in zip(self.__wavelength, self.__frequency)])

    def __call__(self, *coords, checkFormat: bool = True):
        if len(coords) == 0: coords = (0,)
        return self.__noise([np.ravel(coo) for coo in coords], checkFormat).reshape(np.shape(coords[0]))

    # todo: make full support for fancy coords
    def __noise(self, coords: list["np.ndarray"], checkFormat: bool = True):
        if checkFormat:  # handles fancy lengths, safety of coords, proper formatting
            if self.__chunked__:
                assert len(coords) <= len(self.__frequency), \
                    f"too many dimensions for coords: noise fabric is {len(self.__frequency)}-dimensional, " \
                    f"but {len(coords)} were indexed.\n" \
                    f"You are seeing this Error because checkFormat and NPerlin.__chunked__ are enabled."
            # the highest length amongst the elements of coords
            maxLength = maxLen(coords, key=lambda x: x if iterable(x) else (x,))
            coords = list(coords)
            # pre-allocation of required memory
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
            coords = __coords
        else:
            # assumes user has given coords in desired format
            warnings.warn(
                "Using 'checkFormat' as 'False' is unsafe"
                "\n    Can't guarantee safety of arguments(*coords),"
                "\n    Can't use fancy coords,"
                "\n    May face performance uncertainty(can be slower or faster for different cases),"
                "\n    Unexpected results and/or errors may be encountered"
                "\n Use only if you know what it does",
                RuntimeWarning
            )
        coords = coords.__abs__()[::-1]
        assert (depth := len(coords.shape)) == 2, \
            f"coords must be a 2D Matrix of nth row representing nth dimension, but given Matrix of depth {depth}"
        coords /= self.__amp  # unitized coords
        lowerIndex = np.floor(coords).astype(np.uint16)
        coords -= lowerIndex  # relative unitized coords

        # wrapping in-valid index under the valid range
        if self.__chunked__: lowerIndex = lowerIndex % np.array(self.__frequency)[None].transpose()
        # bounding index & space where the coords exists within fabric
        bIndex = (lowerIndex + np.array(findCorners(len(coords)))[..., None]).transpose()
        bSpace = self.__fabric[tuple(bIndex[:, d] for d in range(len(coords)))].astype(np.float32)
        bSpace = bSpace.reshape((-1, *[2] * len(coords)))

        return self.__interpolation(bSpace, coords, len(coords))

    def __interpolation(self, bSpace, relativeCoord, d):
        """
        todo: documentation required
        :param bSpace:
        :param relativeCoord:
        :param d:
        :return:
        """
        if len(bSpace.shape) == 2:
            heightStretch = bSpace[:, 1] - bSpace[:, 0]
            return (self.__warp[d - 1](relativeCoord) * heightStretch + bSpace[:, 0]).ravel()
        bSpace = bSpace.reshape([-1, *bSpace.shape[2:]])
        bSpace = self.__interpolation(bSpace, relativeCoord[1:].repeat(2, axis=1), d - 1)
        bSpace = bSpace.reshape((-1, 2))

        return self.__interpolation(bSpace, relativeCoord[0], d)

    @staticmethod
    def loopifyArr(arr: "np.ndarray"):
        """
        todo: documentation required
        :param arr:
        :return:
        """
        for si in range(len(arr.shape)): arr = np.concatenate((arr, np.expand_dims(arr.take(0, si), si)), axis=si)
        return arr
