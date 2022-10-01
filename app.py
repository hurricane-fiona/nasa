import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
from display.results import create_card 

body = "Some quick example text to build on the card title and make up the bulk of the card's content."

app = dash.Dash(
    __name__, 
    # use_pages = True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1('FIONA'))),
        dbc.Row(dbc.Col(html.H2('Can AI preserve our science legacy?'))),
        # dbc.Row(dbc.Col(html.Div('Text Input', style={'textAlign': 'center'}))),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Textarea(
                        id="query",
                        placeholder="Search"
                    ),
                    width = 9
                ),
                # dbc.Col(dbc.Input(id="text_input", type="search", placeholder="Search")),
                dbc.Col(
                    dbc.Card(
                        dbc.Button(
                            # "Search",
                            'Search',
                            id='search',
                            # color="primary", className="ms-2", n_clicks=0
                        ),
                    ),
                    # width="auto",
                    # align = "stretch"
                )
            ],
            # className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        ),
        html.Br(),
        # html.Div(id='my-output'),
        dbc.Container(id='results', fluid = True),
        # html.Div(dash.page_container),
    ],
    fluid=True
)

@app.callback(
    Output('results', 'children'),
    [Input('search', 'n_clicks')],
    [State('query', 'value')]
)
def show_results(n_clicks, input_value):
    # a = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural " \
    #     "intelligence displayed by animals and humans."
    # b = "Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', " \
    #     "that is, methods that leverage data to improve"
    # c = "Deep learning is part of a broader family of machine learning methods based on artificial neural networks " \
    #     "with representation learning."
    # if input_value == 'AI':
    #     return f'Output: {a}'
    # elif input_value == 'ML':
    #     return f'Output: {b}'
    # elif input_value and input_value.lower() == "hola":
    #     return "Hola Sandri :)   Atentamente, Juan"
    # else:
    #     return f'Output: {c}'
    output = None
    if input_value:
        output = [
            dbc.Row(
                [
                    dbc.Col(
                        create_card("Title 1", "keyword1, keyword2, keyword3", body)
                    ), 
                    dbc.Col( 
                        create_card("Title 2", "keyword1, keyword2, keyword3", body)
                    ),
                    dbc.Col(
                        create_card("Title 3", "keyword1, keyword2, keyword3", body)
                    ),
                ],
                # className = "g-0"
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col( 
                        create_card("Title 4", "keyword1, keyword2, keyword3", body)
                    ),
                    dbc.Col( 
                        create_card("Title 5", "keyword1, keyword2, keyword3", body)
                    ),
                    dbc.Col(
                        create_card("Title 6", "keyword1, keyword2, keyword3", body)
                    )
                ],
                # className = "g-0"
            ),
        ]
    return output


if __name__ == "__main__":
    app.run_server(
        # host = "0.0.0.0",
        port=37639,
        debug=True
    )
