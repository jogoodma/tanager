#!/usr/bin/env python3
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
import dash_html_components as html
import argparse

import tanager.components as tc
import tanager.plots as tp

# Create the parser
parser = argparse.ArgumentParser(
    prog='app',
    usage='%(prog)s [options] path',
    description='Tanager - visualize Inspyred evolutionary computations.')

parser.add_argument('-debug', action="store_true", default=False, help="Run in debug mode.")
#parser.add_argument('path', type=str, help="Directory containing observer files.")

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
                tp.fitness_vs_generation()
            ]),
            tc.graph_panel(children=[
                tp.generation_distribution()
            ]),
            # Add new plots here as children of graph_panel component
            # Use xl:col-span-2 to force a single column row.
            tc.graph_panel('3', className='xl:col-span-2'),
            tc.graph_panel('4'),
            tc.graph_panel('5')
        ], className='grid grid-cols-1 xl:grid-cols-2 gap-6 mt-20 mr-20')
    ]
        , className='w-full bg-gray-100 pl-20')
], className='min-h-screen flex flex-row')

if __name__ == '__main__':
    args = parser.parse_args()
    app.run_server(debug=args.debug)
