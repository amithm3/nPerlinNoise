import numpy as np


def iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False


def maxLen(_iterables, *, key=None):
    if key is None: key = lambda x: x
    return len(key(max(_iterables, key=lambda x: len(key(x)))))


def findCorners(dim):
    """
    :param dim: corners of dim-dimensional box will be found
    :return: list of coords of corners
    """
    if dim == 1:
        return [[0], [1]]
    else:
        r = findCorners(dim - 1)
        corners = []
        [[corners.append([c, *cc]) for cc in r] for c in [0, 1]]
        return corners


def rand3(X, Y, z):
    # mix around the bits in X
    x = X * 3266489917 + 374761393
    x = (x << 17) | (x >> 15)

    # mix around the bits in Y and z and mix those into x
    x = x + Y * 3266489917
    x = x + z * 374761393

    # Give x a good stir
    x = x * 668265263
    x = x ^ (x >> 15)
    x = x * 2246822519
    x = x ^ (x >> 13)
    x *= 3266489917
    x ^= x >> 16

    # trim the result and scale it to a float in [0,2^32)
    return np.where(X == 0, Y, (x & 0x00ffffff) * (2 ** 32 // 0x1000000))


class NPrng:
    __m = np.uint32(2 ** 32 - 1)

    def __init__(self, seed: int = None):
        self.seed(seed)
        self.__seed = np.int64(seed)

    def __call__(self, *ns):
        seed = self.__seed
        for i, n in enumerate(ns): seed = rand3(np.uint32(n), np.uint32(seed), np.uint32(i))
        return seed / self.__m

    def seed(self, seed: int = None) -> int:
        if seed is not None:
            assert (isinstance(seed, int) and self.__m > seed >= 0), \
                f"param 'seed' must be ({self.__m} > 'int' >= 0) or 'None' for default random seed"
            self.__seed = seed
        return self.__seed

    def shaped(self, shape, off=None):
        if off is None: off = (0,) * len(shape)
        mesh = [m.ravel() for m in
                np.meshgrid(*[np.arange(o, s + o) for s, o in zip(shape, off)], indexing="ij")[::-1]]  # noqa
        return self(*mesh).reshape(shape)


class NTuple(tuple):
    def __mul__(self, other) -> "NTuple":
        if iterable(other):
            return NTuple(a * o for a, o in zip(self[:len(other)], other))
        else:
            return NTuple(a * other for a in self)

    def __rmul__(self, other) -> "NTuple":
        return self.__mul__(other)

    def __truediv__(self, other) -> "NTuple":
        if iterable(other):
            return NTuple(a / o for a, o in zip(self[:len(other)], other))
        else:
            return NTuple(a / other for a in self)

    def __rtruediv__(self, other) -> "NTuple":
        if iterable(other):
            return NTuple(o / a for a, o in zip(self[:len(other)], other))
        else:
            return NTuple(other / a for a in self)

    def __getitem__(self, item):
        if isinstance(item, slice):
            r2 = ()
            if item.stop and item.stop >= len(self):
                item, stop = slice(item.start, None, item.step), item.stop
                r2 = (self[-1],) * ((stop - len(self)) // (1 if item.step is None else 1))
            return super(NTuple, self).__getitem__(item) + r2
        else:
            if item >= len(self): item = -1
            return super(NTuple, self).__getitem__(item)
