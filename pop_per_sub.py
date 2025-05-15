#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 09:04:05 2025

@author: vitana
"""

import pandas as pd
fh = open("/Users/vitana/Documents/NY energy resilience/NY_energy/data_from_state_gov/output_text.txt", "w")

buffalo = pd.read_csv('/Users/vitana/Documents/NY energy resilience/NY_energy/syracuse_buffalo/output/buffalo_substations.csv')
syracuse = pd.read_csv('/Users/vitana/Documents/NY energy resilience/NY_energy/syracuse_buffalo/output/syracuse_substations.csv')
total_MW = pd.read_csv('/Users/vitana/Documents/NY energy resilience/NY_energy/nat_grid_stats/output/total_rated_MW.csv')


syracuse['substation'] = syracuse['substation'].astype(str)
buffalo['substation'] = buffalo['substation'].astype(str)
total_MW['substation'] = total_MW['substation'].astype(str)

buffalo = buffalo.merge(total_MW, on='substation', how='left')
syracuse = syracuse.merge(total_MW, on='substation', how='left')

buffalo.to_csv('syracuse_buffalo/output/buffalo_geo.csv')
syracuse.to_csv('syracuse_buffalo/output/syracuse_geo.csv')


print ('Population per substation Buffalo:', 276397/54, file=fh)
print('\nPopulation per substation Syracuse:', 146211/21, file=fh)


buffalo['total_rated_MW'] = buffalo['total_rated_MW'].fillna(0)
syracuse['total_rated_MW'] = syracuse['total_rated_MW'].fillna(0)

buf_total_mw = buffalo['total_rated_MW'].sum()
syr_total_mw = syracuse['total_rated_MW'].sum()

print ('\nkW per person in Buffalo:', buf_total_mw/276397*1000, file=fh)
print('\nkW per person in Syracuse:', syr_total_mw/146211*1000, file=fh)

fh.close()