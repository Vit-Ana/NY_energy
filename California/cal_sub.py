#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 01:22:05 2025

@author: vitana
"""

import pandas as pd
import matplotlib.pyplot as plt

# reading an excel file
cal_sub = pd.read_excel('input/Operational_Substations_CAL.xlsx')
cal_sub.columns = cal_sub.columns.str.lower()
cal_sub = cal_sub.fillna(0)
#fixing value inconsistency
cal_sub['highest_kv'] = cal_sub['highest_kv'].replace({'33kV to 92Kv': '33kV to 92kV'})

#grouping by highest_kv
cal_sub_grouped = cal_sub.groupby(['highest_kv']).size().reset_index(name='count')
print(cal_sub_grouped)

#saving to csv
cal_sub.to_csv('input/substations_california.csv', index=False)

#%%
# plotting the bar chart
plt.figure(figsize=(10, 6))
plt.bar(cal_sub_grouped['highest_kv'], cal_sub_grouped['count'], color='skyblue', edgecolor='black')
plt.title('Number of Substations by Highest kV Rating in California')
plt.xlabel('Highest kV')
plt.ylabel('Number of Substations')
plt.xticks(rotation=45)
plt.tight_layout()

# saving the figure
plt.savefig('output/california_substations_by_kv.png', dpi=300)
plt.show()

