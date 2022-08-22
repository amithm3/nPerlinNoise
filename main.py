import plotly.graph_objects as go
from plotly.offline import offline
from matplotlib import pyplot
from PIL import Image
import numpy as np

from src import *


def main():
    noise: "NPerlinNoise" = NPerlinNoise(frequency=8,
                                         seed=None,
                                         waveLength=128,
                                         _range=(0, 1),
                                         octaves=8,
                                         lacunarity=2,
                                         persistence=.5,
                                         dims=2)
    gradient = Gradient.marble(), Gradient.woodSpread(), Gradient.marbleFractal()
    res, mul = 4, .2
    h, *coordsMesh = perlinGenerator(noise, *[(0, 128 * mul, 256 * res)] * 2, gradient=gradient)
    plot = 1

    # cmap_pil = pyplot.get_cmap('Blues')
    # im = Image.fromarray((cmap_pil(h)[:, :, :-1] * 256).astype(np.uint8))
    # im.save('stump.jpeg')

    if plot == 1:
        # -----Matplotlib-----
        fig, ax = pyplot.subplots()
        ax.imshow(h * 255, cmap='Blues')
        pyplot.show()

    elif plot == 2:
        # -----plotly-----
        marker_data = go.Surface(x=coordsMesh[0], y=coordsMesh[1], z=h)
        fig = go.Figure(data=marker_data)
        fig.update_layout(
            scene=dict(zaxis=dict(nticks=4, range=[0, 1])),
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
