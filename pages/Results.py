import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State


def create_card(title, key_words, summary):
    my_card = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(dbc.Col(html.H4(title, className="card-title"))),
                html.Br(),
                dbc.Row(dbc.Col(html.H6(key_words, className="card-subtitle"))),
                dbc.Row(dbc.Col(html.P(
                    summary,
                    className="card-text",
                ))),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(),
                        dbc.Col(dbc.Button("Summary", href="https://google.com")),
                    ]
                )
            ]
        ),
        style={"width": "18rem"},
    )
    return my_card


body = "Some quick example text to build on the card title and make up the bulk of the card's content."

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    'Here is the results',
                    style={
                        'textAlign': 'center'}
                )
            )
        ),
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
            className="mb-4",
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
            className="mb-4",
        ),
    ],
    fluid=True
)

if __name__ == "__main__":
    app.run_server(
        # host = "0.0.0.0",
        port=37639,
        debug=True
    )
