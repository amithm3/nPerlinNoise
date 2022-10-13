import numpy as np

from src import NPerlin
from src.generator import meshgrid

pern = NPerlin(696969, 32)

inc0 = pern.waveLength[0] * (1 + 1 / (pern.frequency[0] - 1))
inc2 = pern.waveLength[2] * (1 + 1 / (pern.frequency[2] - 1))
print(
    "Repeatability:",
    pern(
        [[4, 9, 16, 25], [inc0 + 4, inc0 + 9, inc0 + 16, inc0 + 25]],
        [[0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 64, 128, 32], [inc2 + 0, inc2 + 64, inc2 + 128, inc2 + 32]]
    ),
    sep='\n',
    end='\n\n'
)

print("Higher Dims Compatibility:")
print(pern(35, 66, 100, 173) == pern(35, 66, 100, 173, 0) == pern(35, 66, 100, 173, 0, 0))
p1 = pern(*meshgrid((0, 128, pern.frequency[0]), (0, 128, pern.frequency[1])))
p2 = pern(*meshgrid((0, 128, pern.frequency[0]), (0, 128, pern.frequency[1]), (0, 128, pern.frequency[2])))
f = pern.fabric((pern.frequency[0], pern.frequency[2], pern.frequency[2]))
print((p1 == p2[0]).all(), np.isclose(f, p2).all(), sep='\n')
