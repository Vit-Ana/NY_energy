#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:46:03 2025

@author: vitana
"""

import pandas as pd
import geopandas as gpd
import requests
import matplotlib.pyplot as plt

out_file = "output/sub_shape.gpkg"


# creating a geopackage file with substations and feeders from the NY state website
base_df = pd.read_csv('output/sub_shape.csv')

geom = gpd.points_from_xy(base_df['x'], base_df['y'])
geo_df = gpd.GeoDataFrame(data=base_df, geometry=geom, crs=3857)
geo_df.to_file(out_file,layer="substations")


#%%
# --- clipping this file to the boundary file of New York state
# downloading state boundary file from Census
url = "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_5m.zip"
output_state = "input/cb_2018_us_state_5m.zip"

response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(output_state, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Download completed: {output_state}")
else:
    print(f"Failed to download. Status code: {response.status_code}")
    
    
#%%
# loading and dissolving NY State
states = gpd.read_file('input/cb_2018_us_state_5m.zip')
ny_state = states[states['STATEFP'] == '36']
ny_state = ny_state.dissolve()#.reset_index(drop=True)

# ensuring CRS matches your existing data (EPSG:3857)
ny_state = ny_state.to_crs(epsg=3857)

# saving NY State as a new layer in each GeoPackage
ny_state.to_file(out_file, layer='state')


#%%
# clipping the substations to NY state boundary
substations_clipped = gpd.overlay(geo_df, ny_state, how='intersection')

# --- plotting ---
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ny_state.boundary.plot(ax=ax, color='black', linewidth=1)

# plotting substations, colored by number of feeders
substations_clipped.plot(
    ax=ax,
    column='dist_feeders',          # make sure 'feeders' column exists
    cmap='viridis_r',
    legend=True,
    markersize=20,
    alpha=0.8
)
ax.set_title('New York State Substations by Number of Feeders', fontsize=15)
ax.axis('off')

plt.savefig('output/gov_file_substations.png', dpi=300, bbox_inches='tight')
plt.close()

