"""
hospital-dash/comparison.py: page to compare two hospitals in the US
Last Modified: December 4, 2022
"""

# import statements
import dash
from dash import html, dcc, Dash, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# building the app and general setups
dash.register_page(__name__)

df = pd.read_csv('hosp_cost_report.csv')

# initialize dict to store states and their hospitals for dropdowns
state_hospital_dict = {}
# add hospitals as value to dict
for index, row in df.iterrows():
    # add state as keys and hospital as value to dict
    if row['State Code'] not in state_hospital_dict.keys():
        state_hospital_dict[row['State Code']] = [row['NAME']]
    else:
        state_hospital_dict[row['State Code']].append(row['NAME'])

states = sorted(list(state_hospital_dict.keys()))

layout = html.Div(children=[
    html.H4('Compare two hospitals'),
    html.Div(id='compare_rows', children=[
        # scatterplots to comapare two hospitals
        html.Div(id='compare_cols', children=[
            # left column for left hospital comparison
            html.Div(id='comp_col1', children=[

                # choose state filter
                html.H5('Select a state to filter on'),
                html.Div(id='dropdown1_div', className='dropdown', children=[
                    dcc.Dropdown(id='state_dropdown1',
                                 options=[{'label': state, 'value': state} for state in states],
                                 searchable=True, clearable=True,
                                 placeholder='Select State(s)')
                ]),

                # choose hospital filter
                html.H5('Select Hospital 1 to compare'),
                html.Div(id='dropdown2_div', className='dropdown', children=[
                    dcc.Dropdown(id='hospital_dropdown1',
                                 searchable=True, clearable=True,
                                 placeholder='Select Hospital')
                ]),

            ]),

            # right column for right hospital comparison
            html.Div(id='comp_col2', children=[

                # choose state filter
                html.H5('Select a state to filter on'),
                html.Div(id='dropdown1_div2', className='dropdown', children=[
                    dcc.Dropdown(id='state_dropdown2',
                                 options=[{'label': state, 'value': state} for state in states],
                                 searchable=True, clearable=True,
                                 placeholder='Select State(s)')
                ]),
                # choose hospital filter
                html.H5('Select Hospital 2 to compare'),
                html.Div(id='dropdown2_div2', className='dropdown', children=[
                    dcc.Dropdown(id='hospital_dropdown2',
                                 searchable=True, clearable=True,
                                 placeholder='Select Hospital')
                ]),
            ]),
        ]),
        # graph to compare both hospitals
        html.Div(id='comp_graph_row', children=[
            html.Div(id='comp_graph', children=[
                html.H4('Comparing Income/Costs of Two Hospitals'),
                html.P('Toggle to view Income/Costs'),
                dcc.RadioItems(id='bar2_choice', options=['Costs', 'Income'], value='Costs'),
                dcc.Graph(id='graph3'),
                html.P('Scroll along x-axis to view all categories. '
                       '\nPress Autoscale in the top right of the graph to see all at once')]),
            html.Div(id='comp_graph_buttons', children=[
                dcc.RadioItems(id='per_discharge', options=['Total Costs', 'Costs Per Discharge'], value='Total Costs'),
                html.P(''),
                html.P('When comparing costs, it is important to consider the size and patient volume of both '
                       'hospitals. In order to have a more fair comparison, select “Cost Per Discharge” to view '
                       'metrics in terms of cost per discharge.')])
        ]),
    ]),
])
