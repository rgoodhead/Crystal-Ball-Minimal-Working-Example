# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 18:53:15 2023

@author: cex
"""

print("")
print("## ========================================================= ")
print("## Executing run_NewFed_tmv_1a_tempoword.py                  ")
print("")

##################
## HOUSEKEEPING ##
##################

#uncomment the below if you havent dled wordnet
#import nltk
#nltk.download('wordnet')

import os
import pandas as pd

import sys
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

# location of data1.pkl
outlocation = "./data/data_MWE/merged_data/"

import contextlib
with contextlib.suppress(FileNotFoundError):
    os.remove(outlocation + "data1a.pkl")
  
#####################
## LOAD DATAFRAME  ##
#####################

## LOAD TMV PARSED DATA
df = pd.read_pickle("./data/data_MWE/merged_data/data1.pkl")

import numpy as np
print("")
print("loading TMV output from " + str(len(np.unique(df.filename))) + " New Fed Data documents")
print("")

## LOAD "FUTURE" VERBS
data = pd.read_csv("./supplements/tempowordnet/verbs_95_L_edited.csv") 

#####################
## GET INFINITIVES ##
#####################

from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize('is', 'v')

df['main'] = [str(s) for s in df['main']] # 24/06/2022
df['lemma'] = df['main'].apply(lemmatizer.lemmatize,0,args='v') 

# e.g. share, accepted, spending, is, convinced ->
# share, accept, spend, be, convince

# the temporword list seems to be already in infinitives, but will make sure
data['lemma'] = data['Name'].apply(lemmatizer.lemmatize,0,args='v') 

# issue: duplicates in this dataset
# keep the version with the highest probability of being future
data2 = data.sort_values('Prob_of_being_Future',ascending=True).drop_duplicates('lemma',keep='last')

###########
## MATCH ##
###########

dfmerged = pd.merge(df, data2, on = ['lemma'], how = 'left', indicator = 'merge', validate = 'm:1')

# inspect the words from TempoWordNet which are successfully matched
dfboth = dfmerged.loc[dfmerged['merge'] == "both"]
dfboth['lemma'].value_counts()

# inspect the words from TempoWordNet which are NOT matched
dfmerged2 = pd.merge(df, data2, on = ['lemma'], how = 'right', indicator = 'merge', validate = 'm:1')
dfboth2 = dfmerged2['lemma'].loc[dfmerged2['merge'] == "right_only"]
dfboth2 = dfboth2.to_frame()
dfboth2['lemma'].value_counts()

# randomly inspect some examples of matched sentences
random_subset = dfboth.sample(n=5)
with pd.option_context('display.max_rows', None, 'display.max_columns', None,'display.max_colwidth', None):  # more options can be specified also
    print(random_subset[['Unique_ID','main','lemma','Prob_of_being_Future']])
    print(random_subset[['sent']])

## ---------------------
## SANITY CHECK EXERCISE
## ---------------------

#from func_basic_tmv_operations import sanityCheckTMV

#sanityCheckTMV(df,originalfilespath,"EUS")

##############################################
## CREATE A NEW DEFINITION OF PRESENT TENSE ##
##############################################
  
#df_join.to_pickle("./merged_data/datatest1.pkl")
dfmerged.to_pickle(outlocation + "data1a.pkl")

print("")
print("storing TMV output from " + str(len(np.unique(dfmerged.filename))) + " speeches from the New Fed dataset")
print("")

print("")
print("## Code execution complete: run_NewFed_tmv_1a_tempoword.py   ")
print("## ========================================================= ")
print("")