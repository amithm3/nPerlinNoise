import numpy as np
import plotly.graph_objects as go
import plotly.offline as offline


def frame_args(duration):
    return {
        "frame": {"duration": duration},
        "mode": "immediate",
        "fromcurrent": True,
        "transition": {"duration": duration, "easing": "linear"},
    }


def run(__DATA__):
    # __DATA__ = (__DATA__[:, :, :, None].repeat(3, axis=3) * 255).astype(__np.uint8)
    fig = go.Figure(frames=[go.Frame(data=go.Surface(
        z=__DATA__[k],
    ),
        name=str(k)
    )
        for k in range(len(__DATA__))],
    )

    fig.add_trace(go.Surface(
        z=__DATA__[0],
    ))

    fig.update_layout(
        title='4D',
        width=500,
        height=500,
        scene=dict(
            zaxis=dict(range=[0, 1], autorange=False),
            aspectratio=dict(x=1, y=1, z=1),
        ),
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, frame_args(0)],
                        "label": "&#9654;",  # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;",  # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
        ],
        # sliders=sliders
    )

    offline.plot(fig)
