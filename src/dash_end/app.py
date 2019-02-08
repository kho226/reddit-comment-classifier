# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import constants
import redis
from elasticsearch import Elasticsearch

es = Elasticsearch(constants.elastic["url"])
redis = redis.StrictRedis(
    host=constants.redis["host"],
    port=constants.redis["port"],
    db=constants.redis["db"]
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Trenddit'),

    html.Div(children='''
        Realtime analytics of trends in reddit topics
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)