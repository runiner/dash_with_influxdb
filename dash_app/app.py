import logging
from datetime import datetime
from urllib3.exceptions import NewConnectionError

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

from repository import Storage


def fig():
    try:
        storage = Storage()  # TODO: keep connection open between refreshes
        data = storage.query("-10m")
    except (ConnectionRefusedError, NewConnectionError) as ex:
        logging.error(f"Got connection error: {ex}")
        data = []
    x, y = [], []
    for p in data:
        # Example: ('price', 77.44539475, datetime.datetime(2021, 5, 23, 17, 7, 52, 787000, tzinfo=tzutc()))
        x.append(p[2])
        y.append(p[1])
    if not x or not y:
        x, y = [datetime.utcnow()], [np.nan]  # Show empty plot when real data is not available
    return px.line(
        x=np.array(x), y=np.array(y),
        title="Data points", height=325,
        labels={'x': 'Datetime', 'y': 'Price'}
    )


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig()),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    ),
])


@app.callback(Output("graph", "figure"),
              Input("interval-component", "n_intervals"))
def update_metrics(_n):
    return fig()


if __name__ == "__main__":
    app.run_server(debug=True)
