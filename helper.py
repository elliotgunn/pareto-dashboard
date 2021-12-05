import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_pareto_table_by_product(dataframe, percentile):
    """Returns a modified CSV of the original df
    with cum sum and cum perc.

    Table saved to: data/plotly_data.csv'
    """

    df = dataframe

    # drop unnecessary column
    df = df.drop(columns='customer_id')

    # sort values before calculating cum sum & cum perc
    df = df.sort_values(by=['amount'], ascending=False)
    df['cumulative_sum'] = df.amount.cumsum()
    df['cumulative_perc'] = 100 * df.cumulative_sum / df.amount.sum()

    # make two tables:
    # the first table: once cumulative_perc hits INPUT%
    # the second table: after cumulative_perc hits INPUT%
    top_perc = df.drop(df[df.cumulative_perc > percentile].index)
    bottom_perc = df.drop(df[df.cumulative_perc <= percentile].index)

    # sanity check. did we lose any rows? nope
    # print(len(top_80), len(bottom_20), len(df))

    # collapse bottom_20 into one row:
    # product | amount
    # other   | 10000

    total_amount = bottom_perc['amount'].sum()
    bottom_perc = {'product': 'other', 'amount': total_amount}

    top_perc = top_perc[['product', 'amount']]

    temp_df = top_perc.append(bottom_perc, ignore_index=True)

    # now calculate cum sum & cum perc for new table
    temp_df['cumulative_sum'] = temp_df.amount.cumsum()
    temp_df['cumulative_perc'] = 100 * temp_df.cumulative_sum / temp_df.amount.sum()

    # save to csv!
    temp_df.to_csv('data/plotly_data.csv', index=True)

def pareto_chart(dataframe):
    """
    Reads the pareto table, returns a pareto fig.
    """

    # variables
    cat = 'product'
    num = 'amount'
    title = 'This is a Pareto chart in Plotly'

    trace1 = go.Bar(
        x=dataframe[cat],
        y=dataframe[num],
        name='Amount',
        marker=dict(
            color='rgb(34,163,192)'
        )
    )
    trace2 = go.Scatter(
        x=dataframe[cat],
        y=dataframe['cumulative_perc'],
        name='Cumulative Percentage',
        yaxis='y2'

    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2, secondary_y=True)
    fig['layout'].update(height=600, width=800, title=title, xaxis=dict(
        tickangle=-90
    ))

    return fig