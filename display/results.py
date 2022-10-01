from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd

load_figure_template("flatly") # darkly

df = pd.DataFrame({
    "words": ["sheida", "devi", "anmol", "Juan", "maiso"],
    "frequency": [1, 2, 5, 2, 1]
})


def create_card(title, key_words, summary):
    my_card = dbc.Card(
        [
            dbc.CardHeader(html.H4(title, className="card-title")),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(dbc.Col(html.B("Authors: " + "authors", className="card-subtitle"))),
                                    dbc.Row(dbc.Col(html.B("Key words: "+key_words, className="card-subtitle"))),
                                    dbc.Row(dbc.Col(html.B("Categories: " + "categories", className="card-subtitle"))),
                                    dbc.Row(dbc.Col(html.B("Relevance: " + "relevance", className="card-subtitle"))),
                                    # dbc.Row(dbc.Col(html.P(
                                    #     summary,
                                    #     className="card-text",
                                    # ))),
                                    html.Br(),
                                    dbc.Row(
                                        [
                                            dbc.Col(width=9),
                                            dbc.Col(dbc.Button("Summary", href="https://google.com")),
                                            dbc.Col(dbc.Button("Full text", href="https://google.com")),
                                        ]
                                    )
                                ],
                                width=8,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id='graph',
                                    figure=px.bar(
                                        df,
                                        x='words',
                                        y='frequency',
                                        template="flatly", # "darkly",
                                    ),
                                ),
                                width=4,
                                style={
                                }
                            ),
                        ]
                    )
                ]
            ),
        ]
    )
    return my_card
