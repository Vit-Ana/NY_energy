#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 21:14:20 2025

@author: vitana
"""

# --- output files ---
#all substations according to the National Grid website
out_1 = "grid_shape.gpkg"
#feeders carrying 10+ MW of power 
out_2 = "MW10_shape.gpkg"


import pandas as pd
OH = pd.read_csv('OH_std.csv')
UG = pd.read_csv('UG_std.csv')

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


#%%
#reading the csv file with the substation coordinates
coordinates = pd.read_csv('coordinates.csv')
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
import geopandas as gpd

geom = gpd.points_from_xy(grid_shape['x'], grid_shape['y'])
geo_df = gpd.GeoDataFrame(data=grid_shape, geometry=geom, crs=3857)
geo_df.to_file(out_1,layer="substations")


#%%
#loading the list of substations
nys_sub = pd.read_csv('nys_sub.csv')
#standardizing substation names to uppercase
nys_sub['substation'] = nys_sub['substation'].str.upper()
#correcting inconsistencies in substation names
nys_sub = nys_sub.replace({"124 ALMEDA AVE": "124 ALAMEDA AVE", 
                           '31 STATION 31': '31 STATION',
                           "LIVINGSTON COUNTY CORRECTIO": "LIVINGSTON COUNTY CORRECTIONAL",
                           'ALBION SUBSTATION NO. 80': 'ALBION',
                           'FLY RD.': 'FLY RD',
                           'LABRADOR SUBSTATION': 'LABRADOR',
                           'SEVENTH AVE. SUB.': 'SEVENTH AVE',
                           'TEALL SUBSTATION': 'TEALL AVE'
                           })
     
#merging substations with grouped feeder data to find unmatched substations
omitted = nys_sub.merge(grouped_feeders, how="outer", on="substation", validate="m:1", indicator=True)
print(omitted['_merge'].value_counts())
#filtering for substations in nys_sub that did not match any in grouped_feeders
left_merged_omitted = omitted[omitted['_merge'] == 'left_only']
result = left_merged_omitted.groupby(['v1']).size()
#filtering for successfully matched substations
both_merged_omitted = omitted[omitted['_merge'] == 'both']
result2 = both_merged_omitted.groupby(['v1']).size()
#saving as a csv file
omitted.to_csv('omitted.csv')

#%%
#cleaning the data, dropping the duplicates
omitted.columns.tolist()
omitted = omitted.drop_duplicates()
agg_dict = {col: (lambda x: list(sorted(x.dropna().unique()))) if col in ['rated voltage', 'rated mva'] else 'first'
            for col in omitted.columns if col != 'substation'}

result3 = omitted.groupby('substation').agg(agg_dict).reset_index()
result3.to_csv('result3.csv')
ny_sub_coord = coordinates.merge(result3, how="right", on='substation') 
ny_sub_coord = ny_sub_coord.drop(columns="_merge")
ny_sub_coord.to_csv('ny_sub_coord.csv')



#%%
#mapping the feeders carrying 10+ MW of power
mw_10 = result3.query("total_rated_MW >= 10")
mv10_shape = coordinates.merge(mw_10, how="right", on='substation') 
mv10_shape = mv10_shape.drop(columns="_merge")

geom_10 = gpd.points_from_xy(mv10_shape['x'], mv10_shape['y'])
geo_df_10 = gpd.GeoDataFrame(data=mv10_shape, geometry=geom_10, crs=3857)
geo_df_10.to_file(out_2,layer="substations")







