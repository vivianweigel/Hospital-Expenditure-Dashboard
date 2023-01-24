"""
hospital-dash/app.py: create plotly dash app
    -all callbacks are on this file
Last Modified: December 4, 2022
"""

# import statements
from dash import Dash, html, dcc, dash_table
import dash
import pandas as pd
import mapper #python file with all graphing functions
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# dash and general page setups
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX])
load_figure_template('SANDSTONE')

df = pd.read_csv('hosp_cost_report.csv')
df_locs = pd.read_csv('hosp_locs.csv')

# initialize dict to store states and their hospitals for dropdowns
state_hospital_dict = {}
# add hospitals as value to dict
for index, row in df.iterrows():
    # add state as keys and hospital as value to dict
    if row['State Code'] not in state_hospital_dict.keys():
        state_hospital_dict[row['State Code']] = [row['NAME']]
    else:
        state_hospital_dict[row['State Code']].append(row['NAME'])

# all states for dropdown list
states = list(state_hospital_dict.keys())

# page navigation bar
navbar = dbc.NavbarSimple( id='navbar',
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Hospital Analysis", href="/solo")),
        dbc.NavItem(dbc.NavLink("Hospital Comparison", href="/comparison")),
    ],
    brand="Hospital Data Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
)

# set upp app
app.layout = html.Div([
    navbar,
    html.Div(id='page_cont', children=[dash.page_container]),

])

# app callback for scatter home page
@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    dash.dependencies.Input('axis_drop', 'value'))
def update_scatter(y_ax):
    fig = mapper.scatter(df, y_ax)
    return fig

# app callback for solo dropdown
@app.callback(
    dash.dependencies.Output('hospital_solo_drop', 'options'),
    dash.dependencies.Input('state_solo_drop', 'value'))
def update_drop(state):
    hosps = sorted(state_hospital_dict[state])
    return [{'label': hosp, 'value': hosp} for hosp in hosps]

# app callback for pie chart viz
@app.callback(
    dash.dependencies.Output('pie_chart', 'figure'),
    dash.dependencies.Input('hospital_solo_drop', 'value'),
    dash.dependencies.Input('pie_choice', 'value'))
def update_pie(hospital, choice):
    fig = mapper.create_pie(df, hospital, choice)
    return fig

# call back to update text blurb
@app.callback(
    dash.dependencies.Output('name', 'children'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_text(hospital):
    return f'Hospital: {hospital}'

# app callback for bed count
@app.callback(
    dash.dependencies.Output('beds', 'children'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_text(hospital):
    df1 = df.loc[(df['NAME'] == hospital)]
    beds = str(df1['Number of Beds'].values[0])
    return f'Number of Beds: {beds}'

# app callback for hospital location
@app.callback(
    dash.dependencies.Output('location', 'children'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_text(hospital):
    df1 = df.loc[(df['NAME'] == hospital)]
    info1 = str(df1['City'].values[0])
    info2 = str(df1['State Code'].values[0])
    return f'Location: {info1}, {info2}'

# app callback for rural or urban hospital
@app.callback(
    dash.dependencies.Output('rvu', 'children'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_text(hospital):
    df1 = df.loc[(df['NAME'] == hospital)]
    info = str(df1['Rural Versus Urban'].values[0])
    return f'Rural(R)/Urban(U)? {info}'

# app callback for number of discharges
@app.callback(
    dash.dependencies.Output('discharges', 'children'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_text(hospital):
    df1 = df.loc[(df['NAME'] == hospital)]
    info = str(df1['Total Discharges (V + XVIII + XIX + Unknown)'].values[0])
    return f'Total Discharges: {info}'

# app callback for charity costs
@app.callback(
    dash.dependencies.Output('charity', 'children'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_text(hospital):
    df1 = df.loc[(df['NAME'] == hospital)]
    info = str(df1['Cost of Charity Care'].values[0])
    return f'Charity Care Cost: {info}'

# app callback for medicaid revenue
@app.callback(
    dash.dependencies.Output('medicare', 'children'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_text(hospital):
    df1 = df.loc[(df['NAME'] == hospital)]
    info = str(df1['Net Revenue from Medicaid'].values[0])
    return f'Net Revenue from Medicaid: {info}'

# app callback for bar graph
@app.callback(
    dash.dependencies.Output('bar', 'figure'),
    dash.dependencies.Input('hospital_solo_drop', 'value'))
def update_bar_chart(hospital):
    fig = mapper.bar_chart(df, hospital)
    return fig

# app callback for first dropdown
@app.callback(
    dash.dependencies.Output('hospital_dropdown1', 'options'),
    dash.dependencies.Input('state_dropdown1', 'value'))
def update_drop(state):
    hosps = sorted(state_hospital_dict[state])
    return [{'label': hosp, 'value': hosp} for hosp in hosps]

# app callback for second dropdown
@app.callback(
    dash.dependencies.Output('hospital_dropdown2', 'options'),
    dash.dependencies.Input('state_dropdown2', 'value'))
def update_drop(state):
    hosps = sorted(state_hospital_dict[state])
    return [{'label': hosp, 'value': hosp} for hosp in hosps]

# app callback for double-dropdown
@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    dash.dependencies.Input('hospital_dropdown1', 'value'),
    dash.dependencies.Input('hospital_dropdown2', 'value'),
    dash.dependencies.Input('bar2_choice', 'value'),
    dash.dependencies.Input('per_discharge', 'value'))
def update_bar_chart(hospital1, hospital2, choice, per_discharge):
    fig = mapper.double_bar_chart(df, hospital1, hospital2, choice, per_discharge)
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

