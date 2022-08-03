import warnings
import tempfile
from typing import Callable

import numpy as np
import numexpr as ne
from numpy.lib import format as fm


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


def writeNpyCache(array: "np.ndarray") -> np.ndarray:
    with tempfile.NamedTemporaryFile(suffix='.npy') as file:
        np.save(file, array)
        file.seek(0)
        fm.read_magic(file)
        fm.read_array_header_1_0(file)
        memMap = np.memmap(file, mode='r', shape=array.shape, dtype=array.dtype, offset=file.tell())
    return memMap


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
            "will convert element to ndarray without warning in future",
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
    def __init__(self, foo: Callable[['np.ndarray'], 'np.ndarray']):
        self.__foo = foo

    def __call__(self, a):
        return self.__foo(a)

    @staticmethod
    def classicLerp(): return Warp(lambda a: ne.evaluate("a", local_dict={'a': a}))

    @staticmethod
    def square(): return Warp(lambda a: ne.evaluate("a * a", local_dict={'a': a}))

    @staticmethod
    def cubic(): return Warp(lambda a: ne.evaluate("a * a * a", local_dict={'a': a}))

    @staticmethod
    def improved(): return Warp(lambda a: ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a}))

    @staticmethod
    def cosine(): return Warp(
        lambda a: ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': np.float32(np.pi)}))

    @staticmethod
    def step(): return Warp(lambda a: ne.evaluate("where(a < .5, 0, 1)", local_dict={'a': a}))

    @staticmethod
    def polynomial(n):
        def poly(): return Warp(lambda a, nn=n: ne.evaluate("a ** nn", local_dict={'a': a, 'nn': nn}))

        return poly
