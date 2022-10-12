from matplotlib import pyplot

from src import *

noise = Noise(
    seed=None,
    frequency=8,
    waveLength=128,
    warp=None,
    _range=None,
    octaves=8,
    persistence=0.5,
    lacunarity=2
)


def main():
    mul, res = 1, 4
    colorMap = (
        "#000",
    )
    gradient = Gradient.scope(), Gradient.terrace(32)
    colorGradient = LinearColorGradient(*colorMap, grad='i')
    colorGradient = LinearColorGradient.earth(grad='i')
    h, *coordsMesh = perlinGenerator(noise,
                                     (0, noise.waveLength[0] * mul, noise.waveLength[0] * res),
                                     (0, noise.waveLength[1] * mul, noise.waveLength[0] * res),
                                     gradient=gradient)
    h = colorGradient(h)

    fig, ax = pyplot.subplots()
    ax.imshow(h, cmap="gray")
    pyplot.show()


if __name__ == '__main__':
    main()
