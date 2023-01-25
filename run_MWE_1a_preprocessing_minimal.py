# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:24:28 2023

@author: D. BYRNE, R. GOODHEAD, M. MCMAHON, C. PARLE
    
"""

##################
## HOUSEKEEPING ##
##################

import random
random.seed(2222)

import nltk
import glob

#import sys 
import os

# sent_corpus_list
sent_corpus_list = ['./data/data_MWE/sent_corpus/*.txt']

for d in sent_corpus_list: 
    # empty the sent_corpus/ folder
    cfiles = glob.glob(d)
    for f in cfiles:
        os.remove(f)
    
corpus_op_list = [['./data/data_MWE/corpus/','./data/data_MWE/sent_corpus/']]

###################
## SENT TOKENIZE ##
###################

for case in range(len(corpus_op_list)):
    fileNumber = 1
    for filename in os.listdir(corpus_op_list[case][0]):
        if filename[-4:] == ".txt":
            print(corpus_op_list[case][0] + filename)
            docs = open(corpus_op_list[case][0] + filename,'r',encoding="utf8")
            
            # SAVE FILES WITH A DIFFERENT SENTENCE ON EACH LINE
            # includes stop words, special characters, not tagged
            # NOTE: ideally I would remove special characters here too but PlaintextCorpusReader needs them to differentiate sentences
            fileOut1 = open(corpus_op_list[case][1] + filename,'w',encoding="utf8")
                
            for line in docs:     
                line = line.strip()
                line = nltk.sent_tokenize(line)
        
                for cleaned_sent in line:
                    text = cleaned_sent
                    fileOut1.write(text+"\n")    
                
            fileOut1.close()
