import collections
from typing import Union

import numpy as np

from .nPerlin import NPerlin


class Noise(NPerlin):
    @property
    def octaves(self) -> int:
        return self.__octaves

    def setOctaves(self, octaves: int):
        self.__octaves = self.__getOctaves(octaves)
        self.setFwm(self.__octaves)

    @property
    def persistence(self) -> float:
        return self.__persistence

    def setPersistence(self, persistence: float):
        self.__persistence = self.__getPersistence(persistence)

    @property
    def lacunarity(self) -> float:
        return self.__lacunarity

    def setLacunarity(self, lacunarity: float):
        self.__lacunarity = self.__getLacunarity(lacunarity)

    def __repr__(self):
        return super(Noise, self).__repr__()[:-1] + f' oct={self.octaves} per={self.persistence} lac={self.lacunarity}>'

    # todo: docs
    @property
    def weight(self):
        hmax = \
            (1 - self.persistence ** self.octaves) / (1 - self.persistence) if self.persistence != 1 else self.octaves
        return [self.persistence ** i / hmax for i in range(self.octaves)]

    def __init__(self, *args,
                 octaves: int = 8,  # todo: diff octaves for diff dims
                 persistence: float = 0.5,
                 lacunarity: float = 2.0,
                 **kwargs):
        """
        todo: docs
        :param octaves: number(s) of additive overlapping noise wave(s)
        :param lacunarity: frequency multiplier for successive noise octave
        :param persistence: amplitude modulator for successive noise octave
        """
        self.__octaves = self.__getOctaves(octaves)
        self.__persistence = self.__getPersistence(persistence)
        self.__lacunarity = self.__getLacunarity(lacunarity)
        super(Noise, self).__init__(*args, **kwargs, fwm=self.__octaves)

    def _noise(self, fCoords):
        fCoords = np.concatenate([fCoords] + [fCoords := fCoords * self.__lacunarity for _ in range(1, self.__octaves)],
                                 axis=1)
        h = super(Noise, self)._noise(fCoords).reshape(self.__octaves, -1)
        h *= [[w] for w in self.weight]
        return h.sum(axis=0)

    @staticmethod
    def __getOctaves(octaves):
        assert isinstance(octaves, int) and 1 <= octaves <= 8
        return octaves

    @staticmethod
    def __getPersistence(persistence):
        assert isinstance(persistence, (int, float)) and 0 < persistence <= 1
        return persistence

    @staticmethod
    def __getLacunarity(lacunarity):
        assert isinstance(lacunarity, (int, float)) and 1 <= lacunarity
        return lacunarity
