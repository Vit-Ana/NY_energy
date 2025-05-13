#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 09:20:54 2025

@author: vitana
"""


import requests
import pandas as pd

#%%
#downloading the data from census
api = "https://api.census.gov/data/2018/acs/acs5"

population = {'get':'B01001_001E', 'for':"zip code tabulation area:*", 'in':"state:36"}

#checking the results
response = requests.get(api, population)
if response.status_code != 200:
    print( 'status:', response.status_code )
    print(response.text)
    assert False

row_list = response.json()         
colnames = row_list[0]
datarows = row_list[1:]

#%%
#downloading census info as a dataframe 
pop = pd.DataFrame(columns=colnames, data=datarows)  

#renaming the columns
new_names = {"B01001_001E": "pop", "zip code tabulation area": "zip"}
pop = pop.rename(columns=new_names)
pop = pop.set_index('zip')

#saving as a csv file
pop.to_csv("NY_pop.csv")


