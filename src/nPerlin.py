import numpy as np
import warnings
from typing import Union

from .tools import RefNDArray, findCorners, iterable, maxLen, Warp, PRNG, Fabric


class NMeta(type):
    def __call__(cls, *args, dims, warp: Union['Warp', list['Warp']] = None, **kwargs):
        obj = cls.__new__(cls, *args, dims=dims, warp=warp, **kwargs)  # noqa
        obj.__init__(*args, **kwargs)
        return obj


class NPerlin(metaclass=NMeta):
    import numpy as __np
    __rnd = __np.random  # todo: make to self
    __DIMS: int  # max dimensional depth
    __BIND: '__np.ndarray'  # unit bounding box of n-dimension
    __WARP: tuple['Warp']  # interpolation function

    @property
    def dims(self):
        return self.__DIMS

    @property
    def seed(self):
        return self.__SEED

    @property
    def frequency(self):
        return self.__FREQUENCY

    @property
    def waveLength(self):
        return self.__WAVE_LENGTH

    @property
    def fabric(self):
        return self.__fabric.copy()

    def __new__(cls, *args, dims, warp: Union['Warp', list['Warp']] = None, **kwargs):
        if warp is None: warp = Warp.improved()
        if not isinstance(warp, list): warp = [warp] * dims
        assert isinstance(dims, int) and dims > 0
        assert isinstance(warp, list) and len(warp) == dims
        obj = super(NPerlin, cls).__new__(cls)
        obj.__DIMS = dims
        obj.__WARP = warp
        obj.__BIND = cls.__np.array(findCorners(obj.__DIMS))[:, :, None]
        return obj

    def __init__(self,
                 frequency: Union[int, tuple[int, ...]] = None,
                 seed: int = None,
                 waveLength: Union[float, tuple[float]] = None,
                 _range: tuple[float, float] = None):
        """
        :param frequency: number(s) of random values in one unit, default 8
        :param seed: seed for random values, default random value
        :param waveLength: length(s) of one unit, default 128
        :param _range: bound for noise values, will be within the give range, default (0, 1)
        """
        if frequency is None: frequency = 8
        assert isinstance(frequency, (int, tuple)), \
            "param 'frequency' must be 'int' > 1 or 'tuple' of 'int' > 1 of length dims or 'None' for value 8"
        if isinstance(frequency, int): frequency = (frequency,) * self.__DIMS
        assert all(f > 1 and isinstance(f, int) for f in frequency) and len(frequency) == self.__DIMS, \
            "param 'frequency' must be 'int' > 1 or 'tuple' of 'int' > 1 of length dims or 'None' for value 8"

        if seed is None: seed = 2 ** 16 + self.__rnd.randint(-(2 ** 16), 2 ** 16)
        assert (isinstance(seed, int) and 2 ** 32 > seed >= 0), \
            "param 'seed' must be +ve 'int' (or zero) less than 2^32 or 'None' for random seed"

        if waveLength is None: waveLength = 128
        if isinstance(waveLength, (int, float)): waveLength = (waveLength,) * self.__DIMS
        assert isinstance(waveLength, tuple) and all(w > 0 and isinstance(w, (int, float)) for w in waveLength) and \
               len(waveLength) == self.__DIMS, \
            "param 'waveLength' must be +ve 'float'('int') or " \
            "'tuple' of +ve 'float'('int) of length dims or 'None' for value 100"  # noqa

        if _range is None: _range = (0, 1)
        assert len(_range) == 2 and isinstance(_range[0], (int, float)) and isinstance(_range[1], (int, float)), \
            "param '_range' must be a tuple of two 'float'('int')"
        self.__range = _range
        self.__rangeMul = self.__range[1] - self.__range[0]

        self.__SEED = seed
        self.__rnd.seed(self.__SEED)
        self.__FREQUENCY = frequency
        self.__WAVE_LENGTH = waveLength

        # matrix of random value nodes
        prng = PRNG(self.__SEED)
        self.__fabric = self.loopifyArr(prng(self.__FREQUENCY).astype(self.__np.float32))
        # length between any 2 consecutive random values
        self.__AMP = [w / (f - 1) for w, f in zip(self.__WAVE_LENGTH, self.__FREQUENCY + np.uint(1))]

    def __call__(self, *coords, checkFormat: bool = True):
        """
        performs pre-processing of coords & generates support data for creating noise values,
        calls interpolation with relevant data

        usage:
            __noise((1, 2, 3, 4), (0, 0, 0, 0), (1, 1, 1, 1), ...)
            1st iterable -> 1st dimension,
            2nd iterable -> 2nd dimension,
            3rd iterable -> 3rd dimension,
            ...,
            nth iterable -> nth dimension
            length of each iterable is same

            if checkFormat is 'True', coords can use fancy lengths, ensures safety of coords and proper formatting:
                __noise((1, 2, 3, 4), 1) -> __noise((1, 2, 3, 4), (1, 1, 1, 1))
                __noise((1, 2, 3, 4),) -> __noise((1, 2, 3, 4), (0, 0, 0, 0), (0, 0, 0, 0), ...)
                __noise((1, 2, 3, 4), (1, 2)) -> __noise((1, 2, 3, 4), (1, 1, 2, 2))
                __noise((1, 2, 3, 4, 5), (1, 2, 3)) -> __noise((1, 2, 3, 4, 5), (1, 2, 3, 3, 3))

        :param coords: point(s) to generate noise value(s) at
        :param checkFormat: if True(default) will coords can use fancy lengths, ensures safety of coords and proper formatting,
        else will skip
        :return: noise value(s) at coords
        """
        return self.__noise(*coords, checkFormat=checkFormat) * self.__rangeMul + self.__range[0]

    def __noise(self, *coords, checkFormat: bool = True):
        """
        performs pre-processing of coords & generates support data for creating noise values,
        calls interpolation with relevant data

        usage:
            __noise((1, 2, 3, 4), (0, 0, 0, 0), (1, 1, 1, 1), ...)
            1st iterable -> 1st dimension,
            2nd iterable -> 2nd dimension,
            3rd iterable -> 3rd dimension,
            ...,
            nth iterable -> nth dimension
            length of each iterable is same

            if checkFormat is 'True', coords can use fancy lengths, ensures safety of coords and proper formatting:
                __noise((1, 2, 3, 4), 1) -> __noise((1, 2, 3, 4), (1, 1, 1, 1))
                __noise((1, 2, 3, 4),) -> __noise((1, 2, 3, 4), (0, 0, 0, 0), (0, 0, 0, 0), ...)
                __noise((1, 2, 3, 4), (1, 2)) -> __noise((1, 2, 3, 4), (1, 1, 2, 2))
                __noise((1, 2, 3, 4, 5), (1, 2, 3)) -> __noise((1, 2, 3, 4, 5), (1, 2, 3, 3, 3))

        :param coords: point(s) to generate noise value(s) at
        :param checkFormat: if True(default) will coords can use fancy lengths, ensures safety of coords and proper formatting,
        else will skip
        :return: noise value(s) at coords
        """
        if checkFormat:  # handles fancy lengths, safety of coords, proper formatting
            assert 0 < (length := len(coords)) <= self.__DIMS, \
                f"coords expected maximum of {self.__DIMS} argument(s) and minimum of 1 argument, " \
                f"but {length} arguments given"
            coords = [*coords, *[[0]] * (self.__DIMS - length)]  # minimal coords of length dims
            # the highest length amongst the elements of coords
            maxLength = maxLen(coords, key=lambda x: x if iterable(x) else (x,))
            # pre-allocation of required memory
            __coords = self.__np.zeros((self.__DIMS, maxLength), dtype=self.__np.float32)
            for d in range(self.__DIMS):
                if not iterable(coords[d]): coords[d] = [coords[d]]  # convert non-iterable to iterable of length 1
                stretch, left = divmod(maxLength, max(1, len(coords[d])))
                """
                to make all the elements of coords of equal(=maxLength) length
                stretch: each sub-element will be repeated 'stretch' times
                left: last element will be repeated 'left' times to fill the remaining gap
                """
                __coords[d, :maxLength - left] = self.__np.repeat(coords[d], stretch)
                __coords[d, maxLength - left:] = self.__np.repeat(coords[d][-1], left)
            coords = __coords
        else:
            # assumes user has given coords in desired format
            assert (length := len(coords)) == self.__DIMS, \
                f"coords expected {self.__DIMS} arguments(s), but {length} arguments given"
            warnings.warn(
                "Using 'checkFormat' as 'False' is unsafe"
                "\n     Can't guarantee safety of arguments(*coords),"
                "\n     Can't use fancy coords,"
                "\n     May face performance uncertainty(can be slower or faster for different cases),"
                "\n     Unexpected results and/or errors may be encountered"
                "\n Use only if you know what it does",
                RuntimeWarning)
        coords = coords.__abs__()[::-1]
        coords = RefNDArray(coords)  # Pseudo-ndarray-like object
        assert (depth := len(self.__np.shape(coords))) == 2, \
            f"coords must be a 2D Matrix, but given Matrix of depth {depth}"
        coords /= self.__AMP  # unitized coords
        lowerIndex = self.__np.floor(coords).astype(self.__np.uint16)
        warpedLowerIndex = lowerIndex % self.__np.array(self.__FREQUENCY)[None].transpose()

        # bounding index & space where the coords exists within fabric
        bIndex = (warpedLowerIndex + self.__BIND).transpose()
        bSpace = self.__fabric[tuple(bIndex[:, d] for d in range(self.__DIMS))]
        bSpace = bSpace.reshape((-1, *[2] * self.__DIMS))
        coords -= lowerIndex  # relative unitized coords

        return self.__interpolation(bSpace, coords, self.__DIMS)

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
            return (self.__WARP[d - 1](relativeCoord) * heightStretch + bSpace[:, 0]).ravel()
        bSpace = bSpace.reshape([-1, *bSpace.shape[2:]])
        bSpace = self.__interpolation(bSpace, relativeCoord[1:].repeat(2, axis=1), d - 1)
        bSpace = bSpace.reshape((-1, 2))

        return self.__interpolation(bSpace, relativeCoord[0], d)

    @staticmethod
    def loopifyArr(arr: np.ndarray):
        """
        todo: documentation required
        :param arr:
        :return:
        """
        for si in range(len(arr.shape)): arr = np.concatenate((arr, np.expand_dims(arr.take(0, si), si)), axis=si)
        return arr
