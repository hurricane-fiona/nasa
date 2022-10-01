from dash import html
import dash_bootstrap_components as dbc


def create_card(title, key_words, summary):
    my_card = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(dbc.Col(html.H4(title, className="card-title"))),
                html.Br(),
                dbc.Row(dbc.Col(html.B(key_words, className="card-subtitle"))),
                dbc.Row(dbc.Col(html.P(
                    summary,
                    className="card-text",
                ))),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(dbc.Button("Summary", href="https://google.com")),
                    ]
                )
            ]
        ),
        # style={"width": "9rem"},
    )
    return my_card
