#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:40:44 2025

@author: vitana
"""

import geopandas as gpd

# Load shapefiles
cities = gpd.read_file('tl_2024_36_place.shp')
zctas = gpd.read_file('tl_2024_us_zcta520.shp')

# Filter for Syracuse (or Buffalo)
syracuse = cities[cities['NAME'] == 'Syracuse']

# Ensure CRS matches
zctas = zctas.to_crs(syracuse.crs)

# Perform spatial join (intersect)
intersected = gpd.sjoin(zctas, syracuse, how='inner', predicate='intersects')

# Now 'intersected' contains only the ZIP codes touching Syracuse
zips_in_city = gpd.overlay(zctas, syracuse, how='intersection', keep_geom_type=False)


#%%
#creating a 2 mi buffer
# Buffer around the city (approx 2 miles)
buffer_distance = 0.029  # degrees
syracuse_buffered = syracuse.buffer(buffer_distance)


#%%
# loading substations layer from your GPKG
substations = gpd.read_file('grid_shape.gpkg')
# Make sure CRS matches
substations = substations.to_crs(syracuse.crs)

# Buffer is a GeoSeries; turn it into GeoDataFrame
buffered_gdf = gpd.GeoDataFrame(geometry=syracuse_buffered, crs=syracuse.crs)

# Spatial join: find substations inside the buffer
substations_in_buffer = gpd.sjoin(substations, buffered_gdf, how='inner', predicate='intersects')


#%%
# Drop geometry column before saving
substations_table = substations_in_buffer.drop(columns='geometry')

# Save to CSV
substations_table.to_csv('syr_sub_in_syracuse_buffer.csv', index=False)

#%%
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 10))

# Plot the buffered city boundary
buffered_gdf.boundary.plot(ax=ax, color='blue', linewidth=2, label='2-Mile Buffer')

# Plot the original city boundary
syracuse.boundary.plot(ax=ax, color='black', linestyle='--', linewidth=1, label='City Boundary')

# Plot substations inside the buffer
substations_in_buffer.plot(ax=ax, color='red', markersize=30, label='Substations')

# Beautify the plot
ax.set_title('Substations within 2 Miles around Syracuse', fontsize=16)
ax.legend()
ax.set_axis_off()

plt.show()

fig.savefig('Syr_subs.png')





