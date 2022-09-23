import random as rnd
from typing import Callable
from types import SimpleNamespace

import numpy as np

try:
    import numexpr as ne
except ImportError:
    class ne:  # noqa
        @staticmethod
        def evaluate(expr, local_dict):
            local_dict['a'] = np.array(local_dict['a'])
            return eval(expr, {}, local_dict)


def iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False


class NTuple(tuple):
    def __getitem__(self, item):
        if isinstance(item, slice):
            stop = r2 = None
            if item.stop and item.stop >= len(self):
                item, stop = slice(item.start, stop, item.step), item.stop
                r2 = (self[-1],) * ((stop - len(self) - 1) // (item.step if item.step is None else 1))
            return super(NTuple, self).__getitem__(item) + r2
        else:
            if item > len(self): item = -1
            return super(NTuple, self).__getitem__(item)

    def __new__(cls, *elements):
        return super(NTuple, cls).__new__(cls, elements)


class XPrng:
    __a = 1664525
    __c = 1013904223
    __m = 2 ** 32

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
        self.__prng = XPrng(seed=seed)
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


class NFabric:
    def __init__(self, seed=None):
        self.__prng = NPrng(seed)
        self.__seed = self.__prng.seed()

    # todo: make slice item and index item available
    def __getitem__(self, item):
        if iterable(item):
            return self.__prng(*[np.ravel(i) for i in item]).reshape(np.shape(item[0]))
        else:
            raise NotImplementedError("slice item and index item un-available, only iterable implemented")

    def seed(self) -> int:
        return self.__seed


class Warp:
    def __repr__(self):
        return f"<Warp:{self.__name}>"

    def __init__(self, foo: Callable[['np.ndarray'], 'np.ndarray'], _name: str):
        self.__name = _name
        self.__foo = foo

    def __call__(self, a):
        return self.__foo(a)

    @staticmethod
    def lerp():
        return Warp(lambda a: ne.evaluate("a", local_dict={'a': a}), "lerp")

    @staticmethod
    def square():
        return Warp(lambda a: ne.evaluate("a * a", local_dict={'a': a}), "Square")

    @staticmethod
    def cubic(): return Warp(lambda a: ne.evaluate("a * a * a", local_dict={'a': a}), "Cubic")

    @staticmethod
    def improved():
        return Warp(lambda a: ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a}), "Improved")

    @staticmethod
    def cosine(): return Warp(
        lambda a: ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': np.float32(np.pi)}), "Cosine")

    @staticmethod
    def step():
        return Warp(lambda a: ne.evaluate("where(a < .5, 0, 1)", local_dict={'a': a}), "Step")

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
    def woodSpread(n=1):
        return Gradient(lambda a, *cm: (np.sin(a * n * np.sqrt(np.sum(np.square(
            cm - np.max(cm, axis=tuple(i for i in range(1, len(cm) + 1)), keepdims=True) / 2), axis=0))) + 1) / 2,
                        "Wood")

    @staticmethod
    def wood(n=1, m=16):
        return Gradient(lambda a, *cm: (np.sin(m * a + n * np.sqrt(np.sum(np.square(
            cm - np.max(cm, axis=tuple(i for i in range(1, len(cm) + 1)), keepdims=True) / 2), axis=0))) + 1) / 2,
                        "Wood")

    @staticmethod
    def ply(n=8):
        def gradient(a):
            a = n * a
            return a - np.floor(a)

        return Gradient(lambda a, *_: gradient(a), "Ply")

    @staticmethod
    def terrace(n=8):
        def gradient(a):
            return np.int8(n * a) / n

        return Gradient(lambda a, *_: gradient(a), "Ply")

    @staticmethod
    def marbleFractal(n=1):
        return Gradient(lambda a, *cm: (np.sin(np.sum(cm, axis=0) * a * n) + 1) / 2, "MarbleSpread")

    @staticmethod
    def marble(n=1, m=32):
        return Gradient(lambda a, *cm: (np.sin((np.sum(cm, axis=0) + a * m) * n) + 1) / 2, "Marble")

    @staticmethod
    def invert():
        return Gradient(lambda a, *_: a.max() - a, "Invert")

    @staticmethod
    def scope(m=1):
        def gradient(a, cm):
            cm = [(c - c.max() / 2) / c.max() * 2 * m for c in cm]
            return a * np.where((b := np.sum(np.square(cm), axis=0) ** .5) > 1, 0, 1 - b)

        return Gradient(lambda a, *cm: gradient(a, cm), "Scope")

    @staticmethod
    def none():
        return Gradient(lambda a, *_: a, 'None ')
