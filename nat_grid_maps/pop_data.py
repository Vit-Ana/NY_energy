#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 09:20:54 2025

@author: vitana
"""

import requests
import pandas as pd

def download_census_population(state_code: str, output_file: str):
    """
    Downloads population data from the U.S. Census API for a given state,
    saves the result to a CSV file.

    Args:
        state_code (str): The FIPS state code (e.g., "36" for New York or "06" for California).
        output_file (str): Path to save the resulting CSV.
    """
    api = "https://api.census.gov/data/2018/acs/acs5"
    params = {
        'get': 'B01001_001E',    # total population
        'for': 'zip code tabulation area:*',
        'in': f'state:{state_code}'
    }

    # sending request to API
    response = requests.get(api, params)
    if response.status_code != 200:
        print('status:', response.status_code)
        print(response.text)
        return  # or raise an exception

    # processing the response
    row_list = response.json()
    colnames = row_list[0]
    datarows = row_list[1:]

    # converting to dataframe
    df = pd.DataFrame(data=datarows, columns=colnames)

    # renaming population column
    df = df.rename(columns={'B01001_001E': 'pop',
                            'zip code tabulation area': 'zip'})

    # saving to CSV
    df.to_csv(output_file, index=False)

# --- usage ---
download_census_population(state_code="36", output_file="input/new_york_population.csv")
download_census_population(state_code="06", output_file="input/california_population.csv")




