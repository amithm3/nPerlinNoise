from typing import Callable

import numpy as np

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

    def __call__(self, a, coordsMesh):
        return self.__foo(a, coordsMesh)

    @classmethod
    def woodSpread(cls, n=1) -> "Gradient":
        return cls(lambda a, cm: (np.sin(a * n * np.sqrt(np.sum(np.square(
            cm - np.max(cm, axis=tuple(i for i in range(1, len(cm) + 1)), keepdims=True) / 2), axis=0))) + 1) / 2,
                   "WoodSpread")

    @classmethod
    def wood(cls, n=1, m=16) -> "Gradient":
        return cls(lambda a, cm: (np.sin(m * a + n * np.sqrt(np.sum(np.square(
            cm - np.max(cm, axis=tuple(i for i in range(1, len(cm) + 1)), keepdims=True) / 2), axis=0))) + 1) / 2,
                   "Wood")

    @classmethod
    def ply(cls, n=8) -> "Gradient":
        def gradient(a):
            a = n * a
            return a - np.floor(a)

        return cls(lambda a, _: gradient(a), "Ply")

    @classmethod
    def terrace(cls, n=8) -> "Gradient":
        return cls(lambda a, _: np.int8(n * a) / n, "Terrace")

    @classmethod
    def terraceSmooth(cls, n=8) -> "Gradient":
        def gradient(a):
            for i in range(1, n + 1):
                a = np.where(a > i / n * a.max(), a, a - a / i)
            return a

        return cls(lambda a, _: gradient(a), "TerraceSmooth")

    @classmethod
    def island(cls, n=16, m=2) -> "Gradient":
        scope = Gradient.scope(m)

        def gradient(a):
            for i in range(1, n + 1):
                a = np.where(a > i / n * a.max(), a + a / i / 3, a)
            return a

        return cls(lambda a, cm: gradient(scope(a, cm)), "Island")

    @classmethod
    def marbleFractal(cls, n=0.5) -> "Gradient":
        return cls(lambda a, cm: (np.sin(np.sum(cm, axis=0) * a * n) + 1) / 2, "MarbleSpread")

    @classmethod
    def marble(cls, n=.5, m=32) -> "Gradient":
        return cls(lambda a, cm: (np.sin((np.sum(cm, axis=0) + a * m) * n) + 1) / 2, "Marble")

    @classmethod
    def invert(cls) -> "Gradient":
        return cls(lambda a, _: a.max() - a, "Invert")

    @classmethod
    def scope(cls, m=2) -> "Gradient":
        def gradient(a, cm):
            cm -= (_max := cm.max(tuple(range(1, a.ndim + 1)), keepdims=True)) / 2
            cm *= 2
            cm /= _max
            cmm = (cm ** 2).sum(0) / len(cm)
            return a * (1 - cmm) ** m

        return cls(lambda a, cm: gradient(a, cm), "Scope")

    @classmethod
    def none(cls) -> "Gradient":
        return cls(lambda a, _: a, "None")


def hexToRGB(cols) -> "np.ndarray[np.ndarray]":
    cols = list(cols)
    for i, col in enumerate(cols):
        col = col[1:]
        assert (length := len(col)) in (3, 6), \
            f"invalid color {col}"
        length //= 3
        col = [int('0x' + col[ch * length:ch * length + length] * max(3 - length, 1), 0) for ch in range(3)]
        cols[i] = col
    return np.array(cols, dtype=np.int16)


def rgbToHex(cols) -> list[str]:
    cols = list(cols)
    for i, col in enumerate(cols):
        assert len(col) == 3, \
            f"invalid color {col}"
        cols[i] = f'#{col[0]:02x}{col[1]:02x}{col[2]:02x}'
    return cols


class LinearColorGradient:
    def __init__(self, *cols: str, grad: str = 'i'):
        self.cols = hexToRGB(cols)
        if len(self.cols) == 1: self.cols = np.array([self.cols[0], 255 - self.cols[0]])
        self.grad = grad

    def sGradient(self, a):
        a = np.array(a)
        s = a.flatten()
        _as = s.argsort()
        length = (len(s) - 1) / (len(self.cols) - 1)
        pCol = self.cols[0]
        pI = 0
        x = np.zeros((np.prod(a.shape), 3))
        for i, col in enumerate(self.cols[1:]):
            ind = slice(pI, pI := np.where(s[_as] == s[_as][int((i + 1) * length)])[0][-1])
            _s = s[_as[ind], None]
            _range = _s.min(d := tuple(range(_s.ndim))), _s.max(d)
            _s = (_s - _range[0]) / (_range[1] - _range[0])
            _s = np.nan_to_num(_s)
            x[_as[ind]] = _s * (col - pCol) + pCol
            pCol = col
        return x.reshape(*a.shape, -1).astype(np.uint8)

    def iGradient(self, a):
        a = np.array(a)
        _range = a.min(d := tuple(range(a.ndim))), a.max(d)
        a = (a - _range[0]) / (_range[1] - _range[0]) * (len(self.cols) - 1)
        a_i = np.ceil(a).astype(np.int16)
        a -= a_i - 1
        _range = self.cols[[a_i - 1, a_i]]
        return (a[..., None] * (_range[1] - _range[0]) + _range[0]).astype(np.uint8)

    def __call__(self, a):
        if self.grad == 'i':
            grad = self.iGradient
        elif self.grad == 's':
            grad = self.sGradient
        else:
            raise ValueError(f"param grad invalid value '{self.grad}'")
        return grad(a)

    @classmethod
    def earth(cls, **kwargs):
        return cls(
            "#003366",
            "#006994",
            "#f6d7b0",
            "#1f6d04",
            "#6b9b1e",
            "#8dbf39",
            "#b9d980",
            "#977c53",
            "#fff",
            **kwargs
        )

    @classmethod
    def none(cls, **kwargs):
        return cls("#fff", **kwargs)

    @classmethod
    def sun(cls, **kwargs):
        return cls("#800909", "#fdcf58", **kwargs)
