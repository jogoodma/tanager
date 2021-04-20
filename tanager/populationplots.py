import plotly.graph_objects as go
import plotly.express as px

def get_line_plot(data, generation, candidate, label, line_color, line_size):
    scatter_plot = go.Scatter(x=generation, y=data[label], mode='markers+lines',
                              name=label,
                              text=candidate,
                              hoverinfo='text',
                              line=dict(color=line_color, width=line_size))
    return scatter_plot

def plot_ec_stats(data):
    title = 'Fitness over Generations'
    labels = ['best_fit', 'average_fit', 'median_fit']
    colors = ['rgb(49,130,189)','rgb(189,189,189)','rgb(67,67,67)', 'rgb(115,115,115)']

    generation = data["generation"]
    candidate = data['best_fit_candidate_hash']

    mode_size = [8, 8, 12, 8]
    line_size = [3, 1, 1, 2]

    fig = go.Figure()

    for i in range(0, len(labels)):
        fig.add_trace(get_line_plot(data, generation, candidate, labels[i], colors[i], line_size[i]))

    # Edit the layout
    fig.update_layout(title=title,
                      xaxis_title='Generation',
                      yaxis_title='Fitness')

    return fig

def plot_ec_population(data):
    # fig = px.scatter(data, x="generation", y="fitness",
    #                  color="i",
    #                  hover_name="values",
    #                  size="fitness",
    #                  size_max=10)

    fig = px.scatter(data, x="fitness", y="i",
                     color="generation",
                     hover_name="values",
                     size="fitness",
                     size_max=10)

    fig.update_layout(title=f"Population Fitness",
                      xaxis_title='Fitness',
                      yaxis_title='')
    return fig

import pandas as pd

def readfile(data_file):
    data = pd.read_csv(data_file) #, converters={'mom_hash':conv}
    return data

inspyred_data_folder = "/System/Volumes/Data/Personal/Degree/Tools/Inspyred/Code/Git/inspyred/tanager_data"

if __name__ == '__main__':
    projects = ['Sphere'] #,'Rastrigin', 'Ackley', 'Rosenbrock', 'TSM']
    #chart_types = ['BestFit', 'AllGenerations', 'Network']

    #choosen_problem = f'{problem_types[0]}_{chart_types[2]}'
    inspyred_data_folder = "/System/Volumes/Data/Personal/Degree/Tools/Inspyred/Code/Git/inspyred/tanager_data"

    for project in projects:
        #data_filename = f'{inspyred_data_folder}/{project}/tanager-individuals-file.csv'
        print(f"###### Generate Graph {project} ###############")
        #Generate the Polulation plot.
        data_filename = f'{inspyred_data_folder}/{project}/tanager-individuals-file.csv'
        data = readfile(data_filename)

        fig = plot_ec_population(project, data)
        fig.show()

        #Generate the stats plot
        data_filename = f'{inspyred_data_folder}/{project}/tanager-statistics-file.csv'
        data = readfile(data_filename)

        fig = plot_ec_stats(project, data)
        fig.show()

        #break
        #data_full_path = os.path.realpath(data_filename)
        # print(data_full_path)
        #data = readfile(data_filename)