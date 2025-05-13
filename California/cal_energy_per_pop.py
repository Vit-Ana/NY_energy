#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 11:15:42 2025

@author: vitana
"""


import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os


plt.rcParams['figure.dpi'] = 300

out_file = 'cal_substation_output.gpkg'

wgs83 = 4269
utm18n = 26918

ca_map = gpd.read_file('ca_zip.gpkg').to_crs(utm18n)
substations = gpd.read_file('ca_sub.gpkg').to_crs(utm18n)
pop = pd.read_csv('CA_pop.csv')

#merging zips and population
ca_map['zip'] = ca_map['ZCTA5CE20']
pop['zip'] = pop['zip'].astype(str)
ca_map['zip'] = ca_map['zip'].astype(str)
ca_map = ca_map.merge(pop, on='zip')


#%%
substations = substations.dropna(subset=['geometry']).copy()
substations = substations.reset_index(drop=True)
substations['sub_id'] = substations.index

#%%
if os.path.exists(out_file):
    os.remove(out_file)

ca_map.to_file(out_file, layer='zip_codes')
substations.to_file(out_file, layer='substations')

#%%
#plotting substations and zip on the map
fig, ax = plt.subplots()
ca_map.boundary.plot(ax=ax, linewidth=0.5, color='gray')
substations.plot(ax=ax, color='red', markersize=2)
ax.axis('off')
plt.title("Substations and zip codes")

#%%
#joining zip codes and substations
sub_in_zip = gpd.sjoin(substations, ca_map, how='left', predicate='within')
sub_in_zip = sub_in_zip.drop_duplicates(subset='Substation_ID', keep='first')
dupes1 = sub_in_zip[sub_in_zip.duplicated(substations.columns, keep=False)]
print(dupes1)

#counting substations per ZIP
zip_counts = sub_in_zip.groupby('zip').size().reset_index(name='substations_in_zip')

#merging counts with population info
zip_with_subs = ca_map.merge(zip_counts, on='zip', how='left')
zip_with_subs['substations_in_zip'] = zip_with_subs['substations_in_zip'].fillna(0).astype(int)

#computing people per substation
zip_with_subs['people_per_substation'] = zip_with_subs.apply(
    lambda row: row['pop'] / row['substations_in_zip'] if row['substations_in_zip'] > 0 else None,
    axis=1
)

    
#merging in only the necessary fields
sub_in_zip = sub_in_zip.merge(
    zip_with_subs[['zip', 'substations_in_zip']],
    on='zip',
    how='left'
)
sub_in_zip = sub_in_zip.drop_duplicates(subset='Substation_ID', keep='first')

# -- people served calculation --
sub_in_zip['people_served'] = sub_in_zip['pop'] / sub_in_zip['substations_in_zip']

#%%
#merging results back to substations
substations = substations.merge(sub_in_zip[['sub_id', 'zip', 'people_served']], on='sub_id', how='left')

#%%
#adding to the geopackage fike
zip_with_subs.to_file(out_file, layer='zip_with_population_per_substation')
substations.to_file(out_file, layer='substations_with_people_served')

#%%
#plotting
fig, ax = plt.subplots()
zip_with_subs.plot(column='people_per_substation', ax=ax, legend=True, cmap='Blues')
substations.plot(ax=ax, color='red', markersize=2)
ax.axis('off')
plt.title("Estimated People per Substation by zip code")
plt.tight_layout()
fig.savefig('est_pop_per_sub.png')
