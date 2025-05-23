#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 17:05:56 2025

@author: vitana
"""

import pandas as pd
import quicklog

# initializing the logger
ql = quicklog.logger("output_log.txt")


# uploading the coordinates file from the National Grid website and a file with substations
# and feeders + substations files from NY state government website
ql.log("Loading CSVs", "coordinates.csv and nys_feeders.csv")
df1 = pd.read_csv('../nat_grid_stats/coordinates.csv')
df2 = pd.read_csv('output/nys_feeders.csv')

df2['substation'] = df2['substation'].str.replace("LIVINGSTON COUNTY CORRECTIO", "LIVINGSTON COUNTY CORRECTIONAL", case=False).str.strip()                                                                                                                      
ql.info("Unique substation names in df1", pd.Series(df1['substation'].unique()))
ql.info("Unique substation names in df2", pd.Series(df2['substation'].unique()))


#%%
#creating dataframe wirh column names to check the uniformity
df = pd.DataFrame()
df['coord'] = df1['substation']
df['feeders'] = df2['substation']
#df['STD'] = df['feeders']
all_different = list(set(df['coord']) ^ set(df['feeders']))
matches = set(df['coord']) & set(df['feeders'])

ql.log("Initial exact matches count", len(matches))
ql.info("Initial unique differences", pd.Series(all_different))

#saving to a csv file
different_series = pd.Series(all_different)
#different_series.to_csv('sub_different.csv')



#%%
# cleaning and unifying the substation names
def clean_substation_name(name):
    if isinstance(name, str):
        name = name.upper()
        name = name.replace("SUBSTATION", "").strip()
        name = name.replace("124 ALMEDA AVE", "124 ALAMEDA AVE").strip()
        name = name.replace("56 ELECTRIC AVE", "55 ELECTRIC AVE").strip()
        name = name.replace("81 BEECH AVE", "81 BEACH AVE").strip()
        name = name.replace("ASH ST. SUB", "ASH ST").strip()
        name = name.replace("DEPOT RD", "DEPOT").strip()
        name = name.replace("BLOOMINGDALE MOBILE SUB", "BLOOMINGDALE").strip()
        name = name.replace("STREET", "ST").strip()
        name = name.replace("ST.", "ST").strip()
        name = name.replace(" BA", " BAY")
        name = name.replace("LIVINGSTON COUNTY CORRECTIO", "LIVINGSTON COUNTY CORRECTIONAL").strip()
        name = name.replace("SELKIRK SUB", "SELKIRK").strip()
        name = name.replace("MIDDLEVILLE,  HANSON MIDDL", "MIDDLEVILLE").strip()
        name = name.replace("MILTON", "MILTON AVE").strip()
        name = name.replace("MILTON AVE AVE", "MILTON AVE").strip()
        name = name.replace("TEALL", "TEALL AVE").strip()
        name = name.replace("TEALL AVE AVE", "TEALL AVE").strip()
        name = name.replace("TIBBITS AVE", "TIBBETS AVE").strip()
        name = name.replace("N.", "NORTH").strip()
        name = name.replace("SUB.", "").strip()
        name = name.replace("AVE.", "AVE").strip()
        name = name.replace("SHERMAN CRCC", "SHERMAN").strip()
        name = name.replace("RD.", "RD").strip()
        name = name.replace("ROAD", "RD").strip()
        name = name.replace("STA.", "").strip() 
        name = name.replace("#", "").strip()  
        name = name.replace("SPRINGFIELD", "EAST SPRINGFIELD").strip()  
        name = name.replace("EAST SPRINGFIELD RD", "SPRINGFIELD RD").strip()  
        name = name.replace("IE.", "").strip()  
        name = name.replace("(", "").replace(")", "").strip() 
        name = name.replace("- PROPOSED", "").strip() 
        
        parts = name.split()
            
        if name.endswith(" BAYY"):
            name = name[:-1].strip()
            
        if len(parts) == 3 and parts[1] == "STATION" and parts[0].isdigit() and parts[2].isdigit() and parts[0] == parts[2]:
            name = f"STATION {parts[2]}"


        return name
    return name 


# applying the cleaning function to both columns
df['cleaned_coord'] = df['coord'].apply(clean_substation_name)
df['cleaned_feeders'] = df['feeders'].apply(clean_substation_name)

df1['substation'] = df['cleaned_coord']
df2['substation'] = df['cleaned_feeders']

#checking unique cleaned names from both columns
unique_cleaned_coord = df['cleaned_coord'].unique()
unique_cleaned_feeders = df['cleaned_feeders'].unique()

ql.info("Cleaned Coord Names", pd.Series(df['cleaned_coord'].unique()))
ql.info("Cleaned Feeders Names", pd.Series(df['cleaned_feeders'].unique()))

#looking for exact matches after cleaning
exact_matches = set(unique_cleaned_feeders) - set(unique_cleaned_coord)
all_different2 = list(set(df['cleaned_coord']) ^ set(df['cleaned_feeders']))

ql.log("Exact matches after cleaning", len(exact_matches))
ql.info("Differences after cleaning", pd.Series(all_different2))

#saving to a csv file
different_series2 = pd.Series(all_different2)
different_series2.to_csv('output/sub_different.csv')


#%%
#MERGING THE DF1 AND DF2
merged = df1.merge(df2, on='substation', how='left', indicator=True) 
ql.info("Merge status counts", merged['_merge'].value_counts())
sub_shape = merged.drop(columns=['_merge'])
sub_shape.to_csv('output/sub_shape.csv')

ql.close()















