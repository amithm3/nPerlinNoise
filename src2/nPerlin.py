from typing import Union

import numpy as np

from .tools import NTuple, NFabric, Warp


class NPerlin:
    __BIND: 'np.ndarray'  # todo: make this also auto dynamic (=np.array(findCorners(obj.__DIMS))[:, :, None])

    @property
    def seed(self):
        return self.__fabric.seed()

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
        :param seed: seed for random values, default random value
        :param waveLength: length of one unit respect to dimension, default 128
        :param _range: bound for noise values, output will be within the give range, default (0, 1)
        :param warp: the interpolation function used between random value nodes, default Warp.improved()
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

        if isinstance(waveLength, Warp): warp = (warp,)
        assert isinstance(warp, tuple) and all(isinstance(w, Warp) for w in warp)

        assert len(_range) == 2 and isinstance(_range[0], (int, float)) and isinstance(_range[1], (int, float)), \
            "param '_range' must be a tuple of two 'float'('int')"

        self.__frequency = NTuple(*frequency)
        self.__wavelength = NTuple(*waveLength)
        self.__warp = NTuple(*warp)
        self.__range = _range
        self.__rangeMul = self.__range[1] - self.__range[0]

        self.__fabric = NFabric(seed)  # matrix generator of random value nodes
        # length between any 2 consecutive random values
        self.__amp = NTuple(*[w / (f - 1) for w, f in zip(self.__wavelength, self.__frequency)])

    def __noise(self):
        pass  # todo

    @staticmethod
    def loopifyArr(arr: "np.ndarray"):
        """
        todo: documentation required
        :param arr:
        :return:
        """
        for si in range(len(arr.shape)): arr = np.concatenate((arr, np.expand_dims(arr.take(0, si), si)), axis=si)
        return arr
