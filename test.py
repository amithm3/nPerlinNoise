import numpy as np

from src.tools import PRNG
from matplotlib import pyplot

prng = PRNG(7688)
x, y = 50, 50
arr = prng([np.tile(np.arange(0, x), x), np.arange(0, x).repeat(x)])
arr.resize((x, y))

pyplot.imshow(arr)
