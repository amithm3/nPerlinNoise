from perlin import PerlinNoise

pn = PerlinNoise(1, _range=(0, 2))
print(pn([1., 50, 100]))
