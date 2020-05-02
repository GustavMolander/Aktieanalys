"""
Sorting stocks after key performance indicators (KPI).
Data from borsdata.com will be formated correctly. 
Value Composite uses following KPI's:
P/E (pris/vinst), 
P/B (pris/eget kapital), 
P/S (pris/försäljning), 
P/FCF (pris/fritt kassaflöde), 
EV/EBITDA (företagsvärde/rörelseresultat före avskrivningar och amorteringar)

Requirements:
-borsdata.csv
Datafile from borsdata.com to be analyzed. 
"""


import pandas as pd
import numpy as np

# Read data from file 'borsdata.csv' 
# (in the same directory that your python process is based)
# encoding="ISO-8859-1"
data = pd.read_csv("borsdata.csv", encoding="ISO-8859-1", sep=";", decimal=',')

#clean up data and convert to float
data = data[1:]
data_name = data["Bolagsnamn"]
data_nameless = data.drop('Bolagsnamn', 1)
data_nameless = data_nameless.replace(',', '.', regex=True).astype(float)
data = pd.concat([data_name, data_nameless], axis=1)



#screen for negative markers and missing information
data.drop(data[data['P/E'] < 0].index, inplace = True)
data.drop(data[data['P/B'] < 0].index, inplace = True)
data.drop(data[data['P/FCF'] < 0].index, inplace = True)
data.drop(data[data['EV/EBITDA'] < 0].index, inplace = True)
data.dropna(inplace = True)

# Create the value ranking
data['Value Rank'] = 0
data.astype({'Value Rank': 'int32'}).dtypes


def _sort_value(data, indicators):
    """
    Sorts the DataFrame 'data' by a number of key performance
    indicators listed in 'indicators'. A combined score will
    determine the best stocks across all the parameters. 

    Parameters
    ----------
    data : DataFrame
        DataFrame to be sorted
    indicators : str[]
        The different performance indicators, as columns headers in 'data'.
    """
    for kpi in indicators:
        data = data.sort_values(kpi)
        for i, x in enumerate(data['Value Rank']):
            data['Value Rank'].iloc[i] = x + i
    data = data.sort_values('Value Rank')
    print(data.head(20))
    

_sort_value(data, ['P/E', 'P/S', 'P/B', 'EV/EBITDA'])
