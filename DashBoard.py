import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1(children='Fiona Dashboard'))),
        dbc.Row(dbc.Col(html.Div('Text Input', style={'textAlign': 'center'}))),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Textarea(
                        id="text_input",
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.Button(
                            'Run Callback',
                            id='button',
                            color='primary',
                            # style={'margin-bottom': '1em'},
                            # block=True
                        ),
                    ),
                )
            ],
            align="center"
        ),
        html.Br(),
        html.Div(id='my-output'),
    ],
    fluid=True
)


@app.callback(
    Output('my-output', 'children'),
    [Input('button', 'n_clicks')],
    [State('text_input', 'value')]
)
def update_output_div(n_clicks, input_value):
    a = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural " \
        "intelligence displayed by animals and humans."
    b = "Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', " \
        "that is, methods that leverage data to improve"
    c = "Deep learning is part of a broader family of machine learning methods based on artificial neural networks " \
        "with representation learning."
    if input_value == 'AI':
        return f'Output: {a}'
    elif input_value == 'ML':
        return f'Output: {b}'
    elif input_value and input_value.lower() == "hola":
        return "Hola Sandri :)   Atentamente, Juan"
    else:
        return f'Output: {c}'


if __name__ == "__main__":
    app.run_server(
        # host = "0.0.0.0",
        port=37639,
        debug=True
    )
