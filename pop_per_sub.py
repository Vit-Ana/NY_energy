#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 09:04:05 2025

@author: vitana
"""

import pandas as pd
buffalo = pd.read_csv('results_buffalo_substations.csv')
syracuse = pd.read_csv('results_syracuse_substations.csv')
total_MW = pd.read_csv('total_rated_MW.csv')

syracuse['substation'] = syracuse['substation'].astype(str)
buffalo['substation'] = buffalo['substation'].astype(str)
total_MW['substation'] = total_MW['substation'].astype(str)

buffalo = buffalo.merge(total_MW, on='substation', how='left')
syracuse = syracuse.merge(total_MW, on='substation', how='left')

buffalo.to_csv('buffalo_geo.csv')
syracuse.to_csv('syracuse_geo.csv')


print ('Population per substation Buffalo:', 276397/54)
print('Population per substation Syracuse:', 146211/21)


buffalo['total_rated_MW'] = buffalo['total_rated_MW'].fillna(0)
syracuse['total_rated_MW'] = syracuse['total_rated_MW'].fillna(0)

buf_total_mw = buffalo['total_rated_MW'].sum()
syr_total_mw = syracuse['total_rated_MW'].sum()

print ('kW per population in Buffalo:', buf_total_mw/276397*1000)
print('kW per population in Syracuse:', syr_total_mw/146211*1000)