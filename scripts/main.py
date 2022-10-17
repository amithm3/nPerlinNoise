# main.py

# todo: versions auto in [package.json, __init__.py, pyproject.toml, README.md]

from nPerlinNoise import *

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
    mul, res = 1, 2
    colorMap = (
        "#000",
        "#b7410e",
    )
    gradients = Gradient.scope()
    colorGradient = LinearColorGradient(*colorMap, grad='s') and LinearColorGradient.sun(grad='s')
    h, coordsMesh = perlinGenerator(noise,
                                    (0, noise.waveLength[0] * mul, noise.waveLength[0] * res),
                                    (0, noise.waveLength[1] * mul, noise.waveLength[1] * res),
                                    # (0, noise.waveLength[2] * mul, 3),
                                    )
    g = applyGrads(h, coordsMesh, gradients)
    c = colorGradient(g)
    # c = g

    if plot == -1:
        from matplotlib import image
        image.imsave(f'snaps/img_{noise.seed}.png', c)
    elif plot == 1:
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
