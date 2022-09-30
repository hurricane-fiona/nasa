import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Output, Input


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1(children = 'Fiona Dashboard'),
        html.Div(children = 'search and enjoy :)))))'),
        html.Hr(),
        html.Label('Text Input'),
        dcc.Input(type = 'text', id = "text_input"),
        dbc.Button(
            'Run Callback', 
            id = 'button', 
            color = 'primary', 
            style = {'margin-bottom': '1em'}, 
            # block=True
        ),
        html.Br(),
        html.Div(id = 'my-output'),
    ]
)

# @app.callback(
#     Output('my-output', 'figure'),
#     [Input('button', 'n_clicks')],
#     [State('dropdown', 'value'),
#      State('slider',
#            'value')])
# callback for updating graph based on selected dropdown values
@app.callback(
    Output('my-output', 'children'),
    Input('text_input', 'value'))
def update_output_div(input_value):
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
    else:
        return f'Output: {c}'


if __name__ == "__main__":
    app.run_server(
        host = "0.0.0.0",
        port = 37639,
        # debug = True
    )
