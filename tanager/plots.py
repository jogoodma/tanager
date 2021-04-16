import glob as glob
import os.path as path
import sys

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


def fitness_vs_generation(basedir, project_name):
    stats_path = path.join(path.normpath(basedir), project_name, 'tanager-statistics-file-*.csv')
    data_files = glob.glob(stats_path, recursive=False)
    try:
        if len(data_files) >= 1:
            if len(data_files) > 1:
                print(f"More than one statistics file found in {path.dirname(stats_path)}.", file=sys.stderr)
                print("Only one file will be used.", file=sys.stderr)
            file = data_files[0]
            print(f"Reading in {file}")
            df = pd.read_csv(file)
            fig = px.scatter(df, x='num_generations', y='average_fit', error_y='std_fit', trendline='lowess',
                             title='Fitness vs Generation',
                             labels={'num_generations': 'Generation', 'average_fit': 'Fitness'})
            return dcc.Graph(id='fitness_vs_generation', figure=fig, responsive=True, className="h-full w-full")
        else:
            print(f"No stats files found in {path.dirname(stats_path)}", file=sys.stderr)
    except IOError as e:
        return html.H3(f"ERROR: Caught an IOError while reading {file}:\n{e}")
    except ValueError as e:
        return html.H3(f"ERROR: Caught a ValueError while reading {file}:\n{e}")
    return html.H3(f'Error reading stats file.')


def generation_distribution(project_name):
    # print(request.host_url)
    print(project_name)
    df = pd.read_csv('data/experiment_1/sample_10i_10g.tsv', sep='\t')
    fig = ff.create_distplot([df.iloc[9, 1:-2]], ['distplot'], show_rug=False, show_hist=False, curve_type="normal")
    return dcc.Graph(id='generation_distribution', figure=fig, responsive=True, className="h-full w-full")
