"""
clean_data.py - for cleaning and processing the data
Last Modified: December 4, 2022
"""
import pandas as pd

#defining a list of columns with monetary values
MONEY_COL = ['Cost of Charity Care','Total Bad Debt Expense','Cost of Uncompensated Care',
             'Total Unreimbursed and Uncompensated Care','Total Salaries From Worksheet A','Overhead Non-Salary Costs',
             'Depreciation Cost','Total Costs','Inpatient Total Charges','Outpatient Total Charges',
             'Combined Outpatient + Inpatient Total Charges','Wage-Related Costs (Core)', 'Wage-Related Costs (RHC/FQHC)',
             'Total Salaries (adjusted)','Contract Labor','Wage Related Costs for Part - A Teaching Physicians',
             'Wage Related Costs for Interns and Residents','Cash on Hand and in Banks',
             'Temporary Investments','Notes Receivable','Accounts Receivable','Less: Allowances for Uncollectible Notes and Accounts Receivable'
            ,'Inventory','Prepaid Expenses','Other Current Assets','Total Current Assets','Total Fixed Assets',
             'Investments','Other Assets','Total Other Assets','Total Assets','Accounts Payable',"Salaries, Wages, and Fees Payable",
             'Payroll Taxes Payable','Notes and Loans Payable (Short Term)','Deferred Income','Other Current Liabilities',
             'Total Current Liabilities','Mortgage Payable','Notes Payable','Unsecured Loans','Other Long Term Liabilities',
             'Total Long Term Liabilities','Total Liabilities','General Fund Balance','Total Fund Balances','Total Liabilities and Fund Balances',
             'Managed Care Simulated Payments','Total IME Payment','Inpatient Revenue','Outpatient Revenue','Gross Revenue',
             'Net Patient Revenue','Less Total Operating Expense','Net Income from Service to Patients','Total Other Income',
             'Total Income','Total Other Expenses', 'Net Income','Net Revenue from Medicaid','Medicaid Charges']

def format_mon(df):
    """
    removes comma in money data and converts to float
    :param df: df of hospital data
    :return: cleaned df
    """
    # loops through df and each col w/money vals
    for index, row in df.iterrows():
        for col in MONEY_COL:
            # replaces commas and converts to float
            if type(row[col]) == str:
                row[col] = row[col].replace(',','')
                df[col][index] = float(row[col][1:])
            # makes null values = 0
            else:
                df[col][index] = 0

    return df

def net_income_mapping(df):
    """
    creates new columns for purposes of mapping net income
    :param df: dataframe of hospital data
    :return: updated df
    """
    abs_incomes = []
    signs = []
    # loops through df and creates list of abs value and list of its sign
    for index, row in df.iterrows():
        abs_incomes.append(abs(df['Net Income'][index]))
        if df['Net Income'][index] < 0:
            signs.append('-')
        else:
            signs.append('+')

    # creates new columns
    df['Absolute Net Income'] = abs_incomes
    df['Sign Net Income'] = signs
    return df
def main():
    # reading in data
    df = pd.read_csv('Hospital_Cost_Report_2019.csv')
    f2 = pd.read_csv('hospitals.csv')

    # defining columns to drop
    drop_col = [
        'rpt_rec_num',
        'Provider CCN',
        'Medicare CBSA Number',
        'CCN Facility Type',
        'Provider Type',
        'Type of Control',
        'Fiscal Year Begin Date',
        'Fiscal Year End Date',
        'Number of Interns and Residents (FTE)',
        'Total Days Title V',
        'Total Days Title XVIII',
        'Total Days Title XIX',
        'Total Discharges Title V',
        'Total Discharges Title XVIII',
        'Total Discharges Title XIX',
        'Total Days Title V + Total for all Subproviders',
        'Total Days Title XVIII + Total for all Subproviders',
        'Total Days Title XIX + Total for all Subproviders',
        'Total Discharges Title V + Total for all Subproviders',
        'Total Discharges Title XVIII + Total for all Subproviders',
        'Total Discharges Title XIX + Total for all Subproviders',
        'Hospital Total Days Title V For Adults &amp; Peds',
        'Hospital Total Days Title XVIII For Adults &amp; Peds',
        'Hospital Total Days Title XIX For Adults &amp; Peds',
        'Hospital Total Discharges Title V For Adults &amp; Peds',
        'Hospital Total Discharges Title XVIII For Adults &amp; Peds',
        'Hospital Total Discharges Title XIX For Adults &amp; Peds',
        'Land',
        'Land Improvements',
        'Buildings',
        'Leasehold Improvements',
        'Fixed Equipment',
        'Major Movable Equipment',
        'Minor Equipment Depreciable',
        'Health Information Technology Designated Assets',
        'DRG Amounts Other Than Outlier Payments',
        'DRG amounts before October 1',
        'DRG amounts after October 1',
        'Outlier payments for discharges',
        'Disproportionate Share Adjustment',
        'Allowable DSH Percentage',
        "Less Contractual Allowance and discounts on patients' accounts",
        'Net Revenue from Stand-Alone SCHIP',
        'Stand-Alone SCHIP Charges'
    ]
    df.drop(drop_col, inplace=True, axis=1)
    # removing rows with no data
    df['Zip Code'].dropna()
    df['ADDRESS'].dropna()
    df['City'].dropna()
    df['State Code'].dropna()

    # combining data to make a df including location
    comb = df.merge(f2, how = 'left', on = 'ADDRESS')
    comb = comb[comb['LATITUDE'].notna()]

    # formatting for data analysis
    df = format_mon(df)
    comb = format_mon(comb)
    comb = net_income_mapping(comb)

    #saving in a csv
    df.to_csv('hosp_cost_report.csv')
    comb.to_csv('hosp_locs.csv')

if __name__ == '__main__':
    main()
