# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output


import constants
import redis
from elasticsearch import Elasticsearch

import random

es = Elasticsearch(constants.elastic["url"])
redis = redis.StrictRedis(
    host=constants.redis["host"],
    port=constants.redis["port"],
    db=constants.redis["db"]
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

size = [20, 40, 60, 80, 100, 80, 60, 40, 20, 40]
trace0 = go.Scatter(
    x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    y=[11, 12, 10, 11, 12, 11, 12, 13, 12, 11],
    mode='markers',
    marker=dict(
        size=size,
        sizemode='area',
        sizeref=2.*max(size)/(40.**2),
        sizemin=4
    )
)

data = [trace0]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Trenddit'),

    html.Div(children='''
        Realtime analytics of trends in reddit topics
    '''),

    dcc.Graph(
        id='realtime-bubble-chart'
    ),

    dcc.Interval(
        id="interval-component",
        interval=3*1000,
        n_intervals=0
    )
])

@app.callback(Output('realtime-bubble-chart', "figure"),
                [Input('interval-component', 'n_intervals')])
def update(n):
    #fetch data in real time

    fig = py.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['xaxis'] = {
        'range' : [1,30]
    }
    fig['layout']['yaxis'] = {
        'range': [1,30]
    }
    fig.append_trace({
        'x': [random.randint(1,20) for i in range(10)],
        'y': [random.randint(1,20) for i in range(10)],
        'type' : 'scatter',
        'mode' : 'markers',
        'marker' : dict(
            size=size,
            sizemode='area',
            sizeref=2.*max(size)/(40.**2),
            sizemin=4,
            color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)',
               'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
            opacity=[1, 0.8, 0.6, 0.4],
        )
    },1,1)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

