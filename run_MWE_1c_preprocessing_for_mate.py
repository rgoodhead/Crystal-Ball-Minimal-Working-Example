 # -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 2023

@author: D. BYRNE, R. GOODHEAD, M. MCMAHON, C. PARLE

NOTE:
- Designed to tokenize raw text into the way the MATE parser expects
- Will loop over the ECB speech corpus

"""

##################
## HOUSEKEEPING ##
##################

import random
random.seed(2222)

import nltk
import unicodedata
import glob

#import sys 
import os
#os.chdir(os.path.dirname(sys.argv[0]))           
#with open('working_directory.txt') as f:
#    lines = f.readlines()
#os.chdir(lines[0])  

# sent_corpus_list
sent_corpus_list = ['./data/data_MWE/corpus_prepared_for_mate/*.txt']

for d in sent_corpus_list: 
    # empty the sent_corpus/ folder
    cfiles = glob.glob(d)
    for f in cfiles:
        os.remove(f)
    
corpus_op_list = [['./data/data_MWE/sent_corpus/','./data/data_MWE/corpus_prepared_for_mate/']]

##############
## TOKENIZE ##
##############

# function to remove accented characters
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

for case in range(len(corpus_op_list)):
    fileNumber = 1
    for filename in os.listdir(corpus_op_list[case][0]): # [-200::]
        print(corpus_op_list[case][0] + filename)
        docs = open(corpus_op_list[case][0] + filename,'r',encoding="utf8")
        
        # SAVE FILES WITH A DIFFERENT SENTENCE ON EACH LINE
        # includes stop words, special characters, not tagged
        # NOTE: ideally I would remove special characters here too but PlaintextCorpusReader needs them to differentiate sentences
        fileOut1 = open(corpus_op_list[case][1] + filename,'w',encoding="utf8")
            
        for line in docs:     
            line = line.strip()
            line = nltk.sent_tokenize(line)
            line = [remove_accented_chars(sent) for sent in line]
            line = [nltk.word_tokenize(sent) for sent in line]
            
            if line not in ['\n', '\r\n']:
                for cleaned_sent in line:
                    compounded = " ".join(cleaned_sent)
                    fileOut1.write(compounded+"\n")    
            
        fileOut1.close()
