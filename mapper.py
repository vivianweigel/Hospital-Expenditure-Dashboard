"""
mapper.py - code to create the map and other graphs
Last Modified: December 4, 2022
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# defining columns needed for certain graphs
COSTS = ['Cost of Charity Care', 'Total Bad Debt Expense', 'Cost of Uncompensated Care',
         'Total Unreimbursed and Uncompensated Care', 'Overhead Non-Salary Costs',
         'Depreciation Cost', 'Wage-Related Costs (Core)', 'Wage-Related Costs (RHC/FQHC)',
         'Total Salaries (adjusted)', 'Contract Labor', 'Wage Related Costs for Part - A Teaching Physicians',
         'Wage Related Costs for Interns and Residents', 'Inventory', 'Investments',
         'Total Other Expenses']

INCOME = ['Total Assets', 'Inpatient Revenue', 'Outpatient Revenue',
          'Net Income from Service to Patients', 'Total Other Income',
          'Total Income', 'Net Revenue from Medicaid']

MAIN = ['Net Income', 'Total Costs', 'Net Patient Revenue']


def create_map(df):
    """
    creates the map
    :param df: pandas hospital df including location data
    :return:
    """
    # Plotting using plotly
    # Inputting token
    # mapping with changing color
    pd.options.plotting.backend = 'plotly'
    px.set_mapbox_access_token(
        'pk.eyJ1Ijoid2VpZ2Vsdml2aWFuIiwiYSI6ImNsMXdhYjVrcjBiZ3AzZWxtczZjNHd6OGIifQ.tc-vqaSVnexmAp1s9ocCUw')

    # mapping with changing size of the points
    fig = px.scatter_mapbox(df, lat='LATITUDE', lon="LONGITUDE",
                            hover_data=["City", "State Code", "Net Income"],
                            hover_name="NAME_x",
                            size='Absolute Net Income', size_max=30,
                            color='Sign Net Income',
                            )

    # changing where initial map show
    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1Ijoid2VpZ2Vsdml2aWFuIiwiYSI6ImNsMXdhYjVrcjBiZ3AzZWxtczZjNHd6OGIifQ.tc-vqaSVnexmAp1s9ocCUw',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=39.8,
                lon=-96.5
            ),
            pitch=0,
            zoom=2.6
        )
    )

    return fig


def create_pie(df, hospital, choice='Costs'):
    """
    creates the pie chart of income/costs
    :param df: pandas df of hosp data
    :param hospital: string of selected hospital
    :param choice: str (either income or costs)
    :return: pie chart figure
    """
    # checks input to grab correct columns for either income or costs
    if choice == 'Income':
        cats = ['Total Assets', 'Inpatient Revenue', 'Outpatient Revenue',
                'Net Income from Service to Patients', 'Total Other Income',
                'Total Income', 'Net Revenue from Medicaid']
    else:
        cats = COSTS

    # filters data for just the selected hospital
    df = df.loc[df['NAME'] == hospital]
    for index, row in df.iterrows():
        amounts = []
        # appends desired columns to a list
        for col in cats:
            amounts.append(df[col][index])

    # creates new dataframe with just the desired info for the chart
    pie_df = pd.DataFrame()
    pie_df['Expense'] = cats
    pie_df['Amount($)'] = amounts

    # creates the figure
    fig = px.pie(pie_df, values='Amount($)', names='Expense')
    return fig


def bar_chart(df, hospital):
    """
    creates bar chart of basic info about a hospital
    :param df: pandas df of hospital data
    :param hospital: str of selected hospital name
    :return: bar chart
    """
    # creates dataframe of the averages for all hospitals
    df2 = df.mean(axis=0)
    #creates dataframe with just the selected hospital
    df = df.loc[df['NAME'] == hospital]

    hospital = []

    # gathering hospital values
    for index, row in df.iterrows():
        amounts = []
        for col in MAIN:
            amounts.append(df[col][index])
            hospital.append(df['NAME'][index])

    # getting averages
    for col in MAIN:
        amounts.append(df2[col])
        hospital.append('Avg. of All Hospitals')

    # creating bar chart data frame
    bar_df = pd.DataFrame()
    bar_df['Hospital Metrics'] = MAIN * 2
    bar_df['Amount($)'] = amounts
    bar_df['Hospital'] = hospital

    # creating figure
    fig = px.bar(bar_df, y='Amount($)', x='Hospital Metrics', color='Hospital', barmode='group',
                 title='General Hospital Metrics for Selected Hospital')
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig


def double_bar_chart(df, hospital1, hospital2, choice='Costs', per_bed='Total Costs'):
    """
    creates a comparison bar chart for two selected hospitals of costs or income
    :param df: pandas df of hospital data
    :param hospital1: str of selected hospital name
    :param hospital2: str of different selected hospital name
    :param choice: str of either Costs or Income to select the info displayed
    :param per_bed: str of choice of whether to look at total cost or to divide it by bed
    :return: comparison bar chart
    """
    # getting new filtered df based on hospital selection
    df = df.loc[(df['NAME'] == hospital1) | (df['NAME'] == hospital2)]

    # getting choice of analysis
    if choice == 'Income':
        cats = ['Total Assets', 'Inpatient Revenue', 'Outpatient Revenue',
                'Net Income from Service to Patients', 'Total Other Income',
                'Total Income', 'Net Revenue from Medicaid']
    else:
        cats = COSTS

    amounts = []
    hospital = []
    # checking cost ber bed choice
    if per_bed == 'Total Costs':
        # gathering info to graph
        for index, row in df.iterrows():
            for col in cats:
                amounts.append(df[col][index])
                hospital.append(df['NAME'][index])
        #creates new df
        pie_df = pd.DataFrame()
        pie_df['Expense'] = cats * 2
        pie_df['Amount($)'] = amounts
        pie_df['Hospital'] = hospital
    else:
        # creating new df to graph
        for index, row in df.iterrows():
            num_discharges = float(df['Total Discharges (V + XVIII + XIX + Unknown)'][index])
            for col in cats:
                amount = float(df[col][index])
                #dividing all amounts by the number of discharges
                amounts.append(amount / num_discharges)
                hospital.append(df['NAME'][index])
        #creates new df
        pie_df = pd.DataFrame()
        pie_df['Expense'] = cats * 2
        pie_df['Amount($)'] = amounts
        pie_df['Hospital'] = hospital

    # graphing the bar chart
    fig = px.bar(pie_df, y='Amount($)', x='Expense', color='Hospital', barmode='group')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return fig


def scatter(df, y_ax):
    """
    creates scatter plot of all hospitals of net income vs a selected y_axis
    :param df: pandas df of hospital data
    :param y_ax: str of selected y_axis column name
    :return: scatter plot
    """
    # creating scatter plot
    fig = px.scatter(df, x='Net Income', y=y_ax, hover_name='NAME')

    return fig
