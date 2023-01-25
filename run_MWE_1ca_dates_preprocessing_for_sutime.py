# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 14:48:20 2023

@author: D. BYRNE, R. GOODHEAD, M. MCMAHON, C. PARLE

"""

##################
## HOUSEKEEPING ##
##################

import random
random.seed(2222)

import re
import glob

#import sys 
import os
#os.chdir(os.path.dirname(sys.argv[0]))            
#with open('working_directory.txt') as f:
#    lines = f.readlines()
#os.chdir(lines[0])  

# sent_corpus_list
sent_corpus_list = ['./data/data_MWE/sent_dates_corpus/*.txt']

for d in sent_corpus_list: 
    # empty the sent_corpus/ folder
    cfiles = glob.glob(d)
    for f in cfiles:
        os.remove(f)
        
corpus_op_list = [['./data/data_MWE/corpus_prepared_for_mate/','./data/data_MWE/sent_dates_corpus/']]

###################
# DROP REFERENCES #
###################

for case in range(len(corpus_op_list)):

    fileNumber = 1
    for filename in os.listdir(corpus_op_list[case][0]):
        print(corpus_op_list[case][0] + filename)
        with  open(corpus_op_list[case][0] + filename,'r',encoding="utf8") as f2:
            data = f2.read()
            #fix issues with "mid-", "late-" and so on by deleting hyphens
            data = re.sub(r'-', " ", data)
            #for the first 3 Qs, replace with word form. SUTime isn't sensitive to whether Q1 is 
            #before or after the year, and so on
            data = re.sub(r'Q1', "first quarter", data)
            data = re.sub(r'Q2', "second quarter", data)
            data = re.sub(r'Q3', "third quarter", data)
            #for both forms of Q4, replace with December
            data = re.sub(r'Q4', "December", data)
            data = re.sub(r'fourth quarter', "December", data)
            data = re.sub(r'the turn of the year', "the end of the year", data)
            data = re.sub(r'earlier in', "early", data)
            data = re.sub(r'later in', "later", data)
            #Library of important economic/financial dates, or historical dates
            data = re.sub(r'Global Financial Crisis', "2008", data)
            data = re.sub(r'global financial crisis', "2008", data)
            data = re.sub(r'the financial crisis', "2008", data)
            data = re.sub(r'GFC', "2008", data)
            data = re.sub(r'euro area crisis', "2012", data)
            data = re.sub(r'Sovereign Debt Crisis', "2012", data)
            data = re.sub(r'sovereign debt crisis', "2012", data)
            data = re.sub(r'pre crisis', "2007", data)
            data = re.sub(r'post war', "1946", data)
            data = re.sub(r'Bretton Woods system', "from 1944 to 1971 BW", data)
            data = re.sub(r'Bretton Woods era', "from 1944 to 1971 BW", data)
            data = re.sub(r'Great Depression', "1929", data)
            data = re.sub(r'Great Recession', "2008", data)
            data = re.sub(r'Gold Standard', "1870", data)
            data = re.sub(r'Volcker era', "from 1979 to 1987", data)
            data = re.sub(r'Volcker disinflation', "1981", data)
            data = re.sub(r'dot com bubble', "2000", data)
            data = re.sub(r'dotcom bubble', "2000", data)
            data = re.sub(r'Greenspan era', "from 1987 to 2006", data)
            data = re.sub(r'interwar period', "1930", data)
            data = re.sub(r'interwar', "1930", data)
            data = re.sub(r'First World War', "1914", data)
            data = re.sub(r'Great War', "1914", data)
            data = re.sub(r'World War 1', "1914", data)
            data = re.sub(r'WWI', "1914", data)
            data = re.sub(r'WW1', "1914", data)
            data = re.sub(r'Second World War', "1939", data)
            data = re.sub(r'World War 2', "1939", data)
            data = re.sub(r'WWII', "1939", data)
            data = re.sub(r'WW2', "1939", data)
            data = re.sub(r'Schuman declaration', "1950", data)
            data = re.sub(r'Schuman Declaration', "1950", data)
            data = re.sub(r'Vietnam War', "1965", data)
            data = re.sub(r'Korean War', "1950", data)
            data = re.sub(r'Gulf War', "1990", data)
            data = re.sub(r'Iraq War', "1990", data)
            data = re.sub(r'French Revolution', "1789", data)
            data = re.sub(r'Industrial Revolution', "1760", data)
            data = re.sub(r'fall of the Berlin Wall', "1989", data)
            data = re.sub(r'German reunification', "1990", data)
            data = re.sub(r'collapse of the Soviet Union', "1991", data)
            data = re.sub(r'dissolution of the Soviet Union', "1991", data)
    
            fileOut1 = open(corpus_op_list[case][1] + filename,'w',encoding="utf8")
            fileOut1.write(data)
            fileOut1.close()
