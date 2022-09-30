from .nPerlin import NPerlin
from .tools import RefND


class Noise(NPerlin):
    def __repr__(self):
        return super(Noise, self).__repr__()[:-1] + \
               f' oct:{self.__octaves} lac:{self.__lacunarity} per:{self.__persistence}>'

    def __init__(self, *args,
                 octaves: int = None,
                 lacunarity: float = None,
                 persistence: float = None,
                 **kwargs):
        """
        :param octaves: number(s) of additive overlapping noise wave(s), default 8
        :param lacunarity: frequency multiplier for successive noise octave, default 2
        :param persistence: amplitude modulator for successive noise octave, default 0.5
        """
        if lacunarity is None: lacunarity = 2
        if persistence is None: persistence = 0.5
        if octaves is None: octaves = 8  # todo: diff octaves for diff dims

        assert isinstance(octaves, int) and 1 <= octaves <= 8
        assert isinstance(persistence, (int, float)) and 0 < persistence <= 1
        assert isinstance(lacunarity, (int, float)) and 1 < lacunarity

        self.__octaves = octaves
        self.__lacunarity = lacunarity
        self.__persistence = persistence
        if self.__chunked__: self.__chunked__ *= self.__octaves
        super(Noise, self).__init__(*args, **kwargs)

        self.__hmax = (1 - self.__persistence ** self.__octaves) / (1 - self.__persistence) if self.__persistence != 1 \
            else self.__octaves
        self.__AMPS = [self.__persistence ** i / self.__hmax for i in range(self.__octaves)][::-1]

    def __call__(self, *coords, checkFormat=True):
        """
        todo: documentation required
        :param coords:
        :param checkFormat:
        :return:
        """
        coords = RefND(coords) * self.__lacunarity ** (self.__octaves - 1)
        h = super(Noise, self).__call__(*coords, checkFormat=checkFormat) * self.__AMPS[0]
        for i in range(1, self.__octaves):
            coords /= self.__lacunarity
            h += super(Noise, self).__call__(*coords, checkFormat=checkFormat) * self.__AMPS[i]
        return h
