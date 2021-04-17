#!/usr/bin/env python3
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import argparse
import os
import os.path as path

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import tanager.components as tc
import tanager.plots as tp
import tanager.utils as tu

import json


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

    app = dash.Dash('Tanager', meta_tags=[
        {'name': 'viewport',
         'content': 'width=device-width, initial-scale=1.0'
         }
    ], external_stylesheets=external_stylesheets)

    navbar = populate_nav_bar(projects)

    app.layout = html.Div(children=[
        dcc.Location(id='url', refresh=False),
        tc.navbar(id='experiment-nav', children=navbar),
        # content will be rendered in this element
        html.Div(id='page-content', children=tc.get_default_page(tanager_config), className='w-full bg-gray-100 pl-20')
    ], className='min-h-screen flex flex-row')

    return app


def populate_nav_bar(projects):
    tanager_nav_children = []
    projects.sort()

    for project in projects:
        nav_bar_item = tc.navbar_item(project, href=f'/{project}')
        tanager_nav_children.append(nav_bar_item)

    return tanager_nav_children


# Global Area
tanager_config = None
tangager_data_folder = None
tanager_debug_flag = True

def get_tanager_config():
    global tanager_config
    if not tanager_config:
        config_file = open("./tanager-config.json",'r')
        tanager_config = json.load(config_file)
    return tanager_config

# Create the parser
parser = argparse.ArgumentParser(
    prog='app',
    usage='%(prog)s [options] [dir]',
    description='Tanager - visualize Inspyred evolutionary computations.')

parser.add_argument('-debug', action="store_true", default=False, help="Run in debug mode.")
parser.add_argument('dir', type=str, help="Directory containing observer files.", nargs="?")
args = parser.parse_args()
if args.dir:
    tangager_data_folder = args.dir
else:
    tangager_data_folder = get_tanager_config()['data-folder']

if args.debug:
    tanager_debug_flag = True

if __name__ == '__main__':
    get_tanager_config()
    projects = get_projects(tangager_data_folder)
    app = prepare_dash_server(projects)

    @app.callback(Output('experiment-nav', 'children'),
                  Input('dir-refresh', 'n_clicks'),
                  Input('experiment-filter', 'value'))
    def refresh_onclick(n_clicks, value):
        if value is None:
            filtered_projects = get_projects(tangager_data_folder)
        else:
            filtered_projects = [p for p in get_projects(tangager_data_folder) if value in p]
        return populate_nav_bar(filtered_projects)

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname="/"):
        project_name = pathname.strip('/')
        if project_name and len(project_name) > 0:
            pathname = path.join(path.normpath(tangager_data_folder),
                                 project_name)
            num_generations = tu.num_generations(pathname)
            slider_step = 1
            num_slider_marks = 20
            if num_generations > num_slider_marks:
                slider_step = tu.slider_round(num_generations / num_slider_marks)

            page_layout = html.Div(children=[
                html.H1(f'Project {project_name}', className='text-gray-400 font-bold text-5xl my-10'),
                html.Main(children=[
                    tc.graph_panel(children=[
                        tp.generation_distribution(pathname),
                        html.Div('Select Generation', className='self-start'),
                        dcc.Slider(
                            id='gen-dist-slider',
                            className="w-full",
                            min=0,
                            max=num_generations,
                            step=1,
                            value=0,
                            marks={i: f"{i}" for i in range(0, num_generations + 1, slider_step)}
                        )
                    ]),
                    tc.graph_panel(children=[
                        tp.fitness_vs_generation(pathname),
                    ]),
                    tc.graph_panel(children=[
                        tp.generation_network_graph(project_name, pathname)
                    ], className='col-span-2')
                ], className='grid grid-cols-1 2xl:grid-cols-2 gap-6 mr-20'),
            ], className='w-full bg-gray-100 pl-20')
        else:
            page_layout = tc.get_default_page(tanager_config)
        return page_layout

    app.title = tanager_config['name']
    app.run_server(debug=tanager_debug_flag)
