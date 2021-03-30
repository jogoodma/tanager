import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


def fitness_vs_generation():
    df = pd.read_csv('data/sample_10i_10g.tsv', sep='\t')
    fig = px.scatter(df, x='generation', y='mean', error_y='stdev', trendline='lowess', title='Fitness vs Generation',
                     labels={'generation': 'Generation', 'mean': 'Fitness'})
    return dcc.Graph(id='fitness_vs_generation', figure=fig, responsive=True, className="h-full w-full")


def generation_distribution():
    df = pd.read_csv('data/sample_10i_10g.tsv', sep='\t')
    fig = ff.create_distplot([df.iloc[9, 1:-2]], ['distplot'], show_rug=False, show_hist=False, curve_type="normal")
    return dcc.Graph(id='generation_distribution', figure=fig, responsive=True, className="h-full w-full")