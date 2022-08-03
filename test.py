import numpy as np
import plotly.graph_objects as go
import plotly.offline as offline
from matplotlib import pyplot

from perlin import PerlinNoise
from tools import Warp

# -----hyper-parameters-----
d = 2
_w = None
dt = d
dl = (0, 100, 1000),
pt = '2D'  # 2D or 3D or 4D
cmap = 'gray'
f = 8
s = None
w = None
o = None
p = None
l = None
_r = None
# --------------------------

perlinNoise = PerlinNoise(d, _w, octaves=o, persistence=p, lacunarity=l, frequency=f, seed=s, waveLength=w, _range=_r)
coordsBase = [np.linspace(*dl[i] if i < len(dl) else dl[-1]) for i in range(dt)]
coords = np.meshgrid(*coordsBase)
coordsRavel = [c.ravel() for c in coords]
h = perlinNoise(*coordsRavel)

try:
    if pt == '2D':
        fig, ax = pyplot.subplots()
        if len(coords) > 1:
            ax.imshow(h.reshape(*coords[0].shape), cmap=cmap)
        else:
            ax.plot(coords[0], h)
            ax.set_ylim(-.1, 1.1)
        fig.show()
        pyplot.show()
    elif pt == '3D':
        assert dt >= 2
        marker_data = go.Surface(
            x=coords[0],
            y=coords[1],
            z=h.reshape(coords[0].shape))
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
    elif pt == '4D':
        import animations
        assert dt >= 3
        h = h.reshape(coords[0].shape).transpose() * .5 + .25
        animations.run(h)
    else:
        raise ValueError(f"{pt=} is invalid")
except NameError:
    pass
