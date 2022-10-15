# todo: versions auto
# todo: usage and main.py
# todo: PyPI link in README.md

from NPerlinNoise import *

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
    plot = 1
    mul, res = 1, 4
    colorMap = (
        "#00f",
        "#0f0",
        "#f00",
    )
    gradients = Gradient.none()
    colorGradient = LinearColorGradient(*colorMap, grad='s').earth(grad='i') or LinearColorGradient.none()
    h, coordsMesh = perlinGenerator(noise,
                                    (0, noise.waveLength[0] * mul, noise.waveLength[0] * res),
                                    (0, noise.waveLength[1] * mul, noise.waveLength[0] * res))
    g = applyGrads(h, coordsMesh, gradients)
    c = colorGradient(g)

    if plot == 1:
        from matplotlib import pyplot
        # ---matplotlib---
        fig, ax = pyplot.subplots()
        ax.imshow(c, cmap="gray")
        pyplot.show()
    elif plot == 2:
        import plotly.graph_objects as go
        from plotly.offline import offline
        # -----plotly-----
        marker_data = go.Surface(x=coordsMesh[0], y=coordsMesh[1], z=g)
        fig = go.Figure(data=marker_data)
        fig.update_layout(
            scene=dict(zaxis=dict(nticks=4, range=[0, 2])),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))
        fig.update_traces(contours_z=dict(
            show=True, usecolormap=True,
            highlightcolor='limegreen',
            project_z=True))
        offline.plot(fig)


if __name__ == '__main__':
    main()
