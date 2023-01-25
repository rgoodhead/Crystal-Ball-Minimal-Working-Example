# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:47:10 2023

@author: cex
"""

print("")
print("## ======================================================================== ")
print("## Executing run_NewFed_sutime_1_datainput.py                               ")
print("")

##################
## HOUSEKEEPING ##
##################

import random
random.seed(2222)

import os
import re
import pandas as pd

import sys
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

################
## DATA SETUP ##
################

ls_cases = ['MWE'] 

colnames = ['sutimefileslocation','corpuspreparedformatelocation','originalspeechespath']
df_info = pd.DataFrame(data=None, index=ls_cases, columns=colnames)

# setup: MWE
df_info.loc['MWE','sutimefileslocation'] = "./data/data_MWE/sent_sutime_corpus/"
df_info.loc['MWE','corpuspreparedformatelocation'] = './data/data_MWE/corpus_prepared_for_mate/'
df_info.loc['MWE','originalspeechespath'] = "./data/data_MWE/sent_dates_corpus/"

output_file = "./data/data_MWE/merged_data/data_SUTime2.pkl"
 
import contextlib
with contextlib.suppress(FileNotFoundError):
    os.remove(output_file)

####################################
## LOAD AND PREPARE SUTIME OUTPUT ##
####################################

dc_df = {}

from func_basic_sutime_operations import sutimeLoader, referenceIsolate, financialTermIsolate

for dd in ls_cases:
    
    print("############################")
    print("## Loading Corpus: " + dd)
    print("############################")
    
    df = sutimeLoader(df_info.loc[dd,'corpuspreparedformatelocation'],df_info.loc[dd,'sutimefileslocation'])
    
    # -----------------------------------
    # CUTTING OUT MORE REFERENCES EX-POST
    # -----------------------------------
    
    # drop duplicate rows
    df = df.drop_duplicates(subset=['Sent_ID', 'TIMEX'],keep="first") 
    
    df.loc[:,'Occurrence'] = df.groupby(['Sent_ID', 'entry_actual']).cumcount().copy() # need to give this in "index space", so subtract 1
    
    # loop over df
    df.loc[:,'ReferenceDum'] = df.apply(lambda row: referenceIsolate(row['File_ID'], row['Sent_Num'], row['entry_actual'], row['Occurrence'],df_info.loc[dd,'originalspeechespath'],"off"), axis=1)
    
    # ------------------------------------------
    # CUTTING OUT "OVERNIGHT RATES" ETC. EX POST
    # ------------------------------------------
    
    df.loc[:,'FinancialTermDum'] = df.apply(lambda row: financialTermIsolate(row['File_ID'], row['Sent_Num'], row['entry_actual'], row['Occurrence'],df_info.loc[dd,'originalspeechespath'],"off"), axis=1).copy()
    
    ## CUT OUT REFERENCES AND FINANCIAL TERMS
    df = df[df['ReferenceDum']!=1]
    df = df[df['FinancialTermDum']!=1]
    
    dc_df[dd] = df.copy()

#########################################################
## CONVERT THE OUTPUT FROM A DICTIONARY TO A DATAFRAME ##
#########################################################

df_out = dc_df[ls_cases[0]]
df_out.loc[:,'Corpus'] = ls_cases[0]

if len(ls_cases) > 0:
    for ii in ls_cases[1:len(ls_cases)]:
        df_tmp = dc_df[ii].copy()
        df_tmp.loc[:,'Corpus'] = ii 
        df_out = df_out.append(df_tmp)
      
df_out.to_pickle(output_file) 

print("")
print("## Code execution complete: run_NewFed_sutime_1_datainput.py                ")
print("## ======================================================================== ")     
print("")
