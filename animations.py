from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Animated GDP and population over decades'),
    html.P("Select an animation:"),
    dcc.RadioItems(
        id='animations-x-selection',
        options=["time"],
        value='time',
    ),
    dcc.Loading(dcc.Graph(id="animations-x-graph"), type="cube")
])

__DF__ = None


@app.callback(
    Output("animations-x-graph", "figure"),
    Input("animations-x-selection", "value"))
def display_animated_graph(selection):
    animations = {
        'time': px.scatter_3d(
            __DF__, animation_frame=0, log_x=True, size_max=55, range_z=[0, 1],
            width=700),
    }
    return animations[selection]
