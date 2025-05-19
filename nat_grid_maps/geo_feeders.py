#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 21:14:20 2025

@author: vitana
"""

import pandas as pd
import geopandas as gpd

# --- output files ---
#all substations according to the National Grid website
out_1 = "output/grid_shape.gpkg"
#feeders carrying 10+ MW of power 
out_2 = "output/MW10_shape.gpkg"

# --- input files ---
OH = pd.read_csv('../nat_grid_stats/output/OH_std.csv')
UG = pd.read_csv('../nat_grid_stats/output/UG_std.csv')

#%%
# --- data cleaning ---

#overhead feeders
OH['voltage'] = OH['voltage'].str.replace(',', '.')
OH['voltage'] = pd.to_numeric(OH['voltage'])
OH['peakampscurr'] = OH['peakampscurr'].str.replace(',', '.')
OH['peakampscurr'] = pd.to_numeric(OH['peakampscurr'])
OH["rated_MW"] = OH['voltage']*OH['peakampscurr']/1000


#underground feeders
UG['voltage'] = UG['voltage'].str.replace(',', '.')
UG['voltage'] = pd.to_numeric(UG['voltage'])
UG['peakampscurr'] = UG['peakampscurr'].str.replace(',', '.')
UG['peakampscurr'] = pd.to_numeric(UG['peakampscurr'])
UG["rated_MW"] = UG['voltage']*OH['peakampscurr']/1000



print(OH['substation'].nunique())
print(UG['substation'].nunique())


#%%
#concatinating 2 columns of both dataframes
frames = [UG[['substation', 'rated_MW']], OH[['substation', 'rated_MW']]]
feeders = pd.concat(frames)

grouped_feeders = feeders.groupby('substation').agg(
    total_rated_MW=('rated_MW', 'sum'),
    sum_feeders=('substation', 'count')
).reset_index()

print(grouped_feeders['substation'].nunique())

#unifying substations names
grouped_feeders = grouped_feeders.replace({
    "124 ALMEDA AVE": "124 ALAMEDA AVE", 
    '31 STATION 31': '31 STATION',
    '59 PERRY': 'PERRY ST',
    'CENTRAL SQUARE': 'CENTRAL SQUARE STATION',
    '81 BEECH AVE': '81 BEACH AVE',
    'ASH ST. SUB': 'ASH STREET',
    'CENTRAL SQUARE STATION': 'CENTRAL SQUARE',
    'CONESUS LAKE SUBSTATION': 'CONESUS LAKE',
    'GALEVILLE SUBSTATION': 'GALEVILLE',
    'MILTON AVE': 'MILTON',
    'SPRINGFIELD RD.': 'SPRINGFIELD',
    'YORK CTR': 'YORK CENTER SUBSTATION'
})
grouped_feeders.to_csv('../nat_grid_stats/output/total_rated_MW.csv')

#%%
#reading the csv file with the substation coordinates
coordinates = pd.read_csv('../nat_grid_stats/coordinates.csv')
#deleting spaces
coordinates.replace({'NEW FRANKHAUSER  STATION ': 'NEW FRANKHAUSER  STATION', 
                     'SOUTHLAND ': 'SOUTHLAND'})
#merging the substation data with feeders
grid_shape = grouped_feeders.merge(coordinates, how="outer", on='substation', indicator=True) 
print(grid_shape['_merge'].value_counts())
grid_shape = grid_shape.drop(columns="_merge")
#print(coordinates['substation'].unique())
#print(grid_shape['substation'].unique())

#%%
# --- adding the substations on the map ---

geom = gpd.points_from_xy(grid_shape['x'], grid_shape['y'])
geo_df = gpd.GeoDataFrame(data=grid_shape, geometry=geom, crs=3857)
geo_df.to_file(out_1,layer="substations")


#%%
#mapping the feeders carrying 10+ MW of power
mw_10 = grid_shape.query("total_rated_MW >= 10")
geom_10 = gpd.points_from_xy(mw_10['x'], mw_10['y'])
geo_df_10 = gpd.GeoDataFrame(data=mw_10, geometry=geom_10, crs=3857)
geo_df_10.to_file(out_2,layer="substations")


#%%
# loading and dissolving NY State
states = gpd.read_file('input/cb_2018_us_state_5m.zip')
ny_state = states[states['STATEFP'] == '36']
ny_state = ny_state.dissolve()#.reset_index(drop=True)

# ensuring CRS matches your existing data (EPSG:3857)
ny_state = ny_state.to_crs(epsg=3857)

# saving NY State as a new layer in each GeoPackage
ny_state.to_file(out_1, layer='state')
ny_state.to_file(out_2, layer='state')



