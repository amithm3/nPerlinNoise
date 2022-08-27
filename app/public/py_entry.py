from src import *

noises = []


def newNoise(*args, **kwargs):
    noises.append(NPerlinNoise(*args, **kwargs))


if __name__ == '__main__':
    pass
