import plotly.graph_objects as go
from plotly.offline import offline
from matplotlib import pyplot

from src import *


def main():
    noise = Noise(
        seed=696969,
        frequency=8,
        waveLength=128,
        warp=Warp.improved(),
        _range=(0, 1),
        octaves=8,
        persistence=.5,
        lacunarity=2,
    )
    gradient = Gradient.island()
    mul, res = 1, 4
    h, *coordsMesh = perlinGenerator(noise, *[(0, 128 * mul, 128 * res * mul)] * 2, gradient=gradient)
    c = LinearColorGradient("#006994",
                            "#f6d7b0",
                            "#4d8204", "#4d8204", "#1F6420", "#1F6420",
                            "#977c53", "#977c53", "#fff")(h)
    plot = 1

    if plot == 1:
        # -----Matplotlib-----
        fig, ax = pyplot.subplots()
        # h *= 255
        ax.imshow(c, cmap="gray")
        pyplot.show()

    elif plot == 2:
        # -----plotly-----
        marker_data = go.Surface(x=coordsMesh[0], y=coordsMesh[1], z=h, colorscale=["#006994",
                                                                                    "#f6d7b0",
                                                                                    "#4d8204",
                                                                                    "#4d8204",
                                                                                    "#1F6420",
                                                                                    "#1F6420",
                                                                                    "#977c53",
                                                                                    "#977c53",
                                                                                    "#fff"])
        fig = go.Figure(data=marker_data)
        fig.update_layout(
            scene=dict(zaxis=dict(nticks=4, range=[0, 16])),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))
        fig.update_traces(contours_z=dict(
            show=True, usecolormap=True,
            highlightcolor='limegreen',
            project_z=True))
        offline.plot(fig)

    return noise


if __name__ == '__main__':
    n = main()
