import numpy as np
import numexpr as ne


class Perlin1D:
    def __init__(self, frequency=None, seed=None):
        if frequency is None:
            frequency = 2
        self.frequency = frequency
        self.amp = 100 / (self.frequency - 1)
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        np.random.seed(self.seed)
        self.fabric = np.random.random(self.frequency).astype(np.float32)

        self.appender = [[[0]], [[1]]]

    def extend_fabric(self, scale):
        for i in range(scale):
            self.fabric = np.concatenate((self.fabric, np.random.random(self.frequency - 1).astype(np.float32)), axis=0)

    def noise(self, x):
        atx = np.array([x]) / self.amp
        if np.max(atx) >= self.fabric.shape[0]:
            self.extend_fabric(int(np.max(atx) // self.fabric.shape[0]))
        x = atx.astype(np.int32)
        index = (x + self.appender).transpose()
        max_i = index.max()
        if max_i >= self.fabric.shape[0]:
            self.extend_fabric(int((max_i - self.fabric.shape[0]) / (self.frequency - 1)) + 1)
        atindex = self.fabric[index[:, 0]]

        return self.wrap(atindex, atx - x)

    @staticmethod
    def wrap(atindex, ata):
        ata = ata.astype(np.float32)
        return Perlin1D.smooth_wrap(ata) * (atindex[:, 1] - atindex[:, 0]) + atindex[:, 0]

    @staticmethod
    def smooth_wrap(a):
        return ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)")


class Perlin2D:
    def __init__(self, frequency=None, seed=None):
        if frequency is None:
            frequency = 2
        self.frequency = frequency
        self.amp = 100 / (self.frequency - 1)
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        np.random.seed(seed)
        self.fabric = np.random.random((self.frequency, self.frequency)).astype(np.float32)

        self.appender = np.array([[[0], [0]], [[1], [0]], [[0], [1]], [[1], [1]]])

    def extend_fabric(self, scale):
        for i in range(scale):
            self.fabric = np.concatenate(
                (self.fabric, np.random.random((self.fabric.shape[0], self.frequency - 1)).astype(np.float32)), axis=1)
            self.fabric = np.concatenate(
                (self.fabric, np.random.random((self.frequency - 1, self.fabric.shape[1])).astype(np.float32)), axis=0)

    def noise(self, x, y):
        atxy = np.array([x, y]) / self.amp
        xy = atxy.astype(np.int32)
        index = (xy + self.appender).transpose()
        max_i = index.max()
        if max_i >= self.fabric.shape[0]:
            self.extend_fabric(int((max_i - self.fabric.shape[0]) / (self.frequency - 1)) + 1)
        atindex = self.fabric[index[:, 1], index[:, 0]]

        return self.wrap(atindex, atxy - xy)

    @staticmethod
    def wrap(atindex, atab):
        intermediate = Perlin1D.wrap(atindex.reshape((-1, 2)), atab[0].repeat(2)).reshape(atindex.shape[0], 2)

        return Perlin1D.wrap(intermediate, atab[1])


class Perlin3D:
    def __init__(self, frequency=None, seed=None):
        if frequency is None:
            frequency = 2
        self.frequency = frequency
        self.amp = 100 / (self.frequency - 1)
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        np.random.seed(seed)
        self.fabric = np.random.random((self.frequency, self.frequency, self.frequency)).astype(np.float32)

        self.appender = np.array([[[0], [0], [0]], [[1], [0], [0]], [[0], [1], [0]], [[1], [1], [0]],
                                  [[0], [0], [1]], [[1], [0], [1]], [[0], [1], [1]], [[1], [1], [1]]])

    def extend_fabric(self, scale):
        for i in range(scale):
            self.fabric = np.concatenate((self.fabric, np.random.random(
                (self.fabric.shape[0], self.fabric.shape[1], self.frequency - 1)).astype(np.float32)), axis=2)
            self.fabric = np.concatenate((self.fabric, np.random.random(
                (self.fabric.shape[0], self.frequency - 1, self.fabric.shape[2])).astype(np.float32)), axis=1)
            self.fabric = np.concatenate((self.fabric, np.random.random(
                (self.frequency - 1, self.fabric.shape[1], self.fabric.shape[2])).astype(np.float32)), axis=0)

    def noise(self, x, y, z):
        atxyz = np.array([x, y, z]) / self.amp
        xyz = atxyz.astype(np.int32)
        index = (xyz + self.appender).transpose()
        max_i = index.max()
        if max_i >= self.fabric.shape[0]:
            self.extend_fabric(int((max_i - self.fabric.shape[0]) / (self.frequency - 1)) + 1)
        atindex = self.fabric[index[:, 2], index[:, 1], index[:, 0]]

        return self.wrap(atindex, atxyz - xyz)

    @staticmethod
    def wrap(atindex, atabc):
        intermediate = Perlin2D.wrap(atindex.reshape((-1, 4)), atabc[[0, 1]].repeat(2).reshape((2, -1))). \
            reshape(atindex.shape[0], 2)

        return Perlin1D.wrap(intermediate, atabc[2])


class PerlinNoise1D:
    def __init__(self, octaves=None, seed=None, lacunarity=None, persistence=None):
        if lacunarity is None:
            lacunarity = 2
        if persistence is None:
            persistence = 0.5
        if octaves is None:
            octaves = 8
        self.octaves = octaves
        self.lacunarity = lacunarity
        self.persistence = persistence
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        self.perlins = [Perlin1D(self.lacunarity ** i, self.seed) for i in range(1, self.octaves + 1)]
        self.amplitude = [self.persistence ** i for i in range(1, self.octaves + 1)]

    def noise(self, x):
        return np.sum([self.perlins[i - 1].noise(x) * self.amplitude[i - 1] for i in range(1, self.octaves + 1)],
                      axis=0)


class PerlinNoise2D:
    def __init__(self, octaves=None, seed=None, lacunarity=None, persistence=None):
        if lacunarity is None:
            lacunarity = 2
        if persistence is None:
            persistence = 0.5
        if octaves is None:
            octaves = 8
        self.octaves = octaves
        self.lacunarity = lacunarity
        self.persistence = persistence
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        self.perlins = [Perlin2D(self.lacunarity ** i, self.seed) for i in range(1, self.octaves + 1)]
        self.amplitude = [self.persistence ** i for i in range(1, self.octaves + 1)]

    def noise(self, x, y):
        return np.sum([self.perlins[i - 1].noise(x, y) * self.amplitude[i - 1] for i in range(1, self.octaves + 1)],
                      axis=0)


class PerlinNoise3D:
    def __init__(self, octaves=None, seed=None, lacunarity=None, persistence=None):
        if lacunarity is None:
            lacunarity = 2
        if persistence is None:
            persistence = 0.5
        if octaves is None:
            octaves = 8
        self.octaves = octaves
        self.lacunarity = lacunarity
        self.persistence = persistence
        if seed is None:
            self.seed = np.random.randint(0, 2 ** 16)
        else:
            self.seed = seed
        self.perlins = [Perlin3D(self.lacunarity ** i, self.seed) for i in range(1, self.octaves + 1)]
        self.amplitude = [self.persistence ** i for i in range(1, self.octaves + 1)]

    def noise(self, x, y, z):
        return np.sum([self.perlins[i - 1].noise(x, y, z) * self.amplitude[i - 1] for i in range(1, self.octaves + 1)],
                      axis=0)
