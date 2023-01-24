"""
hospital-dash/map: page to explore hospitals in the US
Last Modified: December 4, 2022
"""

# import statements
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mapper

# dash and general set up
dash.register_page(__name__)
df = pd.read_csv('hosp_cost_report.csv')
loc_df = pd.read_csv('hosp_locs.csv')

# initialize dict to store states and their hospitals for dropdowns
state_hospital_dict = {}
# add hospitals as value to dict
for index, row in df.iterrows():
    # add state as keys and hospital as value to dict
    if row['State Code'] not in state_hospital_dict.keys():
        state_hospital_dict[row['State Code']] = [row['NAME']]
    else:
        state_hospital_dict[row['State Code']].append(row['NAME'])

# states for dropdown lists
states = sorted(list(state_hospital_dict.keys()))

layout = html.Div(children=[

    # text for dropdown
    html.Div(children='''
        Select a hospital to investigate.
    '''),

    html.Div(id='solo_cols', children=[
        # left column
        html.Div(id='col1', children=[
            # choose state filter
            html.Div(id='solodrop_div', className='dropdown', children=[
                html.H5('Select a state to filter on'),
                dcc.Dropdown(id='state_solo_drop',
                             options=[{'label': state, 'value': state} for state in states],
                             searchable=True, clearable=True,
                             placeholder='Select State(s)')
            ]),

            # choose hospital filter
            html.Div(id='solodrop2_div', className='dropdown', children=[
                html.H5('Select Hospital'),
                dcc.Dropdown(id='hospital_solo_drop',
                             searchable=True, clearable=True,
                             placeholder='Select Hospital')
            ]),

            #pie chart
            html.H4('Costs vs Income'),
            dcc.RadioItems(id='pie_choice', options=['Costs', 'Income'], value='Costs'),
            html.P('Note that 0% figures are likely values that go unreported by the hospital'),
            dcc.Graph(
                id='pie_chart',
            ),
        ]),

        # right column
        html.Div(id='col2', children=[
            html.Div(id='name', children=[]),
            html.Div(id='info', children=[
                html.Div(id='location', children=[]),
                html.Div(id='beds', children=[]),
                html.Div(id='rvu', children=[]),
                html.Div(id='discharges', children=[]),
                html.Div(id='charity', children=[]),
                html.Div(id='medicare', children=[]),
            ]),
            html.Div(id='bar_sect', children=[
                dcc.Graph(
                    id='bar',
                )
            ])

        ])
    ])

])