import dash_core_components as dcc
import dash_html_components as html


def navbar(*args, **kwargs):
    """

    """

    return html.Div(children=[
        html.Div(children=[
            dcc.Link(href="/", children=[
                html.I(className="fab fa-earlybirds mr-3"),
                html.Span(children='Tanager', className="font-semibold")
            ]),
        ], className='mt-8 text-white space-x-5 text-2xl mx-2'),
        html.Div(children=[
            dcc.Input(
                id="experiment-filter",
                name="experiment-filter",
                type="text",
                placeholder="Filter by name",
                className="w-2/3 focus:ring-4 focus:ring-blue-300 py-2 px-4 rounded-full",
            ),
            html.Button(id='dir-refresh', className='text-white active:text-blue-500', title="Refresh expreiment list",
                        children=[
                            html.I(className='fas fa-redo-alt')
                        ]),
        ], className='flex justify-around my-4'),
        html.Nav(*args, className="overflow-y-auto h-5/6", **kwargs)
    ], className='w-52 lg:w-64 bg-gray-900 flex flex-col flex-none text-center h-screen'
    )


def navbar_item(*args, **kwargs):
    """

    """
    children = kwargs.pop('children', [])
    children.append(*args)
    children.insert(0, html.I(className='fas fa-chart-bar mx-3'))

    return dcc.Link(
        className='flex items-center py-2 px-6 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
        children=children,
        **kwargs
    )


def graph_panel(*args, **kwargs):
    classname = kwargs.pop('className', '') + ' flex flex-col items-center px-5 py-6 shadow-lg rounded-xl bg-white'
    return html.Section(*args, className=classname, **kwargs)


def get_default_page(config):
    return html.Div(children=[
        html.H1(config['title'], className="text-6xl font-bold alert-heading"),
        html.H2(
            config['description'],  # "Tanager allows you to visualize Inspyred. "
            className='text-2xl text-gray-400 ml-10'
        ),
        html.Hr(className='border border-black'),
        html.P(
            "Please select the project from the left navigation to get started",
            className="mb-0",
        )
    ], className='mt-40'
    )
