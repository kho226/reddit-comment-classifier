```
''' 
    Author: Kyle Ong
    Date:  02/10/2019

    entry point for front end of trenddit

    fetches data from elasticsearch and redis
    redis contains past five days of histrical data
    elasticsearch contains all historical data

    realtime bubble chart refreshes every 300 milliseconds
'''

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
        Realtime analysis of trends in reddit topics
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

def config_trace(**kwargs):
    trace = {
        'x' : [kwargs.get("x")],
        'y' : [kwargs.get("y")],
        'text': kwargs.get('text'),
        'type' : kwargs.get('type'),
        'mode' : kwargs.get('mode'),
        'name' : kwargs.get('name'),
        'marker' : dict (
            color = [kwargs.get("color")],
            size  = kwargs.get("size"),
            sizemode = kwargs.get("sizemode"),
            sizeref = kwargs.get("sizeref"),
            sizemin = kwargs.get("sizemin"))}
    return trace

@app.callback(Output('realtime-bubble-chart', "figure"),
                [Input('interval-component', 'n_intervals')])
def update(n):
    #fetch data in real time

    size = [20, 40, 60, 80, 100, 80, 60, 40, 20, 40]

    fig = py.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout'] = {
        'showlegend': True
    } 
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['xaxis'] = {
        'range' : [1,40],
        'showticklabels' : False,
        'showline': True,
    }
    fig['layout']['yaxis'] = {
        'range': [1,40],
        'showticklabels' : False,
        'showline': True,
    }
    fig.append_trace(config_trace(
        x = 15,
        y = 15,
        text = "sports",
        type = 'scatter',
        mode = 'markers',
        name = 'Sports',
        color = 'rgb(93, 164, 214)',
        size = random.randint(10,25),
        sizemode = 'area',
        sizeref = 2.*max(size)/(40.**2),
        sizemin = 4
    ),1,1)
    fig.append_trace(config_trace(
        x = 17,
        y = 15,
        text = "sports",
        type = 'scatter',
        mode = 'markers',
        name = 'Media',
        color = 'rgb(255, 144, 14)',
        size = random.randint(6,50),
        sizemode = 'area',
        sizeref = 2.*max(size)/(40.**2),
        sizemin = 4
    ),1,1)
    fig.append_trace(config_trace(
        x = 20,
        y = 17,
        text = "sports",
        type = 'scatter',
        mode = 'markers',
        name = 'Travel',
        color = 'rgb(44, 160, 101)',
        size = random.randint(10,25),
        sizemode = 'area',
        sizeref = 2.*max(size)/(40.**2),
        sizemin = 4
    ),1,1)
    fig.append_trace(config_trace(
        x = 18,
        y = 20,
        text = "dining",
        type = 'scatter',
        mode = 'markers',
        name = 'Dining',
        color = 'rgb(255, 65, 54)',
        size = random.randint(25,30),
        sizemode = 'area',
        sizeref = 2.*max(size)/(40.**2),
        sizemin = 4
    ),1,1)

    return fig


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000)


