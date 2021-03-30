import dash_html_components as html


def navbar(*args, **kwargs):
    """

    """
    return html.Div(children=[
        html.Div(children=[
            html.I(className="fab fa-earlybirds"),
            html.Span(children='Tanager', className="font-semibold")
        ], className='mt-8 text-white space-x-5 text-2xl mx-2'),
        html.Nav(*args, className="mt-5", **kwargs)
    ], className='w-52 lg:w-64 bg-gray-900 flex flex-col flex-none text-center'
    )


def navbar_item(*args, **kwargs):
    """

    """
    children = kwargs.pop('children', [])
    children.append(*args)
    children.insert(0, html.I(className='fas fa-chart-bar mx-3'))

    return html.A(className='flex items-center mt-4 py-2 px-6 text-gray-500 hover:bg-gray-700 hover:bg-opacity-25 hover:text-gray-100',
                  children=children,
                  **kwargs
                  )

def graph_panel(*args, **kwargs):
    classname = kwargs.pop('className', '') + ' flex items-center px-5 py-6 shadow-lg rounded-xl bg-white'
    return html.Section(*args, className=classname, **kwargs)