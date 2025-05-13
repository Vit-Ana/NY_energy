#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:16:40 2025

@author: vitana
"""

import requests
import pandas as pd

def download_census_population(place_code: str, state_code: str, output_file: str):
    """
    Downloads population data from the U.S. Census API for a given place and state,
    saves the result to a CSV file.

    Args:
        place_code (str): The place code for the location (e.g., "73000" for Syracuse).
        state_code (str): The FIPS state code (e.g., "36" for New York).
        output_file (str): Path to save the resulting CSV.
    """
    api = "https://api.census.gov/data/2023/acs/acs5"
    params = {
        'get': 'B01001_001E',   # total population
        'for': f'place:{place_code}',
        'in': f'state:{state_code}'
    }

    # sending request to API
    response = requests.get(api, params)
    if response.status_code != 200:
        print(f'Error fetching data for place {place_code}')
        print('Status:', response.status_code)
        print(response.text)
        return  # or raise an exception

    # processing the response
    data = response.json()
    colnames = data[0]
    datarows = data[1:]

    # converting to dataframe
    df = pd.DataFrame(data=datarows, columns=colnames)

    # renaming population column
    df = df.rename(columns={'B01001_001E': 'pop'})

    # saving to CSV
    df.to_csv(output_file, index=False)
    print(f"Saved population data to {output_file}")

# --- usage ---
download_census_population(place_code="73000", state_code="36", output_file="syr_pop.csv")
download_census_population(place_code="11000", state_code="36", output_file="buff_pop.csv")
