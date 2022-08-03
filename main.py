from src import *


def main():
    noise = NPerlinNoise(dims=2)
    gradient = None
    gen = perlinGenerator(noise, (0, 9, 999), gradient=gradient)


if __name__ == '__main__':
    main()
