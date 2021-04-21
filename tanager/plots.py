import glob as glob
import os.path as path
import sys

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from . import networkgraph as gc
from . import populationplots as pp
import numpy as np

def read_file(pathname, filename, generation_filter):
    df = None
    alt = None
    stats_path = path.join(pathname, filename)
    data_files = glob.glob(stats_path, recursive=False)
    try:
        if len(data_files) >= 1:
            if len(data_files) > 1:
                print(f"More than one statistics file found in {path.dirname(stats_path)}.", file=sys.stderr)
                print("Only one file will be used.", file=sys.stderr)
            file = data_files[0]
            print(f"Reading in {file}")
            all_df = pd.read_csv(file)
            if generation_filter:
                df = all_df[all_df.generation.between(generation_filter[0], generation_filter[1])]
            else :
                df = all_df
        else:
            alt = html.H3(f'No data file found with name {filename}.')
    except IOError as e:
        alt = html.H3(f"ERROR: Caught an IOError while reading {filename}:\n{e}")
    except ValueError as e:
        alt = html.H3(f"ERROR: Caught a ValueError while reading {filename}:\n{e}")
    return df, alt

def get_graph_config():
    config = {
        'displaylogo': False,
        'scrollZoom': True,
        'displayModeBar': True,
        'editable': True,
        'modeBarButtonsToRemove': ['toggleSpikelines',
                                   'hoverCompareCartesian'],
        'sendData': False
    }
    return config

def fitness_vs_generation(pathname: str, generation: tuple = (0, 0), plot_id: str = 'fitness_vs_generation'):
    df, alt = read_file(pathname, 'tanager-statistics-file.csv', None)

    if alt:
        plot_div = alt
    else:
        x = df['generation']
        y = df['average_fit']
        y_upper = y + df['std_fit']
        y_lower = y - df['std_fit']

        fig = go.Figure([
            go.Scatter(
                name='Fitness',
                x=x, y=y,
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(
                name='Upper Bound',
                x=x, y=y_upper,
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='Lower Bound',
                x=x, y=y_lower,
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
            )
        ])
        fig.update_layout(
            yaxis_title='Fitness',
            title='Average Fitness vs Generation',
            hovermode="x"
        )

        plot_div = dcc.Graph(id=plot_id, figure=fig, responsive=True, className="h-full w-full", config=get_graph_config())

    return plot_div

def generation_distribution(pathname: str, generation: int = 0, plot_id: str = 'gen-dist-plot'):
    df, alt = read_file(pathname, 'tanager-individuals-file.csv', None)

    if alt:
        plot_div = alt
    else:
        # Select all individuals for the given generation number.
        fitness_vals = df[df["generation"].isin([generation])]["fitness"]
        # fig = px.histogram(generation_df, x="fitness", show_hist=False, histnorm="probability density")
        fig = ff.create_distplot([fitness_vals], [f"Generation {generation}"], show_rug=True, show_hist=False,
                                 curve_type="normal")
        fig.update_layout(title_text='Fitness Distribution')
        plot_div = dcc.Graph(id=plot_id, figure=fig, responsive=True, className="h-full w-full", config=get_graph_config())

    return plot_div

def generation_network_graph(pathname: str, generation: tuple = (np.NINF, np.inf), plot_id: str = 'gen-network-plot'):
    df, alt = read_file(pathname, 'tanager-individuals-file.csv', generation)

    if alt:
        plot_div = alt
    else:
        fig = gc.createNetworkGraph(df)
        plot_div = dcc.Graph(id=plot_id, figure=fig, responsive=True, className="h-full w-full", config=get_graph_config())

    return plot_div

def plot_ec_population(pathname: str, generation: tuple = (np.NINF, np.inf), plot_id: str = 'ec-population-plot'):
    df, alt = read_file(pathname, 'tanager-individuals-file.csv', generation)

    if alt:
        plot_div = alt
    else:
        fig = pp.plot_ec_population(df)
        plot_div = dcc.Graph(id=plot_id, figure=fig, responsive=True, className="h-full w-full", config=get_graph_config())

    return plot_div


def plot_ec_stats(pathname: str, generation: tuple = (np.NINF, np.inf), plot_id: str = 'ec-population-plot'):
    df, alt = read_file(pathname, 'tanager-statistics-file.csv', generation)

    if alt:
        plot_div = alt
    else:
        fig = pp.plot_ec_stats(df)
        graph = dcc.Graph(id=plot_id,
                          figure=fig,
                          responsive=True,
                          className="h-full w-full",
                          config=get_graph_config())
        plot_div = graph

    return plot_div

def plot_stats_table(pathname: str, num_rows: int=10):
    df, alt = read_file(pathname, 'tanager-statistics-file.csv', None)
    table = ff.create_table(df.head(num_rows))
    #py.iplot(table)

def plot_individual_table(pathname: str, num_rows: int=10):
    df, alt = read_file(pathname, 'tanager-individuals-file.csv', None)
    table = ff.create_table(df.head(num_rows))
    #py.iplot(table)
