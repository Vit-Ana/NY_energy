#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 16:31:03 2025

@author: vitana
"""


import pandas as pd

OH = pd.read_csv('OH.csv', dtype=str, sep=';')
UG = pd.read_csv('UG.csv', dtype=str, sep=';')
UG = UG.drop(columns=['x', 'y'])

#%%
#creating dataframe wirh column names
T = pd.DataFrame()
T['OH'] = OH.columns
T['UG'] = UG.columns
T['STD'] = T['UG'].str.lower()


#%%
#creating new column names

new_column_names = {
    'feeder': 'feeder',
    'substation': 'substation',
    'operating voltage (kv)': 'voltage',
    'summer rating (amps)': 'summerrating',
    'peak_amps_current_year': 'peakampscurr',
    'pct_rating_current_year': 'pctratingcurr',
    'peak_amps_last_year': 'peakampslast',
    'pct_rating_last_year': 'pctratinglast',
    'historical_load_curve_extract': 'loadcurvehist',
    'forecast_load_curve_extract': 'loadcurvefor'
}

T['STD'] = T['STD'].replace(new_column_names)


T.to_csv('column_names.csv')
