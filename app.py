#!/usr/bin/env python3
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html

import tanager.components as tc
import tanager.plots as tp

external_stylesheets = [
    "https://use.fontawesome.com/releases/v5.15.3/css/all.css"
]

app = dash.Dash(__name__, meta_tags=[
    {'name': 'viewport',
     'content': 'width=device-width, initial-scale=1.0'
     }
], external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    tc.navbar(children=[
        tc.navbar_item('Experiment 1', href='/overview/experiment1'),
        tc.navbar_item('Experiment 2', href='/overview/experiment2')
    ]),
    html.Div(children=[
        html.Main(children=[
            tc.graph_panel(children=[
               tp.generation_distribution()
            ]),
            tc.graph_panel(children=[
                tp.fitness_vs_generation()
            ]),
            tc.graph_panel('3'),
            tc.graph_panel('4'),
            tc.graph_panel('5')
        ], className='grid grid-cols-2 gap-6 mt-20 mr-20')
    ]
        , className='w-full bg-gray-100 pl-20')
], className='min-h-screen flex flex-row')

if __name__ == '__main__':
    app.run_server(debug=True)
