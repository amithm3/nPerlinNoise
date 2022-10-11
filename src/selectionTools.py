from typing import Callable

import numpy as np

from .tools import iterable, NTuple

try:
    import numexpr as ne
except ImportError:
    class ne:  # noqa
        @staticmethod
        def evaluate(expr, local_dict):
            local_dict['a'] = np.array(local_dict['a'])
            return eval(expr, {}, local_dict)


class Warp:
    def __repr__(self):
        return f"<Warp:{self.__name}>"

    def __init__(self, foo: Callable[['np.ndarray'], 'np.ndarray'], _name: str):
        self.__name = _name
        self.__foo = foo

    def __call__(self, a):
        return self.__foo(a)

    @staticmethod
    def improved():
        return Warp(lambda a: ne.evaluate("a * a * a * (3 * a * (2 * a - 5) + 10)", local_dict={'a': a}), "Improved")

    @staticmethod
    def lerp():
        return Warp(lambda a: ne.evaluate("a", local_dict={'a': a}), "lerp")

    @staticmethod
    def square():
        return Warp(lambda a: ne.evaluate("a * a", local_dict={'a': a}), "Square")

    @staticmethod
    def cubic(): return Warp(lambda a: ne.evaluate("a * a * a", local_dict={'a': a}), "Cubic")

    @staticmethod
    def cosine(): return Warp(
        lambda a: ne.evaluate("(1 - cos(pi*a)) / 2", local_dict={'a': a, 'pi': np.float32(np.pi)}), "Cosine")

    @staticmethod
    def step():
        return Warp(lambda a: ne.evaluate("where(a < .5, 0, 1)", local_dict={'a': a}), "Step")

    @staticmethod
    def polynomial(n: float):
        return Warp(lambda a: ne.evaluate("a ** n", local_dict={'a': a, 'n': n}), f"Poly{n}")


class Gradient:
    def __repr__(self):
        return f"<Gradient:{self.__name}>"

    def __init__(self, foo: Callable[['np.ndarray', ...], 'np.ndarray'], _name):
        self.__name = _name
        self.__foo = foo

    def __call__(self, a, *_coordsShape):
        return self.__foo(a, *_coordsShape)

    @staticmethod
    def woodSpread(n=1) -> "Gradient":
        return Gradient(lambda a, *cm: (np.sin(a * n * np.sqrt(np.sum(np.square(
            cm - np.max(cm, axis=tuple(i for i in range(1, len(cm) + 1)), keepdims=True) / 2), axis=0))) + 1) / 2,
                        "WoodSpread")

    @staticmethod
    def wood(n=1, m=16) -> "Gradient":
        return Gradient(lambda a, *cm: (np.sin(m * a + n * np.sqrt(np.sum(np.square(
            cm - np.max(cm, axis=tuple(i for i in range(1, len(cm) + 1)), keepdims=True) / 2), axis=0))) + 1) / 2,
                        "Wood")

    @staticmethod
    def ply(n=8) -> "Gradient":
        def gradient(a):
            a = n * a
            return a - np.floor(a)

        return Gradient(lambda a, *_: gradient(a), "Ply")

    @staticmethod
    def terrace(n=8) -> "Gradient":
        return Gradient(lambda a, *_: np.int8(n * a) / n, "Terrace")

    @staticmethod
    def terraceSmooth(n=8) -> "Gradient":
        def gradient(a):
            for i in range(1, n + 1):
                a = np.where(a > i / n * a.max(), a, a - a / i)
            return a

        return Gradient(lambda a, *_: gradient(a), "TerraceSmooth")

    @staticmethod
    def island(n=16, m=1) -> "Gradient":
        scope = Gradient.scope(m)

        def gradient(a):
            for i in range(1, n + 1):
                a = np.where(a > i / n * a.max(), a + a / i / 3, a)
            return a

        return Gradient(lambda a, *cm: gradient(scope(a, *cm)), "Island")

    @staticmethod
    def marbleFractal(n=0.5) -> "Gradient":
        return Gradient(lambda a, *cm: (np.sin(np.sum(cm, axis=0) * a * n) + 1) / 2, "MarbleSpread")

    @staticmethod
    def marble(n=.5, m=32) -> "Gradient":
        return Gradient(lambda a, *cm: (np.sin((np.sum(cm, axis=0) + a * m) * n) + 1) / 2, "Marble")

    @staticmethod
    def invert() -> "Gradient":
        return Gradient(lambda a, *_: a.max() - a, "Invert")

    @staticmethod
    def scope(m=1) -> "Gradient":
        if not iterable(m): m = NTuple((m,))

        def gradient(a, cm):
            cm = [(c - c.max() / 2) / c.max() * 2 * m[i] for i, c in enumerate(cm)]
            return a * np.where((b := np.sum(np.square(cm), axis=0) ** .5) > 1, 0, 1 - b)

        return Gradient(lambda a, *cm: gradient(a, cm), "Scope")

    @staticmethod
    def none() -> "Gradient":
        return Gradient(lambda a, *_: a, "None")


def linearColorGradient(*cols: str):
    cols = list(cols)
    for i, col in enumerate(cols):
        col = col[1:]
        assert (length := len(col)) in (3, 6, 9), \
            f"invalid color {col}"
        length //= 3
        col = [int('0x' + col[ch * length:ch * length + length] * (3 - length), 0) for ch in range(3)]
        cols[i] = col
    cols = np.array(cols + [cols[0]], dtype=np.int16)

    def gradient(a, off: float = 0):
        a = np.array(a)
        _range = [a.min(d := tuple(range(a.ndim))), a.max(d)]
        if off > 0: _range[0] -= (_range[1] - _range[0]) * off
        elif off < 0: _range[1] -= (_range[1] - _range[0]) * off
        a = (a - _range[0]) / (_range[1] - _range[0]) * (len(cols) - 2)
        a_i = np.floor(a).astype(np.uint8)
        a -= a_i
        _range = cols[a_i], cols[a_i + 1]
        return (a[..., None] * (_range[1] - _range[0] + 1) + _range[0]).astype(np.uint8)

    return gradient
