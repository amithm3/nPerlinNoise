import random as rnd
from types import SimpleNamespace

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
    if dim == 1:
        return [[0], [1]]
    else:
        r = findCorners(dim - 1)
        corners = []
        [[corners.append([c, *cc]) for cc in r] for c in [0, 1]]
        return corners


class NTuple(tuple):
    def __getitem__(self, item):
        if isinstance(item, slice):
            stop = r2 = None
            if item.stop and item.stop >= len(self):
                item, stop = slice(item.start, stop, item.step), item.stop
                r2 = (self[-1],) * ((stop - len(self) - 1) // (item.step if item.step is None else 1))
            return super(NTuple, self).__getitem__(item) + r2
        else:
            if item >= len(self): item = -1
            return super(NTuple, self).__getitem__(item)

    def __new__(cls, *elements):
        return super(NTuple, cls).__new__(cls, elements)


class XPrng:
    __a = np.float32(1664525)
    __c = np.float32(1013904223)
    __m = np.float32(2 ** 32)

    @property
    def acm(self):
        return SimpleNamespace(a=self.__a, c=self.__c, m=self.__m)

    def __init__(self, seed: int = None):
        if seed is None: seed: int = rnd.randint(0, self.__m)
        assert (isinstance(seed, int) and self.__m > seed >= 0), \
            f"param 'seed' must be ({self.__m} > 'int' >= 0) or 'None' for default random seed"

        self.__seed = seed

    def __call__(self, x):
        return self.atX(x, self.__seed) / self.__m

    def atX(self, x: int, seed: int):
        off = (self.__c * ((self.__a * x) ** .5 // 1) + seed) % self.__m
        return np.where(x == 0, seed, (self.__a * ((seed * off) ** .5 // 1) + self.__c) % self.__m)

    def seed(self, seed: int = None) -> int:
        if seed is not None: self.__seed = seed
        return self.__seed


class NPrng:
    def __init__(self, seed=None):
        self.__prng = XPrng(seed)
        self.__seed = self.__prng.seed()

    def __call__(self, *ns):
        return self.atN(self.__seed, ns) / self.__prng.acm.m

    def atN(self, seed, ns):
        if len(ns) == 1:
            return self.__prng.atX(ns[0], seed)
        else:
            seed = self.__prng.atX(ns[-1], seed)
            return self.atN(seed, ns[:-1])

    def seed(self, seed: int = None) -> int:
        if seed is not None: self.__seed = seed
        return self.__seed

    def shaped(self, shape, off=None):
        if off is None: off = (0,) * len(shape)
        mesh = [m.ravel() for m in np.meshgrid(*[np.arange(o, s + o) for s, o in zip(shape, off)])]  # noqa
        return self(*mesh).reshape(shape)


class NFabric:
    def __init__(self, seed=None):
        self.__prng = NPrng(seed)
        self.__seed = self.__prng.seed()

    # todo: make slice item and index item available
    def __getitem__(self, item):
        if iterable(item):
            # todo: check if prod(shape) > prod(np.shape(item)) and take different paths
            off, shape = np.array([(i.min(), i.max()) for i in item]).transpose()
            fabric = self.__prng.shaped(shape + 1, off)
            return fabric[item]
        else:
            raise NotImplementedError("slice item and index item un-available, only iterable implemented")

    def seed(self) -> int:
        return self.__seed


class RefND(list):
    def __mul__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a *= o
        else:
            for a in self: a *= other
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a /= o
        else:
            for a in self: a /= other
        return self

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __init__(self, obj):
        super(RefND, self).__init__(obj)
