import plotly.graph_objects as go
import pandas as pd

def conv(s):
    try:
        if s:
            return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return -1

def readfile(data_file):
    data = pd.read_csv(data_file) #, converters={'mom_hash':conv}
    return data

def makeInt(item):
    str_item = None
    if item and item != 'None':
        if isinstance(item, float):
            str_item = str(format(item, '.0f'))
        elif isinstance(item, int):
            str_item = str(item)
    return str_item

# function below sets the color based on amount
def setColor(fitness):
    range = int(format(fitness, '.0f'))
    clr = 'grey'
    if(range > 50):
        clr = "red"
    elif(range >= 10 and range <= 50):
        clr = "yellow"
    elif(range < 10):
        clr = "green"

    if clr == 'grey':
        print(clr)

    return clr

def createNetworkGraph(data):
    node_x = []
    node_y = []
    node_text = []
    node_fitness = []

    for index, row in data.iterrows():
        node_x.append(row["generation"])
        node_y.append(row["i"])
        node_fitness.append(setColor(row['fitness']))

    mom_traces, dad_traces, edge_hover_dict = getNetworkEdges(data)

    for key in edge_hover_dict.keys():
        node_text.append(edge_hover_dict[key])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        text=node_text,
        # marker=dict(
        # showscale=True,
        # # colorscale options
        # #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        # #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        # #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        # colorscale='YlGnBu',
        # reversescale=True,
        # color=[],
        # size=10,
        # colorbar=dict(
        #     thickness=15,
        #     title='Node Connections',
        #     xanchor='left',
        #     titleside='right'
        # )),
        marker=dict(size=1, line_width=1, color=node_fitness),
        #marker = dict(color=list(map(SetColor, y))
        hoverinfo='text'
    )

    fig = go.Figure(data=node_trace,
                 layout=go.Layout(
                    title='Evolution Network Graph',
                    xaxis_title='Generation',
                    yaxis_title='Candidate',
                    titlefont_size=16,
                    plot_bgcolor="#FFFFFF",
                    legend=dict(
                         # Adjust click behavior
                         #itemclick="toggleothers",
                         itemdoubleclick="toggle",
                    ),
                    xaxis=dict(
                        title="time",
                        linecolor="#BCCCDC",
                    ),
                    yaxis=dict(
                        title="price",
                        linecolor="#BCCCDC"
                    ),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40)
                    )
                )

    #Add parent lines.
    for trace in mom_traces:
        fig.add_trace(trace)

    for trace in dad_traces:
        fig.add_trace(trace)

    return fig

def getNetworkEdges(data):
    mom_traces = []
    dad_traces = []
    edge_hover_dict = {}

    generations = data.generation.unique()

    for generation in generations:
        if generation == 0:
            #collect the hover text.
            this_generation_rows = data[data['generation'] == generation]
            for index, row in this_generation_rows.iterrows():
                candidate_value = row["values"]
                candidate_fitness = row["fitness"]
                edge_hover_text = f"Candidate=[{candidate_value}]<br>" \
                                  f"Fitness={candidate_fitness}"
                edge_hover_dict[index] = edge_hover_text
        else:
            try:
                edge_mom_x = []
                edge_mom_y = []
                edge_dad_x = []
                edge_dad_y = []

                prev_generation_rows = data[data['generation'] == (generation - 1)]
                prev_gen_data = {}
                for index, row in prev_generation_rows.iterrows():
                    candidate_hash = makeInt(row["hash"])
                    candidate_hash = f'{candidate_hash}'
                    prev_gen_data[candidate_hash] = row

                this_generation_rows = data[data['generation'] == generation]

                #Generate the edges.
                for index, row in this_generation_rows.iterrows():
                    candidate_value = row["values"]
                    candidate_fitness = row["fitness"]
                    mom_hash = f"{makeInt(row['mom_hash'])}"
                    dad_hash = f"{makeInt(row['dad_hash'])}"

                    edge_hover_text = f"Candidate=[{candidate_value}]<br>" \
                                      f"Fitness={candidate_fitness}"

                    if mom_hash and mom_hash in prev_gen_data.keys():
                        mom_row = prev_gen_data[mom_hash]
                        edge_mom_x.append(generation-1)
                        edge_mom_y.append(mom_row["i"])
                        edge_mom_x.append(generation)
                        edge_mom_y.append(row["i"])
                        edge_hover_text = f"{edge_hover_text}<br>" \
                                          f"Parent1=[{mom_row['values']}]"
                    if dad_hash and (mom_hash != dad_hash) and dad_hash in prev_gen_data.keys():
                        dad_row = prev_gen_data[dad_hash]
                        edge_dad_x.append(generation-1)
                        edge_dad_y.append(dad_row["i"])
                        edge_dad_x.append(generation)
                        edge_dad_y.append(row["i"])
                        edge_hover_text = f"{edge_hover_text}<br>" \
                                          f"Parent2=[{dad_row['values']}]"

                    edge_hover_dict[index] = edge_hover_text

                edge_mom_trace = go.Scatter(
                    x=edge_mom_x, y=edge_mom_y,
                    line=dict(width=0.5, color='red'),
                    hoverinfo='text',
                    mode='lines')

                edge_dad_trace = go.Scatter(
                    x=edge_dad_x, y=edge_dad_y,
                    line=dict(width=0.5, color='blue'),
                    hoverinfo='text',
                    mode='lines')

                mom_traces.append(edge_mom_trace)
                dad_traces.append(edge_dad_trace)
                #fig.add_trace(edge_mom_trace)
                #fig.add_trace(edge_dad_trace)

            except Exception as e:
                print(e)

            #fig.update_traces(mode="markers+lines")
            #fig.update_layout(hovermode="closest")
            #fig.text(edge_hover_text)

    #   pd.reset_option.display

    return mom_traces, dad_traces, edge_hover_dict

def showNetworkGraph(project_name, data):
    fig = createNetworkGraph(project_name, data)
    fig.show()

inspyred_data_folder = "/System/Volumes/Data/Personal/Degree/Tools/Inspyred/Code/Git/inspyred/tanager_data"

if __name__ == '__main__':
    projects = ['Rastrigin','Sphere', 'Ackley', 'Rosenbrock', 'TSM']
    #chart_types = ['BestFit', 'AllGenerations', 'Network']

    #choosen_problem = f'{problem_types[0]}_{chart_types[2]}'
    inspyred_data_folder = "/System/Volumes/Data/Personal/Degree/Tools/Inspyred/Code/Git/inspyred/tanager_data"

    for project in projects:
        #data_filename = f'{inspyred_data_folder}/{project}/tanager-individuals-file.csv'
        print(f"###### Generate Graph {project} ###############")
        #Generate the graph.
        data_filename = f'{inspyred_data_folder}/{project}/tanager-individuals-file.csv'
        data = readfile(data_filename)

        fig = showNetworkGraph(project, data)
        #fig.show()
        #break
        #data_full_path = os.path.realpath(data_filename)
        # print(data_full_path)
        #data = readfile(data_filename)