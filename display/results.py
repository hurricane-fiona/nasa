from dash import html
import dash_bootstrap_components as dbc

def article(
    title = "title",
    keywords = ["a", "b", "c"],
    text = "testing text",
    pdf = "file.pdf"
):
    output = dbc.Col(
        [
            title,
            html.Div(keywords),
            text,
            pdf
        ]
    )
    return output

