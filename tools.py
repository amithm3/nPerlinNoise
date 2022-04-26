import numpy as np
import numexpr as ne


def iterable(var):
    try:
        iter(var)
        return True
    except TypeError:
        return False


def maxlen(_iterables, *, key=None):
    if key is None:
        return len(max(_iterables, key=lambda x: len(x)))
    else:
        return len(max(_iterables, key=lambda x: len(key(x))))


def findCorners(dim):
    if dim == 1:
        return [[0], [1]]
    else:
        r = findCorners(dim - 1)
        corners = []
        [[corners.append([c, *cc]) for cc in r] for c in [0, 1]]
        return corners


class RefNDArray(list):
    def __sub__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a -= o
        else:
            for a in self: a -= other
        return self

    def __truediv__(self, other):
        if iterable(other):
            for a, o in zip(self, other): a /= o
        else:
            for array in self: array /= other
        return self

    def __getitem__(self, item):
        if isinstance(item, int):
            return super(RefNDArray, self).__getitem__(item)
        elif isinstance(item, slice):
            return RefNDArray(super(RefNDArray, self).__getitem__(item))
        else:
            return RefNDArray([array[item[1:]] for array in self[item[0]]])

    def repeat(self, repeats=None, axis=None):
        if repeats is None: repeats = 1
        if axis is None: axis = 0
        if axis == 0:
            self.extend([self] * repeats)
        else:
            for i, array in enumerate(self): self[i] = array.repeat(repeats, axis - 1)
        return self


class Warp:
    CLASSIC_LERP = lambda a: ne.evaluate("a", local_dict={'a': a})
    SQUARE = lambda a: ne.evaluate("a * a", local_dict={'a': a})
    CUBIC = lambda a: ne.evaluate("a * a * a", local_dict={'a': a})
    IMPROVED = lambda a: ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a})
    COSINE = lambda a: ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': np.float32(np.pi)})
    STEP = lambda a: ne.evaluate("where(a < .5, 0, 1)", local_dict={'a': a})

    @staticmethod
    def polynomial(n):
        return lambda a: ne.evaluate("a ** n", local_dict={'a': a, 'n': n})
