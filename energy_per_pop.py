#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 09:50:24 2025

@author: vitana
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# setting plot resolution
plt.rcParams['figure.dpi'] = 300

# defining file paths and projections
out_file = 'substation_output.gpkg'
wgs83 = 4269
utm18n = 26918

# reading and projecting spatial data
ny_map = gpd.read_file('nys_zip.gpkg').to_crs(utm18n)
substations = gpd.read_file('MW10_shape.gpkg').to_crs(utm18n)
pop = pd.read_csv('NY_pop.csv')

#%%
#merging zip shapefile and population data
ny_map['zip'] = ny_map['ZCTA5CE20']
pop['zip'] = pop['zip'].astype(str)
ny_map['zip'] = ny_map['zip'].astype(str)
ny_map = ny_map.merge(pop, on='zip')


#%%
#cleaning substations and creating unique IDs
substations = substations.dropna(subset=['geometry']).copy()
substations = substations.reset_index(drop=True)
substations['sub_id'] = substations.index

#%%
#removing previous output if exists
if os.path.exists(out_file):
    os.remove(out_file)
#saving initial layers
ny_map.to_file(out_file, layer='zip_codes')
substations.to_file(out_file, layer='substations')

#%%
#creating a basic map of substations and ZIPs
fig, ax = plt.subplots()
ny_map.boundary.plot(ax=ax, linewidth=0.5, color='gray')
substations.plot(ax=ax, color='red', markersize=2)
ax.axis('off')
plt.title("Substations and zip codes")

#%%
#spatially joining substations by zip
sub_in_zip = gpd.sjoin(substations, ny_map, how='left', predicate='within')

#counting substations per ZIP
zip_counts = sub_in_zip.groupby('zip').size().reset_index(name='substations_in_zip')

#merging counts with population info
zip_with_subs = ny_map.merge(zip_counts, on='zip', how='left')
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

#calculating people served
sub_in_zip['people_served'] = sub_in_zip['pop'] / sub_in_zip['substations_in_zip']

#%%
#merging results back to substations
substations = substations.merge(sub_in_zip[['sub_id', 'zip', 'people_served']], on='sub_id', how='left')

#%%
#saving as layers
zip_with_subs.to_file(out_file, layer='zip_with_population_per_substation')
substations.to_file(out_file, layer='substations_with_people_served')

#%%
#creating a heat map of people per substation by ZIP
fig, ax = plt.subplots()
zip_with_subs.plot(column='people_per_substation', ax=ax, legend=True, cmap='Blues')
substations.plot(ax=ax, color='red', markersize=2)
ax.axis('off')
plt.title("Estimated People per Substation by zip code")
plt.tight_layout()


#%%
#creating a scatter plot with rated MW vs people served
plot_data = sub_in_zip[['total_rated_MW', 'people_served']].dropna()

plt.figure(figsize=(10, 6))
plt.scatter(plot_data['total_rated_MW'], plot_data['people_served'], alpha=0.6, edgecolor='k')
plt.title('Rated MW vs. People Served per Substation')
plt.xlabel('Rated MW')
plt.ylabel('People Served')
plt.grid(True)
plt.tight_layout()
plt.show()





