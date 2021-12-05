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

from helper import make_pareto_table_by_product, pareto_chart, pareto_analysis_by_product

app = dash.Dash(__name__)

# layout: describes what the application looks like
app.layout = html.Div(children=[
    html.H1(children='Pareto Data Science'),

    html.Div(children='''
        Performing Pareto analysis on your data.
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
    df0 = pd.read_csv('data/sample.csv', index_col=0)

    # df = pd.read_csv('data/sample.csv', index_col=0)
    df = df0.copy()

    # create pareto table as new csv file
    make_pareto_table_by_product(df, percentile)

    # read new csv
    temp_df = pd.read_csv('data/plotly_data.csv', index_col=0)

    # create pareto chart
    # this function returns a fig directly
    # the temp_df is for the chart
    # the df and percentile are to update the title
    return pareto_chart(temp_df, df, percentile)

if __name__ == '__main__':
    app.run_server(debug=True)