import numpy as np

from .nPerlin import NPerlin


class Noise(NPerlin):
    @property
    def octaves(self):
        return self.__octaves

    def setOctaves(self, val):
        self.__octaves = self.__getOctaves(val)
        self.__hmax, self.__weight = self.__calcHMaxWeight()
        self.fwm = self.__octaves

    @property
    def persistence(self):
        return self.__persistence

    def setPersistence(self, val):
        self.__persistence = self.__getPersistence(val)
        self.__hmax, self.__weight = self.__calcHMaxWeight()

    @property
    def lacunarity(self):
        return self.__lacunarity

    def setLacunarity(self, val):
        self.__lacunarity = self.__getLacunarity(val)

    def __repr__(self):
        return super(Noise, self).__repr__()[:-1] + \
               f' oct:{self.octaves} per:{self.persistence} lac:{self.lacunarity}>'

    def __init__(self, *args,
                 octaves: int = None,
                 persistence: float = None,
                 lacunarity: float = None,
                 **kwargs):
        """
        :param octaves: number(s) of additive overlapping noise wave(s), default 8
        :param lacunarity: frequency multiplier for successive noise octave, default 2
        :param persistence: amplitude modulator for successive noise octave, default 0.5
        """
        if octaves is None: octaves = 8  # todo: diff octaves for diff dims
        if persistence is None: persistence = 0.5
        if lacunarity is None: lacunarity = 2

        self.__octaves = self.__getOctaves(octaves)
        self.__persistence = self.__getPersistence(persistence)
        self.__lacunarity = self.__getLacunarity(lacunarity)
        # todo: explain hMax, weight
        self.__hmax, self.__weight = self.__calcHMaxWeight()
        super(Noise, self).__init__(*args, **kwargs, fwm=self.__octaves)

    def __call__(self, *coords, checkFormat=True):
        """
        todo: documentation required
        :param coords:
        :param checkFormat:
        :return:
        """
        if len(coords) == 0: coords = (0,)

        fCoords = self.formatCoords([np.ravel(coo) for coo in coords]) * self.__lacunarity ** (self.__octaves - 1)
        bIndex, bCoords = self.findBounds(fCoords)
        fab = self.findFab(bIndex)
        bSpace = fab[tuple(bIndex - bIndex.min((1, 2))[:, None, None])]

        h = self.bNoise(bSpace.T, bCoords.T) * self.__weight[0]
        for i in range(1, self.__octaves):
            fCoords = self.formatCoords(fCoords / self.__lacunarity)
            bIndex, bCoords = self.findBounds(fCoords)
            bSpace = fab[tuple(bIndex - bIndex.min((1, 2))[:, None, None])]
            h += self.bNoise(bSpace.T, bCoords.T) * self.__weight[i]
        return self.applyRange(h)

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
        assert isinstance(lacunarity, (int, float)) and 1 < lacunarity
        return lacunarity
