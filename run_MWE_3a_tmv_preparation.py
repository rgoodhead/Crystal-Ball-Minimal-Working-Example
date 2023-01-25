# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:57:08 2023

@author: cex
"""

print("")
print("## ============================================= ")
print("## Executing run_NewFed_tmv_preparation.py       ")
print("")

import pandas as pd
import numpy as np
import re

import sys
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

##################
## HOUSEKEEPING ##
##################

in_file = "./data/data_MWE/merged_data/data1a.pkl"

###################
## LOAD TMV DATA ##
###################

df = pd.read_pickle(in_file)

df["File_ID"] = [re.split("_S\d+$",s)[0] for s in df.Sent_ID]

print("")
print("loading TMV information from " + str(len(np.unique(df.File_ID))) + " New Fed data files")
print("")

##########################
## BASIC TMV OPERATIONS ##
##########################

from func_basic_tmv_operations import basicTMVOperations_general

dfb, df_all = basicTMVOperations_general(df,"\d{8}")

dfb.to_pickle("./data/data_MWE/merged_data/data_TMV_cleaned.pkl")

print("")
print("## Executing run_NewFed_tmv_preparation.py      ")
print("## ============================================ ")
print("")
