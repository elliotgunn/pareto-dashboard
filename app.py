# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from helper import make_pareto_table_by_product, pareto_chart

app = dash.Dash(__name__)

# layout: describes what the application looks like
app.layout = html.Div(children=[
    html.H1(children='Pareto Data Science'),

    html.Div(children='''
        Performing pareto analysis on your data.
    '''),

    dcc.Graph(id='pareto-chart-by-product'),
    dcc.Input(id='percentile', type='number', min=1, max=100, step=1, value=80)
])

@app.callback(
    Output('pareto-chart-by-product', 'figure'),
    Input('percentile', 'value')
)
def update_graph(percentile):
    # read original df and make copy
    df = pd.read_csv('data/sample.csv', index_col=0)

    # df = pd.read_csv('data/sample.csv', index_col=0)
    df2 = df.copy()

    # create pareto table as new csv file
    make_pareto_table_by_product(df2, percentile)

    # read new csv
    temp_df = pd.read_csv('data/plotly_data.csv', index_col=0)

    # create pareto chart
    # this function returns a fig directly
    return pareto_chart(temp_df)

if __name__ == '__main__':
    app.run_server(debug=True)