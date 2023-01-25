# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:55:34 2023

@author: cex
"""

import pandas as pd
import numpy as np
import os

import sys
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

##################
## HOUSEKEEPING ##
##################

#path = "C:/Users/Dave/Documents/Communications/text_mining_resources"
#path = "C:/Users/cex/Documents/RESEARCH/Future-Text-Mining"
#os.chdir(path)

idx = pd.IndexSlice

#originalspeechespath = "./data/all_corpora_definitive/EUSpeech/sent_dates_corpus/"

input_file = "./data/data_MWE/merged_data/data_SUTime2.pkl"

######################
## LOAD SUTIME DATA ##
######################

df_ST = pd.read_pickle(input_file)

# print("")
# print("loading SUTime output from " + str(len(np.unique(df_ST.File_ID))) + " speeches from the EUSpeech dataset")
# print("")
# # extract the file name and sentence number
# spl = [s.split("_S") for s in df_ST['Sent_ID']]
# spl1 = [i[0] for i in spl]
# spl2 = [int(i[1]) for i in spl]
# df_ST['Speech'] = spl1
# df_ST['sent nr'] = spl2

df = df_ST.copy()

# ## SANITY CHECK EXERCISE
# # load the original sentence for a randomly selected sentence
# # examine the winning topic for that sentence
# def sentencefinder(df,originalspeechespath,fileofinterest,sentenceofinterest):
#     print("")
#     print("----- Sentence ID -----")
#     print(fileofinterest + "_" + "S" + str(sentenceofinterest))
#     print("")
#     print("----- Original Sentence -----")
#     docs = open(originalspeechespath + fileofinterest + ".txt",'r',encoding="utf8")
#     for i, line in enumerate(docs):
#         if i == sentenceofinterest - 1:
#             print(line)
            
#     # locate the sentence in the data frame
#     dfout = df.loc[df['Sent_ID'] == fileofinterest + "_" + "S" + str(sentenceofinterest) ]
#     print("----- SUTime Output -----")
#     for jj in range(1,len(dfout)+1):
#         print("Tag #" + str(jj))
#         print("SUTime Info: date_type = " + dfout['date_type'].iloc[jj-1] +   " | " + "value_type = " + dfout['value_type'].iloc[jj-1] + " | " + "range_type = " + dfout['range_type'].iloc[jj-1] + " | " + "entry_actual = " + dfout['entry_actual'].iloc[jj-1])
#         print("")
    
#     return dfout

# # use the below code to compare a speech of particular interest
# fileofinterest = "EUSP_EC_2007_01_04" # "ECB_1997_02_07_N1" 
# sentenceofinterest = 10 # function call takes row subtract one (zero indexing accounted for)
# #dfout = sentencefinder(df,originalspeechespath,fileofinterest,sentenceofinterest)

# # the below loop compares 5 random sentences from the dataset (to help spot bugs)
# cut = df['Sent_ID'].sample(n = 5, replace = False)  
# cut_l = [s.split("_S",1)[0] for s in cut]
# cut_s = [s.split("_S",1)[1] for s in cut]
# counter = 1
# for a, b in zip(cut_l,cut_s):
#     print("")
#     print("===== ===== ===== ===== =====")
#     print("Example #" + str(counter))
#     print("===== ===== ===== ===== =====")
#     dfout = sentencefinder(df,originalspeechespath,a,int(b))   
#     counter = counter + 1
# print("")

##################################
## BASIC SUTIME DATA OPERATIONS ##
##################################

from func_basic_sutime_operations import dataOperations_general

#df_new = dataOperations_EUSpeech(df)

# US_M, US_PC, US_S
# US_S: S_19940204
# US_M: 19760120, VC_20140304, CC_20010113
# US_PC: 20110427_Q, 20211215_S, 20110427_A

# each Corpus encases the date in the filename in a different way
# want to write a code that can /generally/ extract the corpora

pattern_in_fname = "\d{8}"
df_new = dataOperations_general(df,pattern_in_fname)

# sort the data
df_new = df_new.sort_values(by=['Corpus','Year','Month','Day','Sent_Num'])

# this is useful for the creation of the union interaction terms
df_new.to_pickle("./data/data_MWE/merged_data/data_SUTime_cleaned.pkl")

print("")
print("## Code execution complete: run_NewFed_sutime_preparation.py ")
print("## =========================================================== ")
print("")