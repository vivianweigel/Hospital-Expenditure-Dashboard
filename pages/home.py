"""
hospital-dash/home.py: home page of app, links to map and comparison pages
Last Modified: December 4, 2022
"""

# import statements
import dash
from dash import html, dcc, callback, Input, Output
import mapper
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# UNIVERSAL VARIABLES
AXIS_COLS = ['Cost of Charity Care','Total Salaries From Worksheet A','Overhead Non-Salary Costs',
             'Total Costs','Inpatient Total Charges','Outpatient Total Charges',
             'Combined Outpatient + Inpatient Total Charges', 'Number of Beds', 'FTE - Employees on Payroll',
             'Total Salaries (adjusted)','Contract Labor','Wage Related Costs for Part - A Teaching Physicians',
             'Wage Related Costs for Interns and Residents','Cash on Hand and in Banks', 'Total Assets',
             'Total Current Liabilities','Mortgage Payable','Total Liabilities and Fund Balances',
             'Managed Care Simulated Payments','Gross Revenue','Net Patient Revenue', 'Total Discharges (V + XVIII + XIX + Unknown)',
             'Net Income from Service to Patients','Total Other Expenses','Net Revenue from Medicaid']
AXIS_COLS.sort()

# general page setup
dash.register_page(__name__, path='/')
loc_df = pd.read_csv('hosp_locs.csv')

# home page layout
layout = html.Div(children=[
    html.H4('Dashboard Details :'),

    #general info sections
    html.Div(className='home_paras', children=[
        html.P('We created the Hospital Data Dashboard to present United States healthcare cost data in an easily '
               'digestible manner for hospital administration individuals. We used Plotly Dash to create the dashboard '
               'and chose a multi-page dashboard to organize the three parts of our work.'),
        html.P('On our homepage, we showcase general visualizations regarding all of the hospitals in our dataset. We '
               'have a map of the United States highlighting Net Income for each hospital, as well as a customizable '
               'scatterplot. Users can choose what they wish to compare on the y-axis against the pre-set x-axis '
               'which remains Net Income.'),
        html.P('On the Hospital Analysis page, we give users an opportunity to filter for a state then select a '
               'specific hospital. Then they can choose to view a pie chart for either costs or income, and gain more '
               'insight into hospital metrics with an associated bar graph.'),
        html.P('Finally, the Hospital Comparison page allows for users to select any two hospitals from our data and '
               'compare their costs and incomes. We also allow for users to toggle between total costs and cost per '
               'bed in order to have more fair comparisons between larger and smaller hospitals.')
    ]),
        
    html.H4('About our Data :'),
    html.A('Data Link', href='https://data.cms.gov/provider-compliance/cost-report/hospital-provider-cost-report/data'),
    html.Div(className='home_paras', children=[
        html.P('The data we are using comes from the Hospital Provider Cost Report dataset from data.CMS.gov (data), '
               'and it provided us the expenditure statements of American hospitals from the 2011-2019 fiscal years, '
               'along with a attributes of each hospital such as salaries of the employees, whether the hospital is '
               'located in a rural or urban area, and the type of care the hospital provides (e.g. cancer, '
               'psychiatric, rehabilitation. The hospitals in this dataset come from across the United States, '
               'with 6,118 hospitals represented in the data.'),
        html.P('Since this is the first rendition of our Hospital Data Dashboard, we chose to only work with the 2019 '
               'data. However, in the future we could like to adapt the tool to house all the data available to us '
               'starting with 2011.')
    ]),

    html.Div(id='home_cols', children=[
        # left graph col
        html.Div(id='left_col', children=[
            html.H4('Map of hospitals across the US'),
            dcc.Graph(
                id='map',
                figure=mapper.create_map(loc_df)),
            html.P('Size of points corresponds to the absolute value of the net income.'
                   '\nColor corresponds to positive or negative net income.')
        ]),

        # right graph col
        html.Div(id='right_col', children=[
            html.H4('Analysis of Hospitals'),
            html.P('Use dropdown to change the y-axis'),
            dcc.Dropdown(id='axis_drop', options=AXIS_COLS, value='Total Costs'),
            html.P('vs. Net Income'),
            dcc.Graph(id='scatter')
        ])
    ]),

    #Acknowledgements and table with extra info
    html.H4('Acknowledgements:'),
    html.Ul(children=[
        html.Li(children=[
            html.A("Plotly Dash", href='https://dash.plotly.com/urls', target="_blank") ]),
        html.Li(children=[
            html.A("Dash Bootstrap Themes", href='https://bootswatch.com/lux/', target="_blank") ]),
        html.Li(children=[
            html.A("Rachlin Lectures", href='https://www.ccs.neu.edu/home/rachlin/python/ds3500/', target="_blank") ]),
        html.Li(children=[
            html.A("Pandas", href='https://pandas.pydata.org/', target="_blank") ]),
        html.Li(children=[
            html.A("Plotly Express", href='https://plotly.com/python/plotly-express/', target="_blank") ]),
        ]),
    html.P('Data Dictionary'),
    html.Img(src='assets/data_dict.jpg', alt='image', id='data_dict'),

])