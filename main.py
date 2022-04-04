import numpy as np
import plotly.graph_objects as go
import plotly.offline as offline
from matplotlib import pyplot, cm, animation

from perlin import PerlinNoise

# todo: even if dim changes the values in the prev plane should be same

# -----hyper-parameters-----
d = 3
dt = d
dl = (0, 100, 50), (0, 100, 50), (-50, 50, 100)
pt = '4D'  # 2D or 3D or 4D
cmap = 'gray'
f = None
s = None
w = None
o = None
p = None
# --------------------------

perlinNoise = PerlinNoise(d, octaves=o, persistence=p, frequency=f, seed=s, waveLength=w)
coordsBase = [np.linspace(*dl[i] if i < len(dl) else dl[-1]) for i in range(dt)]
coords = np.meshgrid(*coordsBase)
coordsRavel = [c.ravel() for c in coords]
h = perlinNoise(*coordsRavel)

try:
    if pt == '2D':
        fig, ax = pyplot.subplots()
        if len(coords) > 1:
            h = h.repeat(3)
            ax.imshow(h.reshape((*coords[0].shape, 3)), cmap=cmap)
        else:
            ax.plot(coords[0], h)
            ax.set_ylim(-.1, 1.1)
        fig.show()
    elif pt == '3D':
        assert dt >= 2
        marker_data = go.Surface(
            x=coords[0],
            y=coords[1],
            z=h.reshape(coords[0].shape) * .75 + .125)
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
        frames = go.Frames(
            go.Surface(
                x=coords[0],
                y=coords[1],
                z=h.reshape(coords[0].shape) * .75 + .125)
        )
        animations.__DF__ = frames
        animations.app.run_server(debug=True)
    else:
        raise ValueError(f"{pt=} is invalid")
except NameError:
    pass
