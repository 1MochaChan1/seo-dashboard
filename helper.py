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


def compare(aftr_data, bfr_data):
    compare_map = {} # link -> pos
    for _, rows in bfr_data.iterrows():
        compare_map[rows['Link']] = rows['Position']

    pos_column = []
    for _, rows in aftr_data.iterrows():
        curr_link = rows['Link']
        if(curr_link in compare_map.keys()):
            curr_pos = rows['Position']
            bfr_pos = compare_map[curr_link]
            if(curr_pos < bfr_pos):
                jump = (bfr_pos - curr_pos)
                pos_column.append(f"🔼 +{jump}")
            elif (curr_pos > bfr_pos):
                jump = (curr_pos - bfr_pos)
                pos_column.append(f"🔽 -{jump}")
            else:
                pos_column.append("")
        else:
            pos_column.append("")
    aftr_data['Change'] = pos_column
    return aftr_data