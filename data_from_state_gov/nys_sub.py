#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 22:01:17 2025

@author: vitana
"""

import pandas as pd

 # --- Converting excel into a csv file for coding purposes ---

# reading an excel file
df = pd.read_excel('input/nys-substations.xlsx')
df.columns = df.columns.str.lower()
#df = df.fillna(0)

#deviding the badly shaped table into 2 dataframes to further join them
df1 = df.loc[:752]
#dropping columns with missing values
df1 = df1.drop(columns=['unnamed: 1', 'unnamed: 3', 'unnamed: 5'])
df2 = df.loc[753:].reset_index() 
#dropping columns with missing values
df2 = df2.drop(columns=['index', 'unnamed: 2', 'unnamed: 4', 'unnamed: 6', 'unnamed: 7', 'unnamed: 8', 'unnamed: 9', 'unnamed: 10'])
nys_sub = pd.concat([df1, df2], axis=1, ignore_index=False)
nys_sub = nys_sub.drop([0, 1]) 

#filling the lines with 0 values with previous values
nys_sub = nys_sub.fillna(method='ffill').reset_index()
nys_sub = nys_sub.drop(columns=['index']) 

#deleting the last row which only duplicates the data a summarizes customers
nys_sub = nys_sub.loc[:749]


#%%
#creating new column names
nys_sub.columns = nys_sub.iloc[0].str.lower()
nys_sub = nys_sub.drop([0]) 
print(nys_sub.columns.tolist())


new_column_names = {
    '#transmission feed ckt(s)': 'trans_feeders',
    '#sub t feed ckt': 'subtrans_feeders',
    '#distribution feeders': 'dist_feeders',
    'substation name': 'substation',
    '#banks': 'banks',
    '# circuits': 'circuits', 
    'age / last\nmajor upgrade': 'age'
}
#renaming the columns
nys_sub = nys_sub.rename(columns=new_column_names)

print(nys_sub.columns.tolist())





#%%
#cleaning the data
#exploring unique values
print(nys_sub['rated voltage'].unique())


#checking the strange entries
in_voltage = nys_sub['rated voltage'].value_counts()
#nys_sub['rated voltage'].explode
#nys_sub['rated voltage'] = nys_sub['rated voltage'].str.replace('-', '/')
nys_sub['rated voltage'] = nys_sub['rated voltage'].replace({'34.4/5.04/13.':'34.4/5.04/13.8', '115/34.4/13.': '115/34.4/13.8', '115/34.5/13.': '115/34.5/13.8'})
print(nys_sub['rated voltage'].unique())


#%%
#standardizing separators
nys_sub['rated voltage'] = nys_sub['rated voltage'].astype(str)
def replace_if_hyphen(voltage):
    if '-' in voltage:
        parts = voltage.split('-')
        return '/'.join(parts)
    return voltage

nys_sub['rated voltage'] = nys_sub['rated voltage'].apply(replace_if_hyphen)
print(nys_sub['rated voltage'].unique())
nys_sub[['v1', 'v2', 'v3']] = nys_sub['rated voltage'].str.split('/', expand=True)



#%%
#cleaning mva column
print(nys_sub['rated mva'].unique())
nys_sub['rated mva'] = nys_sub['rated mva'].astype(str)
#changing the false numbers 
nys_sub['rated mva'] = nys_sub['rated mva'].replace({'2020-12-16 00:00:00':'12/16/20', 
                                                             '(blank)': '0', 
                                                             '2014-10-12 00:00:00': '10/12/14', 
                                                             '2022-12-16 00:00:00':'12/16/22', 
                                                             '7500/9375': '7.5/9.3'})
print(nys_sub['rated mva'].unique())


#%%
#standardizing separators

nys_sub[['mva1', 'mva2', 'mva3', 'mva4', 'mva5']] = nys_sub['rated mva'].str.split('/', expand=True)
print(nys_sub.head())


#%%
#turning all values in voltage columns to numeric
nys_sub = nys_sub.fillna(0)
nys_sub['v1'] = pd.to_numeric(nys_sub['v1'])
nys_sub['v2'] = pd.to_numeric(nys_sub['v2'])
nys_sub['v3'] = pd.to_numeric(nys_sub['v3'])
nys_sub["v1_bigger"] = (nys_sub["v1"] > nys_sub["v2"]) & (nys_sub["v1"] > nys_sub["v3"])

#checking bad rows where v2 or v2 is bigger than v1
for index, row in nys_sub.iterrows():
    if not (row["v1"] > row["v2"] and row["v1"] > row["v3"]):
        print(index)

print(nys_sub.loc[401])


#%%
#saving as a csv file
nys_sub.to_csv('output/nys_sub.csv', index=False)

#%%
#grouping
nys_grouped = nys_sub.groupby(['rated voltage']).size().reset_index(name='count')
nys_feeders = nys_sub.groupby(['substation'])['dist_feeders'].count().fillna(0)
#nys_voltage = nys_sub.groupby(['substation'])['rated voltage'].sum().fillna(0)
#nys_summary = pd.DataFrame({'dist_feeders': nys_feeders, 'rated voltage': nys_voltage})


#%%
#checking the number of substations 
print("Number of substations: ", nys_sub["substation"].nunique())  


#%%
nys_feeders.to_csv('output/nys_feeders.csv')














