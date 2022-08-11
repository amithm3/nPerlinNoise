from src.tools import BasePRNG
from matplotlib import pyplot

prng = BasePRNG(999)
arr = [[prng(i * 100 + j) / prng.m for j in range(100)] for i in range(100)]

pyplot.imshow(arr)

