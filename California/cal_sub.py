#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 01:22:05 2025

@author: vitana
"""

import pandas as pd


# reading an excel file
cal_sub = pd.read_excel('Operational_Substations_CAL.xlsx')
cal_sub.columns = cal_sub.columns.str.lower()
cal_sub = cal_sub.fillna(0)
cal_sub['highest_kv'] = cal_sub['highest_kv'].replace({'33kV to 92Kv': '33kV to 92kV'})

cal_sub_grouped = cal_sub.groupby(['highest_kv']).size().reset_index(name='count')
print(cal_sub_grouped)


cal_sub.to_csv('substations_california.csv', index=False)



