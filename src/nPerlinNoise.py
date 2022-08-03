from typing import Union

from .nPerlin import NPerlin
from .tools import RefNDArray


class NPerlinNoise(NPerlin):
    @property
    def hmax(self):
        return self.__HMAX

    def __init__(self,
                 frequency: Union[int, tuple] = None,
                 seed: int = None,
                 waveLength: Union[float, tuple] = None,
                 _range: tuple[float, float] = None,
                 octaves: int = None,
                 lacunarity: int = None,
                 persistence: float = None):
        """
        todo: documentation required
        :param frequency:
        :param seed:
        :param waveLength:
        :param _range:
        :param octaves:
        :param lacunarity:
        :param persistence:
        """
        if lacunarity is None: lacunarity = 2
        if persistence is None: persistence = 0.5
        if octaves is None: octaves = 8  # todo: diff octaves for diff dims
        assert isinstance(octaves, int) and 1 <= octaves <= 8
        assert isinstance(lacunarity, int)
        assert isinstance(persistence, (int, float)) and 0 < persistence <= 1
        self._octaves = octaves
        self._lacunarity = lacunarity
        self._persistence = persistence
        super(NPerlinNoise, self).__init__(frequency, seed, waveLength, _range)

        self.__HMAX = (1 - self._persistence ** self._octaves) / (1 - self._persistence) if self._persistence != 1 \
            else self._octaves
        self.__AMPS = [self._persistence ** i / self.__HMAX for i in range(self._octaves)]

    def __call__(self, *coords, checkFormat=True):
        """
        todo: documentation required
        :param coords:
        :param checkFormat:
        :return:
        """
        coords = RefNDArray(coords, dep_warn=True)
        h = super(NPerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self.__AMPS[0]
        for i in range(1, self._octaves):
            coords *= self._lacunarity
            h += super(NPerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self.__AMPS[i]
        return h
