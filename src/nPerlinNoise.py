from typing import Union

from .nPerlin import NPerlin
from .tools import RefNDArray


class NPerlinNoise(NPerlin):
    def __init__(self,
                 frequency: Union[int, tuple] = None,
                 seed: int = None,
                 waveLength: Union[float, tuple] = None,
                 _range: tuple[float, float] = None,
                 octaves: int = None,
                 lacunarity: float = None,
                 persistence: float = None):
        """
        :param frequency: number(s) of random values in one unit, default 8
        :param seed: seed for random values, default random value
        :param waveLength: length(s) of one unit, default 128
        :param _range: bound for noise values, will be within the give range, default (0, 1)
        :param octaves: number(s) of additive overlapping noise wave(s), default 8
        :param lacunarity: frequency multiplier for successive noise octave, default 2
        :param persistence: amplitude modulator for successive noise octave, default 0.5
        """
        if frequency is None: frequency = 8
        assert isinstance(frequency, (int, tuple)), \
            "param 'frequency' must be 'int' > 1 or 'tuple' of 'int' > 1 of length dims or 'None' for value 8"
        if isinstance(frequency, int): frequency = (frequency,) * self.dims
        assert all(f > 1 and isinstance(f, int) for f in frequency) and len(frequency) == self.dims, \
            "param 'frequency' must be 'int' > 1 or 'tuple' of 'int' > 1 of length dims or 'None' for value 8"

        if waveLength is None: waveLength = 128
        if isinstance(waveLength, (int, float)): waveLength = (waveLength,) * self.dims
        assert isinstance(waveLength, tuple) and all(w > 0 and isinstance(w, (int, float)) for w in waveLength) and \
               len(waveLength) == self.dims, \
            "param 'waveLength' must be +ve 'float'('int') or " \
            "'tuple' of +ve 'float'('int) of length dims or 'None' for value 100"  # noqa

        if lacunarity is None: lacunarity = 2
        if persistence is None: persistence = 0.5
        if octaves is None: octaves = 8  # todo: diff octaves for diff dims
        assert isinstance(octaves, int) and 1 <= octaves <= 8
        assert isinstance(persistence, (int, float)) and 0 < persistence <= 1
        self._octaves = octaves
        self._lacunarity = lacunarity
        self._persistence = persistence
        super(NPerlinNoise, self).__init__(
            tuple([f * self._lacunarity * self._octaves for f in frequency]), seed,
            tuple([w * self._lacunarity * self._octaves for w in waveLength]), _range
        )

        self.__HMAX = (1 - self._persistence ** self._octaves) / (1 - self._persistence) if self._persistence != 1 \
            else self._octaves
        self.__AMPS = [self._persistence ** i / self.__HMAX for i in range(self._octaves)][::-1]

    def __call__(self, *coords, checkFormat=True):
        """
        todo: documentation required
        :param coords:
        :param checkFormat:
        :return:
        """
        coords = RefNDArray(coords, dep_warn=True) * self._lacunarity ** (self._octaves - 1)
        h = super(NPerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self.__AMPS[0]
        for i in range(1, self._octaves):
            coords /= self._lacunarity
            h += super(NPerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self.__AMPS[i]
        return h
