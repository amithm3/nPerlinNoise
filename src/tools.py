import warnings
from typing import Callable
from functools import cache

import numpy as np
import numexpr as ne


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


class PRNG:
    def __init__(self, seed):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2 ** 32
        self.seed = seed

    def __call__(self, ids):
        return self.__n_rnd(ids, [self.seed] * len(ids[0]))

    def __rnd(self, _id, seed):
        if len(_id) == 1:
            return self.__gen(_id[-1], seed)
        else:
            return self.__rnd(_id[:-1], self.__gen(_id[-1], seed))

    def __n_rnd(self, ids, seeds):
        if len(ids) == 1:
            arr = np.zeros_like(ids[0], dtype=np.float32)
            for i, x in enumerate(ids[0]): arr[i] = self.__gen(x, seeds[i]) / self.m
        else:
            seeds = [self.__gen(x, seeds[i]) for i, x in enumerate(ids[-1])]
            arr = self.__n_rnd(ids[:-1], seeds)
        return arr

    @cache
    def __gen(self, n, seed):
        if n == 0: return seed
        gen = (self.a * int(n) + self.c) % self.m
        return (self.a * int(seed ** .5 * gen ** .5) + self.c) % self.m


class Fabric:
    def __init__(self, seed, frequency):
        self.frequency = frequency
        self.prng = PRNG(seed)

    def __getitem__(self, item):
        return self.prng([i.flatten() for i in item]).reshape(item[0].shape)


class RefNDArray(list):
    def __add__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a += o
        else:
            for a in self: a += other
        return self

    def __sub__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a -= o
        else:
            for a in self: a -= other
        return self

    def __mul__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a *= o
        else:
            for a in self: a *= other
        return self

    def __truediv__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a /= o
        else:
            for a in self: a /= other
        return self

    def __getitem__(self, item):
        if isinstance(item, int):
            return super(RefNDArray, self).__getitem__(item)
        elif isinstance(item, slice):
            return RefNDArray(super(RefNDArray, self).__getitem__(item))
        else:
            return RefNDArray([array[item[1:]] for array in self[item[0]]])

    def np_array(self, c):
        self._non_ndarray_present = True
        return np.array(c)

    def __init__(self, arr, **kwargs):
        try:
            dep_warn = kwargs["dep_warn"]
        except KeyError:
            dep_warn = False
        self._non_ndarray_present = False
        super(RefNDArray, self).__init__(self.np_array(c) if not isinstance(c, np.ndarray) else c for c in arr)
        if self._non_ndarray_present and not dep_warn: warnings.warn(
            "Using RefNDArray on array with non ndarray elements is not recommended, "
            "will convert element(s) to ndarray without warning in future",
            FutureWarning)

    def repeat(self, repeats=None, axis=None):
        if repeats is None: repeats = 1
        if axis is None: axis = 0
        if axis == 0:
            self.extend([self] * repeats)
        else:
            for i, array in enumerate(self): self[i] = array.repeat(repeats, axis - 1)
        return self


class Warp:
    def __repr__(self):
        return f"<Warp:{self.__name}>"

    def __init__(self, foo: Callable[['np.ndarray'], 'np.ndarray'], _name: str):
        self.__name = _name
        self.__foo = foo

    def __call__(self, a):
        return self.__foo(a)

    @staticmethod
    def classicLerp(): return Warp(lambda a: ne.evaluate("a", local_dict={'a': a}), "ClassicLerp")

    @staticmethod
    def square(): return Warp(lambda a: ne.evaluate("a * a", local_dict={'a': a}), "Square")

    @staticmethod
    def cubic(): return Warp(lambda a: ne.evaluate("a * a * a", local_dict={'a': a}), "Cubic")

    @staticmethod
    def improved(): return Warp(lambda a: ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a}),
                                "Improved")

    @staticmethod
    def cosine(): return Warp(
        lambda a: ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': np.float32(np.pi)}), "Cosine")

    @staticmethod
    def step(): return Warp(lambda a: ne.evaluate("where(a < .5, 0, 1)", local_dict={'a': a}), "Step")

    @staticmethod
    def polynomial(n):
        def poly(): return Warp(lambda a, nn=n: ne.evaluate("a ** nn", local_dict={'a': a, 'nn': nn}), f"Poly{n}")

        return poly


class Gradient:
    def __repr__(self):
        return f"<Gradient:{self.__name}>"

    def __init__(self, foo: Callable[['np.ndarray', ...], 'np.ndarray'], _name):
        self.__name = _name
        self.__foo = foo

    def __call__(self, a, *_coordsShape):
        return self.__foo(a, *_coordsShape)

    @staticmethod
    def woodSpread(n=4):
        return Gradient(lambda a, *cs: np.sin(a * n * np.sqrt(np.sum(np.square(
            cs - np.max(cs, axis=tuple(i for i in range(1, len(cs) + 1)), keepdims=True) / 2), axis=0))),
                        "Wood")

    @staticmethod
    def wood(n=4, m=8):
        return Gradient(lambda a, *cs: np.sin(m * a + n * np.sqrt(np.sum(np.square(
            cs - np.max(cs, axis=tuple(i for i in range(1, len(cs) + 1)), keepdims=True) / 2), axis=0))),
                        "Wood")

    @staticmethod
    def ply(n=16):
        def gradient(a):
            a = n * a
            return a - np.floor(a)

        return Gradient(lambda a, *_: gradient(a), "Ply")

    @staticmethod
    def terrace(n=16):
        def gradient(a):
            return np.int8(n * a) / n

        return Gradient(lambda a, *_: gradient(a), "Ply")

    @staticmethod
    def marbleSpread(n=4):
        return Gradient(lambda a, *cs: np.sin(np.sum(cs, axis=0) * a * n), "MarbleSpread")

    @staticmethod
    def marble(n=4, m=8):
        return Gradient(lambda a, *cs: np.sin((np.sum(cs, axis=0) + a * m) * n), "Marble")

    @staticmethod
    def none():
        return Gradient(lambda a, *cs: a, 'None ')
