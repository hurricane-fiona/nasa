import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
from display.results import create_card
from search_engine.dummy import compute_relevance

body = "Some quick example text to build on the card title and make up the bulk of the card's content."

app = dash.Dash(
    __name__,
    # use_pages = True,
    # external_stylesheets=[dbc.themes.BOOTSTRAP],
    # external_stylesheets=[dbc.themes.CYBORG],
    external_stylesheets=[dbc.themes.DARKLY]
)

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1('FIONA', style={'textAlign': 'center'}))),
        dbc.Row(dbc.Col(html.H2('Can AI preserve our science legacy?'))),
        # dbc.Row(dbc.Col(html.Div('Text Input', style={'textAlign': 'center'}))),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Input(
                        id="query",
                        placeholder="Search",
                        type="text",
                        value = "test query"
                    ),
                    width=9
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.Button(
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
        dbc.Container(id='results', fluid=True),
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
    output = None
    if input_value:
        data = compute_relevance(input_value).head(6)
        # print(data)
        # print(data.relevance)
        output = [
            dbc.Row(
                [
                    dbc.Col(
                        create_card(
                            data.iloc[0]["title"],
                            "keyword1, keyword2, keyword3", 
                            data.iloc[0]["relevance"],
                            data.iloc[0]["abstract"],
                        )
                    ),
                    dbc.Col(
                        create_card(
                            data.iloc[1]["title"],
                            "keyword1, keyword2, keyword3", 
                            data.iloc[1]["relevance"],
                            data.iloc[1]["abstract"],
                        )
                    ),
                    dbc.Col(
                        create_card(
                            data.iloc[2]["title"],
                            "keyword1, keyword2, keyword3", 
                            data.iloc[2]["relevance"],
                            data.iloc[2]["abstract"],
                        )
                    ),
                ],
                # className = "g-0"
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        create_card(
                            data.iloc[3]["title"],
                            "keyword1, keyword2, keyword3", 
                            data.iloc[3]["relevance"],
                            data.iloc[3]["abstract"],
                        )
                    ),
                    dbc.Col(
                        create_card(
                           data.iloc[4]["title"],
                           "keyword1, keyword2, keyword3", 
                           data.iloc[4]["relevance"],
                           data.iloc[4]["abstract"],
                        )
                    ),
                    dbc.Col(
                        create_card(
                           data.iloc[5]["title"],
                           "keyword1, keyword2, keyword3", 
                           data.iloc[5]["relevance"],
                           data.iloc[5]["abstract"],
                        )
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
