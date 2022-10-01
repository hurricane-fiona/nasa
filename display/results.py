from dash import html
import dash_bootstrap_components as dbc


def create_card(title, key_words, relevance, summary):
    my_card = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(dbc.Col(html.H4(title, className="card-title"))),
                html.Br(),
                dbc.Row(dbc.Col(html.B(key_words, className="card-subtitle"))),
                html.Br(),
                dbc.Row(dbc.Col(f"Relevance: {relevance:.3f}")),
                html.Br(),
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
    )
    return my_card
