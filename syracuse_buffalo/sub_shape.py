#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:46:03 2025

@author: vitana
"""

import pandas as pd
import geopandas as gpd

# creating a geopackage file with substations and feeders from the NY state website
base_df = pd.read_csv('data_from_state_gov/output/sub_shape.csv')

geom = gpd.points_from_xy(base_df['x'], base_df['y'])
geo_df = gpd.GeoDataFrame(data=base_df, geometry=geom, crs=3857)
geo_df.to_file("data_from_state_gov/output/sub_shape.gpkg",layer="substations")
