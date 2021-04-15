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

from dash.dependencies import Input, Output


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

    navbar = populate_nav_bar(projects)

    app.layout = html.Div(children=[
        dcc.Location(id='url', refresh=False),
        tc.navbar(id='experiment-nav', children=navbar),
        # content will be rendered in this element
        html.Div(id='page-content', children=tc.get_default_page(), className='w-full bg-gray-100 pl-20')
    ], className='min-h-screen flex flex-row')

    return app


def get_tanager_layouts():
    tanager_layouts = {}

    tanager_layouts['Project'] = html.Div(children=[
        html.Main(children=[
            tc.graph_panel(children=[
                tp.generation_distribution('Rastrigin')
            ]),
            tc.graph_panel(children=[
                tp.fitness_vs_generation('Rastrigin')
            ])
        ], className='grid grid-cols-2 gap-6 mt-20 mr-20'),
        html.Div(children=[
            tc.graph_panel(children=[
                tp.generate_nework_graph('Rastrigin')
            ])], className='gap-6')
    ], className='w-full bg-gray-100 pl-20')

    return tanager_layouts


def populate_nav_bar(projects):
    tanager_nav_children = []
    projects.sort()

    for project in projects:
        nav_bar_item = tc.navbar_item(project, href=f'/{project}')
        tanager_nav_children.append(nav_bar_item)

    return tanager_nav_children


# Global Area
# Create the parser
parser = argparse.ArgumentParser(
    prog='app',
    usage='%(prog)s [options] dir',
    description='Tanager - visualize Inspyred evolutionary computations.')

parser.add_argument('-debug', action="store_true", default=False, help="Run in debug mode.")
parser.add_argument('dir', type=str, help="Directory containing observer files.")
args = parser.parse_args()

if __name__ == '__main__':
    projects = get_projects(args.dir)
    app = prepare_dash_server(projects)

    @app.callback(Output('experiment-nav', 'children'),
                  Input('dir-refresh', 'n_clicks'),
                  Input('experiment-filter', 'value'))
    def refresh_onclick(n_clicks, value):
        if value is None:
            filtered_projects = get_projects(args.dir)
        else:
            filtered_projects = [p for p in get_projects(args.dir) if value in p]
        return populate_nav_bar(filtered_projects)

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname="/"):
        ctx = dash.callback_context
        # triggered_by = ctx.triggered[0].get("prop_id")

        project_name = pathname.strip('/')
        print(f'Project={project_name}')
        if project_name:
            page_layout = html.Div(children=[
                html.Main(children=[
                    'hi here'
                    # tc.graph_panel(children=[
                    #     tp.generation_distribution(project_name)
                    # ]),
                    # tc.graph_panel(children=[
                    #     tp.fitness_vs_generation(project_name)
                    # ])
                ], className='grid grid-cols-2 gap-6 mt-20 mr-20'),
                html.Div(children=[
                    'hi there'
                    # tc.graph_panel(children=[
                    #     tp.generate_nework_graph(project_name)
                    # ])
                ], className='gap-6')
            ], className='w-full bg-gray-100 pl-20')
        else:
            page_layout = tc.get_default_page()
        return page_layout


    app.run_server(debug=args.debug)
