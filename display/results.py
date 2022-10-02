from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd

load_figure_template("flatly")  # darkly

df = pd.DataFrame({
    "words": ["sheida", "devi", "anmol", "Juan", "maiso"],
    "frequency": [1, 2, 5, 2, 1]
})


def build_figure(df):
    figure = px.bar(
        df,
        x='Words',
        y='Frequency',
        template="flatly",  # "darkly",
        width=300,
        height=300,
    )
    figure.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="#375a7f",  # cornflowerblue lightsteelblue steelblue
        font_color = "white",
    )
    return figure


def create_card(title, authors, key_words, relevance, summary, words, full_text_url):  # summary
    df_words = pd.DataFrame(
        {
            "Words":[i[0] for i in words],
            "Frequency":[i[1] for i in words]
        }        
    )
    my_card = dbc.Card(
        # <<<<<<< HEAD
        [
            dbc.CardHeader(html.H4(title, className="card-title")),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(dbc.Col(html.Div(
                                        [
                                            html.B("Authors: "),
                                            ", ".join(authors.split(";")), 
                                        ],
                                        className="card-subtitle"))),
                                    html.Br(),
                                    dbc.Row(dbc.Col(html.Div(
                                        [
                                            html.B("Key Words: "),
                                            ", ".join(key_words.lower().split(";")), 
                                        ],
                                        className="card-subtitle"))),
                                    html.Br(),
                                    # dbc.Row(dbc.Col(html.B("Categories: " + "categories", className="card-subtitle"))),
                                    # html.Br(),
                                    dbc.Row(dbc.Col(
                                        [
                                            html.B("Relevance: "),
                                            str("{:.2f}".format(relevance)),
                                        ],
                                        className="card-subtitle")),
                                    html.Br(),
                                    dbc.Row(dbc.Col(html.P(
                                        [html.B("Abstract: "), summary],
                                        className="card-text",
                                    ))),
                                    html.Br(),
                                    dbc.Row(
                                        [
                                            # dbc.Col(width=9),
                                            dbc.Col(dbc.Button(
                                                "Summary", 
                                                # href="https://google.com",
                                                # href=full_tex,
                                                style={"width": "100%"})),
                                            dbc.Col(dbc.Button(
                                                "Full text", 
                                                # href="https://google.com",
                                                href=full_text_url,
                                                target = "_blank",
                                                style={"width": "100%"})),
                                        ]
                                    )
                                ],
                                width=9,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dcc.Graph(
                                        id='graph',
                                        figure=build_figure(df_words),
                                        style={'border-radius': '15px', 'background-color': '#375a7f'}
                                    ),
                                    style={
                                        'background-color': '#375a7f', 
                                        'padding': '5px', 
                                        'border-radius': '15px', 
                                        # "margin-left":"auto",
                                        # "margin-right":"auto",
                                    },
                                    className = "align-items-center"
                                ),
                                width=3,
                                # align="center"
                            ),
                        ]
                    )
                ]
            ),
        ]
    )
    return my_card
