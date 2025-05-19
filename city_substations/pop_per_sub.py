#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 09:04:05 2025

@author: vitana
"""

import pandas as pd
import quicklog


ql = quicklog.logger("output/quicklog_log.txt")
fh = open("output_text.txt", "w")

#reading input data
buffalo = pd.read_csv('output/buffalo_substations.csv')
syracuse = pd.read_csv('output/syracuse_substations.csv')
total_MW = pd.read_csv('../nat_grid_stats/output/total_rated_MW.csv')

# logging initial dataframes
ql.info("Buffalo substations input", buffalo.head())
ql.info("Syracuse substations input", syracuse.head())
ql.info("Total rated MW data", total_MW.head())

#consistent types for merging
for df, name in zip([syracuse, buffalo, total_MW], ['syracuse', 'buffalo', 'total_MW']):
    df['substation'] = df['substation'].astype(str)
    ql.log(f"Converted 'substation' to string in {name}", df.dtypes['substation'])

    
# merging substations with total MW
buffalo = buffalo.merge(total_MW, on='substation', how='left')
syracuse = syracuse.merge(total_MW, on='substation', how='left')

# Log after merge
ql.info("Buffalo after merging with MW", buffalo.head())
ql.info("Syracuse after merging with MW", syracuse.head())

# saving merged data
buffalo.to_csv('output/buffalo_geo.csv', index=False)
syracuse.to_csv('output/syracuse_geo.csv', index=False)
ql.log("Saved merged files", "output/buffalo_geo.csv, output/syracuse_geo.csv")

# counting population per substation
buffalo_pop_per_sub = 276397 / 54
syracuse_pop_per_sub = 146211 / 21
print('Population per substation Buffalo:', buffalo_pop_per_sub, file=fh)
print('Population per substation Syracuse:', syracuse_pop_per_sub, file=fh)
ql.log("Buffalo pop/substation", buffalo_pop_per_sub)
ql.log("Syracuse pop/substation", syracuse_pop_per_sub)

# filling missing MW with 0
buffalo['total_rated_MW'] = buffalo['total_rated_MW'].fillna(0)
syracuse['total_rated_MW'] = syracuse['total_rated_MW'].fillna(0)

# computing total MW and kW/person
buf_total_mw = buffalo['total_rated_MW'].sum()
syr_total_mw = syracuse['total_rated_MW'].sum()
buffalo_kw_per_person = buf_total_mw / 276397 * 1000
syracuse_kw_per_person = syr_total_mw / 146211 * 1000

print('\nkW per person in Buffalo:', buffalo_kw_per_person, file=fh)
print('\nkW per person in Syracuse:', syracuse_kw_per_person, file=fh)
ql.log("Buffalo total MW", buf_total_mw)
ql.log("Syracuse total MW", syr_total_mw)
ql.log("Buffalo kW/person", buffalo_kw_per_person)
ql.log("Syracuse kW/person", syracuse_kw_per_person)

# closing file and logger
fh.close()
ql.close()