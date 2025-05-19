#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 08:53:59 2025

@author: vitana
"""

import geopandas as gpd
import matplotlib.pyplot as plt


def analyze_city_substations(city_name, cities_fp, substations_fp, buffer_miles=2):
    """
    Analyzing and plotting substations within a buffer around a city.

    Parameters:
        city_name (str): Name of the city (e.g., 'Syracuse', 'Buffalo').
        cities_fp (str): File path to the city shapefile.
        substations_fp (str): File path to the substations shapefile (GPKG).
        buffer_miles (float): Radius around the city to search, in miles.
    """

    #converting miles to meters for projected CRS (EPSG:3857)
    buffer_meters = buffer_miles * 1609.34

    #loading city shapefile
    cities = gpd.read_file(cities_fp)
    city = cities[cities['NAME'] == city_name].copy()
    if city.empty:
        raise ValueError(f"City '{city_name}' not found in shapefile.")

    #projecting to a metric CRS
    city = city.to_crs(epsg=3857)

    #creating buffer
    city_buffer = city.buffer(buffer_meters)
    buffer_gdf = gpd.GeoDataFrame(geometry=city_buffer, crs=city.crs)

    #loading substations and ensure CRS matches
    substations = gpd.read_file(substations_fp)
    substations = substations.to_crs(city.crs)

    #spatial join: substations within the buffer
    substations_in_buffer = gpd.sjoin(substations, buffer_gdf, how='inner', predicate='intersects')

    #saving as csv-files
    csv_path = f"output/{city_name.lower()}_substations.csv"
    substations_in_buffer.drop(columns='geometry').to_csv(csv_path, index=False)
    print(f"Saved substations CSV for {city_name}: {csv_path}")

    #plotting
    fig, ax = plt.subplots(figsize=(10, 10))
    buffer_gdf.boundary.plot(ax=ax, color='blue', linewidth=2, label='2-Mile Buffer')
    city.boundary.plot(ax=ax, color='black', linestyle='--', linewidth=1, label='City Boundary')
    substations_in_buffer.plot(ax=ax, color='red', markersize=30, label='Substations')
    ax.set_title(f'Substations within 2 Miles around {city_name}', fontsize=16)
    ax.legend()
    ax.set_axis_off()
    plt.tight_layout()
    plot_path = f"output/{city_name.lower()}_map.png"
    fig.savefig(plot_path, dpi=300)
    plt.show()
    print(f"Saved plot for {city_name}: {plot_path}")

#%%
# --- Usage ---
#calling the function for Syracuse and Buffalo
cities_fp = 'input/tl_2024_36_place.zip'
substations_fp = 'input/grid_shape.gpkg'

analyze_city_substations('Syracuse', cities_fp, substations_fp)
analyze_city_substations('Buffalo', cities_fp, substations_fp)




