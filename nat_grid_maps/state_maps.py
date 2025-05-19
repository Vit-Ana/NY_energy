#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 16 22:47:31 2025

@author: vitana
"""

import geopandas as gpd
import os
import requests

# downloading state boundary file from Census
url = "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_500k.zip"
output_state = "input/cb_2018_us_state_500k.zip"

response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(output_state, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Download completed: {output_state}")
else:
    print(f"Failed to download. Status code: {response.status_code}")
    
    
    
#%%
# downloading zip codes shapefile from Census
zcta_url = "https://www2.census.gov/geo/tiger/TIGER2024/ZCTA520/tl_2024_us_zcta520.zip"
output_zip = "input/tl_2024_us_zcta520.zip"

# Download the file
response = requests.get(zcta_url, stream=True)
if response.status_code == 200:
    with open(output_zip, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded: {output_zip}")
else:
    raise Exception(f"Download failed with status code: {response.status_code}")   
    
    
#%%    
# reading input files
zips = gpd.read_file('input/tl_2024_us_zcta520.zip')
states = gpd.read_file('input/cb_2018_us_state_5m.zip')

# ensuring both have the same CRS
if zips.crs != states.crs:
    states = states.to_crs(zips.crs)

# filtering state geometries for New York (36) and California (06)
# and dissolving to get single polygon per state
ny_state = states[states['STATEFP'] == '36'].dissolve()
ca_state = states[states['STATEFP'] == '06'].dissolve()

# clipping zip codes to each state
zips_ny = zips.clip(ny_state, keep_geom_type=True)
zips_ca = zips.clip(ca_state, keep_geom_type=True)

# setting output file names
out_file_ny = 'output/zips_ny.gpkg'
out_file_ca = 'output/zips_ca.gpkg'

# removing old files if they exist
for out_file in [out_file_ny, out_file_ca]:
    if os.path.exists(out_file):
        os.remove(out_file)

# saving to GeoPackage
zips_ny.to_file(out_file_ny, layer='zips_ny', driver='GPKG')
zips_ca.to_file(out_file_ca, layer='zips_ca', driver='GPKG')

