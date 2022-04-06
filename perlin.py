from typing import *

import numpy as np

from nPerlin import NPerlin


class Perlin(NPerlin):
    @property
    def range(self):
        return self.__range

    def __init__(self, dims: int,
                 frequency: Union[int, tuple] = None,
                 seed: int = None,
                 waveLength: int = None,
                 _range: tuple[float, float] = None):
        if _range is None: _range = (0, 1)
        assert len(_range) == 2 and isinstance(_range[0], (int, float)) and isinstance(_range[1], (int, float))
        self.__range = _range
        self.__rangeMul = self.__range[1] - self.__range[0]
        super(Perlin, self).__init__(frequency, seed, waveLength)

    def __new__(cls, dims, *args, **kwargs):
        assert isinstance(dims, int) and dims > 0
        cls.__DIMENSION__ = dims
        return super(Perlin, cls).__new__(cls, *args, **kwargs)

    def __call__(self, *coords, checkFormat=True):
        return super(Perlin, self).__call__(*coords, checkFormat=checkFormat) * self.__rangeMul + self.__range[0]


class PerlinNoise(Perlin):
    def __init__(self, dims: int,
                 octaves: int = None,
                 lacunarity: int = None,
                 persistence: float = None,
                 frequency: Union[int, tuple] = None,
                 seed: int = None,
                 waveLength: int = None,
                 _range: tuple[float, float] = None):
        if lacunarity is None: lacunarity = 2
        if persistence is None: persistence = 0.5
        if octaves is None: octaves = 4
        assert isinstance(octaves, int) and 1 <= octaves <= 8
        assert isinstance(lacunarity, int)
        assert isinstance(persistence, (int, float)) and 0 < persistence <= 1
        self._octaves = octaves
        self._lacunarity = lacunarity
        self._persistence = persistence
        super(PerlinNoise, self).__init__(dims, frequency, seed, waveLength, _range)

        self._hMax = (1 - self._persistence ** self._octaves) / (1 - self._persistence) if self._persistence != 1 \
            else self._octaves
        self._amps = [self._persistence ** i / self._hMax for i in range(self._octaves)]

    def __call__(self, *coords, checkFormat=True):
        coords = np.array(coords)
        h = super(PerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self._amps[0]
        for i in range(1, self._octaves):
            coords *= self._lacunarity
            h += super(PerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self._amps[i]

        return h
