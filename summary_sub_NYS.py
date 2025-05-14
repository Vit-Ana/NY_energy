#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 16:31:03 2025

@author: vitana
"""


import pandas as pd
import quicklog

ql = quicklog.logger('summary_sub_NYS.log')

ql.log('Reading input files',{'OH.csv','UG.csv','column_names.csv'},json=True)

OH = pd.read_csv('OH.csv', dtype=str, sep=';')
UG = pd.read_csv('UG.csv', dtype=str, sep=';')
names = pd.read_csv('column_names.csv')

#%%
#changing the column names in OH
OH_names = names.set_index('OH')['STD'].to_dict() 
OH = OH.rename(columns = OH_names)


#%%
#changing the column names in UG
UG_names = names.set_index('UG')['STD'].to_dict() 
UG = UG.rename(columns = UG_names)
UG = UG.drop(columns=['x', 'y'])

# Rewritten later: defer until then
#OH.to_csv('OH_std.csv', index=False)
#UG.to_csv('UG_std.csv', index=False)

#%%
#checking the number of substations
OH_total_sub = OH.groupby("substation").size().reset_index(name="count")
#OH_grouped = OH.groupby("substation", as_index=False)[["summerrating", "peakampscurr", "pctratingcurr", "peakampslast", "pctratinglast"]].sum()

ql.log("Number of OH substations", OH["substation"].nunique())


#%%
#checking the number of substations
UG_total_sub = UG.groupby("substation").size().reset_index(name="count")

ql.log("Number of UG substations", UG["substation"].nunique())    


#%%
# --- computing summer rating sum for OH ---

#creating bins of 100amp

bin_edges = [0, 100, 200, 300, 400, 500, float('inf')] #Example bin edges
bin_labels = ["0-100", "101-200", "201-300", "301-400", "401-500", "500+"] #Example bin labels

OH['summerrating'] = pd.to_numeric(OH['summerrating'])
OH['amp_rating_bin'] = pd.cut(OH['summerrating'], bins=bin_edges, labels=bin_labels)

UG['summerrating'] = pd.to_numeric(UG['summerrating'])
UG['amp_rating_bin'] = pd.cut(UG['summerrating'], bins=bin_edges, labels=bin_labels)






#%%
# counting the number of feeders and total amp fillna = 0
OH_feeders = OH.groupby(['substation', 'amp_rating_bin'], observed=True)['summerrating'].count().fillna(0)
OH_total_amps = OH.groupby(['substation', 'amp_rating_bin'], observed=True)['summerrating'].sum().fillna(0)
UG_feeders = UG.groupby(['substation', 'amp_rating_bin'], observed=True)['summerrating'].count().fillna(0)
UG_total_amps = UG.groupby(['substation', 'amp_rating_bin'], observed=True)['summerrating'].sum().fillna(0)



#%%
# 2-level index count and sum
OH_summary = pd.DataFrame({'feeders': OH_feeders, 'total_amps': OH_total_amps})
UG_summary = pd.DataFrame({'feeders': UG_feeders, 'total_amps': UG_total_amps})
#saving the summary files
OH_summary.to_csv('OH_summary.csv')
UG_summary.to_csv('UG_summary.csv')

ql.log('Wrote summary files',{'OH_summary.csv','UG_summary.csv'},json=True)

#  The following are not used or saved: comment out for now
#
# OH_grouped = OH.groupby('amp_rating_bin').size().reset_index(name='count')
# UG_grouped = UG.groupby('amp_rating_bin').size().reset_index(name='count')
#
# kV_OH_grouped = OH.groupby('voltage').size().reset_index(name='count')
# kV_UG_grouped = UG.groupby('voltage').size().reset_index(name='count')


#%%
#saving the standardized csv files
OH.to_csv('OH_std.csv', index=False)
UG.to_csv('UG_std.csv', index=False)

ql.log('Wrote standardized output files',{'OH_std.csv','UG_std.csv'},json=True)





