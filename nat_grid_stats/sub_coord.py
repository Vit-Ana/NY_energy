#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 06:48:04 2025

@author: vitana
"""

import pandas as pd
output = 'output/coordinates.csv'

#%%
#reading the substations file
coord = pd.read_csv('input/Substations.csv', dtype=str, index_col=0, sep=';')
print(coord.dtypes)
print(coord['y'].unique())
print(coord['x'].unique())
print(coord.columns)

coord.index.name = 'substation'

#%%
coord["x"] = coord["x"].str.replace('\xa0', '')
coord["x"] = coord["x"].str.replace(',', '.')
print(coord.dtypes)
print(coord["x"])
coord["x"] = coord["x"].str.replace(' ', '')
#coord["x"] = coord["x"].astype(float)


#%%
# cleaning the values in the columns
coord["y"] = coord["y"].str.replace('\xa0', '')
coord["y"] = coord["y"].str.replace(',', '.')
#coord["y"] = coord["y"].astype(float)

print(coord.dtypes)

#%%

coord.to_csv(output)
















