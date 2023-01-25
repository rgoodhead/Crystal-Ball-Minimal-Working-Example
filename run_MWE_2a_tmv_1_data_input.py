# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:51:55 2023

@author: cex

NOTE:
    - designed to load in the .txt files outputted by TMV annotator
    - then save tenses as data objects 

- input:  ./data/all_corpora_definitive/all_corpora_definitive/TMV/speeches/xml/*.txt
- output: ./data/merged_data/data1.pkl
    
"""

print("")
print("## ================================================================== ")
print("## Executing run_NewFed_tmv_1_data_input.py                           ")
print("")

##################
## HOUSEKEEPING ##
##################

import os
import numpy as np
import pandas as pd 

import sys
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

################
## DATA SETUP ##
################

ls_cases = ['MWE']

colnames = ['tmvfileslocation','corpuspreparedformatelocation','originalspeechespath']
df_info = pd.DataFrame(data=None, index=ls_cases, columns=colnames)

# setup: FOMC Minutes
df_info.loc['MWE','tmvfileslocation'] = "./data/data_MWE/tmv/xml/"
df_info.loc['MWE','corpuspreparedformatelocation'] = "./data/data_MWE/corpus_prepared_for_mate/"
df_info.loc['MWE','originalspeechespath'] = "./data/data_MWE/sent_dates_corpus/"

output_file = "./data/data_MWE/merged_data/data1.pkl"
 
#import contextlib
#with contextlib.suppress(FileNotFoundError):
#    os.remove(output_file)

## WARNING:
## I enforce consistency between the loaded TMV files and the files from corpus_prepared_for_mate
## some of the files in the MATE parsed folders from Dropbox include foreign language speeches
## rather than manually delete them, I choose to only load files that are also in corpus_prepared_for_mate
## the code will break if there is a file in corpus_prepared_for_mate that is NOT in tmv/xml
## however, this is probably a good thing - you need all the files gathered first

#################################
## LOAD AND PREPARE TMV OUTPUT ##
#################################

from func_basic_tmv_operations import order_tmv_output

dc_df = {}

for dd in ls_cases:
    
    print("")
    print("############################")
    print("## Loading Corpus: " + dd)
    print("############################")
    
    df = order_tmv_output(df_info.loc[dd,'corpuspreparedformatelocation'],df_info.loc[dd,'tmvfileslocation'])
    
    dc_df[dd] = df.copy()
    
df_out = dc_df[ls_cases[0]]
df_out.loc[:,'Corpus'] = ls_cases[0]

print("")
print("loading tmv information from " + str(len(np.unique(df_out.filename))) + " documents from corpus: " + ls_cases[0])

if len(ls_cases) > 0:
    for ii in ls_cases[1:len(ls_cases)]:
        df_tmp = dc_df[ii].copy()
        df_tmp.loc[:,'Corpus'] = ii 
        df_out = df_out.append(df_tmp)
        print("loading tmv information from " + str(len(np.unique(df_tmp.filename))) + " documents from corpus: " + ii)
        
print("")

## ---------------
## SAVE DATA FRAME 
## ---------------

df_out.to_pickle(output_file)

print("")
print("## Code execution complete: run_NewFed_tmv_1_data_input.py            ")
print("## ================================================================== ")
print("")
