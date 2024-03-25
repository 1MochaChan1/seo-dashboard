import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Color:
    red = "#623333"
    green = "#314E37"
    grey = 'grey'

def make_table(csv:pd.DataFrame):
    fig = go.Figure(
        data=go.Table(
            header=dict(
                values=csv.columns.to_list()), 
                cells=dict(values=[csv[x].values.tolist() for x in csv.columns.to_list()])))
    
    return fig


def colorize(_:pd.Series, df:pd.DataFrame):
    colors = []
    for status in df['Status']:
        if(status == 'Negative'):
            colors.append(f'background-color: {Color.red}')
        elif (status == 'Positive'):
            colors.append(f'background-color:  {Color.green}')
        else:
            colors.append('')
    return colors


def compare(a_data, b_data):
    compare_map = {}
    for _, rows in b_data.iterrows():
        compare_map[rows['Link']] = rows['Position']

    pos_column = []
    for _, rows in a_data.iterrows():
        curr_link = rows['Link']
        if(curr_link in compare_map.keys()):
            curr_pos = rows['Position']
            if(curr_pos < compare_map[curr_link]):
                pos_column.append("🔼")
            elif (curr_pos > compare_map[curr_link]):
                pos_column.append("🔽")
            else:
                pos_column.append("")
        else:
            pos_column.append("")
    a_data['Change'] = pos_column
    return a_data