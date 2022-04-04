import numpy as np

from nPerlin import NPerlin


class Perlin(NPerlin):
    def __init__(self, dims: int, frequency: int = None, seed: int = None, waveLength: int = None):
        super(Perlin, self).__init__(frequency, seed, waveLength)

    def __new__(cls, dims, *args, **kwargs):
        assert isinstance(dims, int) and dims > 0
        cls.__DIMENSION__ = dims
        return super(Perlin, cls).__new__(cls, *args, **kwargs)


class PerlinNoise(Perlin):
    def __init__(self, dims: int,
                 octaves: int = None,
                 lacunarity: int = None,
                 persistence: float = None,
                 frequency: int = None,
                 seed: int = None,
                 waveLength: int = None):
        if lacunarity is None: lacunarity = 2
        if persistence is None: persistence = 0.5
        if octaves is None: octaves = 8
        assert isinstance(octaves, int) and 1 <= octaves <= 8
        assert isinstance(lacunarity, int)
        assert isinstance(persistence, (int, float)) and 0 <= persistence <= 1
        super(PerlinNoise, self).__init__(dims, frequency, seed, waveLength)
        self._octaves = octaves
        self._lacunarity = lacunarity
        self._persistence = persistence

        self._amps = [self._persistence ** (i + 1) for i in range(self._octaves)]
        self._hMax = self._persistence * (1 - self._persistence ** self._octaves) / (
                    1 - self._persistence) if self._persistence != 1 else 1

    # todo: make faster?
    def __call__(self, *coords, checkFormat=True):
        coords = np.array(coords)
        h = super(PerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self._amps[0]
        for i in range(1, self._octaves):
            coords *= self._lacunarity
            h += super(PerlinNoise, self).__call__(*coords, checkFormat=checkFormat) * self._amps[i]

        return h / self._hMax
