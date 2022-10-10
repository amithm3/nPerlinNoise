import collections

from .nPerlin import NPerlin


class Noise(NPerlin):
    @property
    def octaves(self) -> int:
        return self.__octaves

    def setOctaves(self, octaves: int):
        self.__octaves = self.__getOctaves(octaves)
        self.__hmax, self.__weight = self.__calcHMaxWeight()
        self.fwm = self.__octaves

    @property
    def persistence(self) -> float:
        return self.__persistence

    def setPersistence(self, persistence: float):
        self.__persistence = self.__getPersistence(persistence)
        self.__hmax, self.__weight = self.__calcHMaxWeight()

    @property
    def lacunarity(self) -> float:
        return self.__lacunarity

    def setLacunarity(self, lacunarity: float):
        self.__lacunarity = self.__getLacunarity(lacunarity)

    def __repr__(self):
        return super(Noise, self).__repr__()[:-1] + \
               f' oct={self.octaves} per={self.persistence} lac={self.lacunarity}>'

    def __init__(self, *args,
                 octaves: int = 8,  # todo: diff octaves for diff dims
                 persistence: float = 0.5,
                 lacunarity: float = 2.0,
                 **kwargs):
        """
        :param octaves: number(s) of additive overlapping noise wave(s), default 8
        :param lacunarity: frequency multiplier for successive noise octave, default 2
        :param persistence: amplitude modulator for successive noise octave, default 0.5
        """

        self.__octaves = self.__getOctaves(octaves)
        self.__persistence = self.__getPersistence(persistence)
        self.__lacunarity = self.__getLacunarity(lacunarity)
        # todo: explain hMax, weight
        self.__hmax, self.__weight = self.__calcHMaxWeight()
        super(Noise, self).__init__(*args, **kwargs, fwm=self.__octaves)

    def __call__(self, *coords: "collections.Iterable", _format: str = "fill" or "expand" or "none"):
        """
        todo: documentation required
        :param coords:
        :param checkFormat:
        :return:
        """
        fCoords, shape = self.formatCoords(coords, _format)
        fCoords *= self.__lacunarity ** (self.__octaves - 1)
        bIndex, bCoords = self.findBounds(fCoords)
        fab = self.findFab(bIndex)
        bSpace = fab[tuple(bIndex - bIndex.min((1, 2))[:, None, None])]

        h = self.bNoise(bSpace.T, bCoords.T) * self.__weight[0]
        for i in range(1, self.__octaves):
            fCoords /= self.__lacunarity
            bIndex, bCoords = self.findBounds(fCoords)
            bSpace = fab[tuple(bIndex - bIndex.min((1, 2))[:, None, None])]
            h += self.bNoise(bSpace.T, bCoords.T) * self.__weight[i]
        return self.applyRange(h).reshape(shape)

    def __calcHMaxWeight(self):
        hmax = (1 - self.__persistence ** self.__octaves) / (1 - self.__persistence) if self.__persistence != 1 \
            else self.__octaves
        weight = [self.__persistence ** i / hmax for i in range(self.__octaves)][::-1]
        return hmax, weight

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
