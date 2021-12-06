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


markdown_text = '''
#### What is Pareto analysis/the Pareto principle/the 80-20 rule?
It has been widely observed that 80% of consequences come from 20% of causes. 
In business, this generally translates to 80% of revenue coming from 20% of clients.

#### Why Pareto for data science?
Real world data commonly follow a power law distribution. As [Vicki Boykis explained](https://veekaybee.github.io/2021/03/26/data-ghosts/), "There are both statistical and business implications for how you deal with this rule. In particular, it means that paying attention to tail-end phenomena is just as as important as understanding an “average” user."

This phenomenon isn't well covered in formal study. And it's [hard to find accessible resources online](https://twitter.com/vboykis/status/1375954010600054785)! 

#### How does this app work?
I created this web app to provide a template for thinking through and visualizing Pareto distributions.
It's difficult to understand how unique power law distributions are until you encounter one.
The data has been synthetically generated from a power law distribution for demonstration purposes.
The default Pareto value has been set to to 80%. You can change this to any number between 0 and 100% to see how the chart changes.

As the total number of products is more than 1000, I bucketed the products that did not make the percentile cutoff as OTHER to make the x-axis less crowded.

#### Github repo
Accessible [here](https://github.com/elliotgunn/pareto-dashboard).
'''

# layout: describes what the application looks like
app.layout = html.Div(children=[
    html.H1(children='Pareto Data Science'),

    html.Div(children='''
        A Plotly Dash app that runs a quick Pareto-style analysis.
 
    '''),

    dcc.Markdown(children=markdown_text),
    dcc.Graph(id='pareto-chart-by-product'),
    dcc.Input(id='percentile', type='number', min=1, max=100, step=1, value=80),

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