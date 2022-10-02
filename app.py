import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
from display.results import create_card
# from search_engine.dummy import compute_relevance
from search_engine.whoosh_engine import compute_relevance

body = "Some quick example text to build on the card title and make up the bulk of the card's content."

app = dash.Dash(
    __name__,
    # use_pages = True,
    # external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_stylesheets=[dbc.themes.DARKLY]
    # external_stylesheets=[dbc.themes.CYBORG]
)
app.title = "FIONA"
app.layout = dbc.Container(
    # dbc.Row(
    # dbc.Col(
# app.layout = dbc.Col(
        [
            # dbc.Row(dbc.Col(html.H1('FIONA', style={'textAlign': 'center'}))),
            html.H1('FIONA', style={'textAlign': 'center'}),
            html.H2(
                'Can AI preserve our science legacy?',
                style={'textAlign': 'center'}
            ),
            # dbc.Row(dbc.Col(html.Div('Text Input', style={'textAlign': 'center'}))),
            # ________ search row and it's button ______
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            id="query",
                            placeholder="What are you looking for?",
                            type="text",
                            # value="test query"
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
            # ___________ results container ___________
            dbc.Container(id='results', fluid=True),
            # html.Div(dash.page_container),
        ],
        # style = {"align":"center"}
        #align = "stretch"
    # ),
    # ),
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
        if data.shape[0] > 0 :
        # print(data)
        # print(data.relevance)
            output = [
                create_card(
                    data.iloc[0]["title"],
                    data.iloc[0]["authors"],
                    data.iloc[0]["keywords"],
                    data.iloc[0]["score"],
                    data.iloc[0]["abstract"],
                    data.iloc[0]["high_frequency_words"][:5],
                    data.iloc[0]["pdf_link"],
                ),
                html.Br(),
                create_card(
                    data.iloc[1]["title"],
                    data.iloc[1]["authors"],
                    data.iloc[1]["keywords"],
                    data.iloc[1]["score"],
                    data.iloc[1]["abstract"],
                    data.iloc[1]["high_frequency_words"][:5],
                    data.iloc[1]["pdf_link"],
                    # data.iloc[1]["title"],
                    # "keyword1, keyword2, keyword3",
                    # data.iloc[1]["relevance"],
                    # data.iloc[1]["abstract"],
                ),
                html.Br(),
                create_card(
                    data.iloc[2]["title"],
                    data.iloc[2]["authors"],
                    data.iloc[2]["keywords"],
                    data.iloc[2]["score"],
                    data.iloc[2]["abstract"],
                    data.iloc[2]["high_frequency_words"][:5],
                    data.iloc[2]["pdf_link"],
                ),
                html.Br(),
                create_card(
                    data.iloc[3]["title"],
                    data.iloc[3]["authors"],
                    data.iloc[3]["keywords"],
                    data.iloc[3]["score"],
                    data.iloc[3]["abstract"],
                    data.iloc[3]["high_frequency_words"][:5],
                    data.iloc[3]["pdf_link"],
                ),
                html.Br(),
                create_card(
                    data.iloc[4]["title"],
                    data.iloc[4]["authors"],
                    data.iloc[4]["keywords"],
                    data.iloc[4]["score"],
                    data.iloc[4]["abstract"],
                    data.iloc[4]["high_frequency_words"][:5],
                    data.iloc[4]["pdf_link"],
                ),
                html.Br(),
                create_card(
                    data.iloc[5]["title"],
                    data.iloc[5]["authors"],
                    data.iloc[5]["keywords"],
                    data.iloc[5]["score"],
                    data.iloc[5]["abstract"],
                    data.iloc[5]["high_frequency_words"][:5],
                    data.iloc[5]["pdf_link"],
                ),
            ]
        else:
            output = html.H4("Sorry, we couldn't find any results for this query :(")
    return output


if __name__ == "__main__":
    app.run_server(
        host = "0.0.0.0",
        port=37639,
        debug=True
    )
