import numpy as np

from src import NPerlin
from src.generator import meshgrid

pern = NPerlin(696969, 32)

print(
    pern(
        [4, 9, 16, 25],
        [0, 0, 0, 0],
        [0, 64, 128, 192]
    )
)

print(pern(35, 66, 100) == pern(35, 66, 100, 0))

p1 = pern(*meshgrid((0, 128, pern.frequency[0]), (0, 128, pern.frequency[1])))
p2 = pern(*meshgrid((0, 128, pern.frequency[0]), (0, 128, pern.frequency[1]), (0, 128, pern.frequency[2])))
f = pern.fabric((pern.frequency[0], pern.frequency[2], pern.frequency[2]))
print((p1 == p2[0]).all(), np.isclose(f, p2).all())
