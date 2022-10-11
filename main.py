# import plotly.graph_objects as go
# from plotly.offline import offline
from matplotlib import pyplot, colors
import numpy as np

from src import *


def main():
    noise = Noise(
        seed=None,
        frequency=8,
        waveLength=128,
        warp=Warp.improved(),
        _range=(0, 1),
        octaves=8,
        persistence=.5,
        lacunarity=2,
    )
    gradient = Gradient.scope(), Gradient.terraceSmooth()
    mul, res = 1, 4
    h, *coordsMesh = perlinGenerator(noise, *[(0, 128 * mul, 128 * res * mul)] * 2, gradient=gradient)
    # h = linearColorGradient("#4d8204", "#006994")(h)
    plot = 1

    # cmap_pil = pyplot.get_cmap('Blues')
    # im = Image.fromarray((cmap_pil(h)[:, :, :-1] * 256).astype(np.uint8))
    # im.save('stump.jpeg')

    if plot == 1:
        # -----Matplotlib-----
        fig, ax = pyplot.subplots()
        h *= 255
        ax.imshow(h.astype(np.uint8), cmap="gray")
        pyplot.show()

    # island
    # h *= 255
    # ax.imshow(np.where(h < 25, h / 3, np.where(h < 45, h / 1.5, h)),
    #           cmap=colors.LinearSegmentedColormap.from_list(
    #               "", ["#006994", "#f6d7b0", "#4d8204", "#4d8204", "#977c53", "#977c53", "white"]
    #           ))

    # elif plot == 2:
    #     # -----plotly-----
    #     marker_data = go.Surface(x=coordsMesh[0], y=coordsMesh[1], z=h)
    #     fig = go.Figure(data=marker_data)
    #     fig.update_layout(
    #         scene=dict(zaxis=dict(nticks=4, range=[0, 1])),
    #         width=700,
    #         margin=dict(r=20, l=10, b=10, t=10))
    #     fig.update_traces(contours_z=dict(
    #         show=True, usecolormap=True,
    #         highlightcolor='limegreen',
    #         project_z=True))
    #     offline.plot(fig)

    return noise


if __name__ == '__main__':
    n = main()
