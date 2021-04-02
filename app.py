#!/usr/bin/env python3
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import argparse
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

import tanager.components as tc
import tanager.plots as tp


def get_projects(path: str):
    projects = []
    if os.path.exists(path):
        directory_contents = os.listdir(path)
        for item in directory_contents:
            item_path = f'{path}/{item}'
            if os.path.isdir(item_path):
                projects.append(item)
    return projects


def prepare_dash_server(projects):
    external_stylesheets = [
        "https://use.fontawesome.com/releases/v5.15.3/css/all.css"
    ]

    app = dash.Dash(__name__, meta_tags=[
        {'name': 'viewport',
         'content': 'width=device-width, initial-scale=1.0'
         }
    ], external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        dcc.Location(id='url', refresh=False),
        tc.navbar(children=tanager_nav_children),
        # content will be rendered in this element
        html.Div(id='page-content', className='w-full bg-gray-100 pl-20')
    ], className='min-h-screen flex flex-row')

    return app


def load_tanager_layouts():
    tanager_layouts['default'] = html.Div(children=
    [
        html.H1("Welcome to Tanager!", className="text-6xl font-bold alert-heading"),
        html.H2(
            "Tanager allows you to visualize Inspyred. ",
            className='text-2xl text-gray-400 ml-10'
        ),
        html.Hr(className='border border-black'),
        html.P(
            "Please select the project from the left navigation to get started",
            className="mb-0",
        )
    ], className='mt-40'
    )

    tanager_layouts['Rastrigin'] = html.Div(children=[
        html.Main(children=[
            tc.graph_panel(children=[
                tp.generation_distribution('Rastrigin')
            ]),
            tc.graph_panel(children=[
                tp.fitness_vs_generation('Rastrigin')
            ])
        ], className='grid grid-cols-2 gap-6 mt-20 mr-20')
    ], className='w-full bg-gray-100 pl-20')

    tanager_layouts['Polygon'] = html.Div(children=[
        html.Main(children=[
            tc.graph_panel(children=[
                tp.generation_distribution('Polygon')
            ]),
            tc.graph_panel(children=[
                tp.fitness_vs_generation('Polygon')
            ]),
            tc.graph_panel('3'),
            tc.graph_panel('4')
        ], className='grid grid-cols-2 gap-6 mt-20 mr-20')
    ], className='w-full bg-gray-100 pl-20')

    return


# Global Area
# Create the parser
parser = argparse.ArgumentParser(
    prog='app',
    usage='%(prog)s [options] dir',
    description='Tanager - visualize Inspyred evolutionary computations.')

parser.add_argument('-debug', action="store_true", default=False, help="Run in debug mode.")
parser.add_argument('dir', type=str, help="Directory containing observer files.")
args = parser.parse_args()

projects = get_projects(args.dir)
tanager_nav_children = []
tanager_layouts = {}

for project in projects:
    nav_bar_item = tc.navbar_item(project, href=f'/{project}')
    tanager_nav_children.append(nav_bar_item)

if __name__ == '__main__':
    load_tanager_layouts()
    app = prepare_dash_server(projects)


    @app.callback(dash.dependencies.Output('page-content', 'children'),
                  [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname="/"):
        # ctx = dash.callback_context
        # triggeredred_by = ctx.triggered[0].get("prop_id")

        layout_name = pathname.strip('/')
        if layout_name is not None and layout_name in tanager_layouts:
            page_layout = tanager_layouts[layout_name]
        else:
            page_layout = tanager_layouts['default']

        return page_layout


    app.run_server(debug=args.debug)
