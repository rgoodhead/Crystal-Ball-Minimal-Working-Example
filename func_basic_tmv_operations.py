# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 19:30:55 2021

@author: Utente
"""

import pandas as pd
import os
import numpy as np
import re

def speakerReassign(dfb):
    
    pd.options.mode.chained_assignment = None 
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Willem F. Duisenberg,Eugenio Domingo Solans', value='D.berg/Solans', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Jean_Claude Trichet', value='Trichet', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Benoît Cœuré', value='Cœuré', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Mario Draghi', value='Draghi', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Lorenzo Bini Smaghi', value='Bini Smaghi', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Vítor Constâncio', value='Constâncio', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Gertrude Tumpel_Gugerell', value='Tumpel-Gugerell', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Yves Mersch', value='Mersch', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Peter Praet', value='Praet', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Willem F. Duisenberg', value='Duisenberg', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='José Manuel González_Páramo', value='González-Páramo', regex=True)
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Lucas Papademos', value='Papademos', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Otmar Issing', value='Issing', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Sabine Lautenschläger', value='Lautenschläger', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Jürgen Stark', value='Stark', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Tommaso Padoa_Schioppa', value='Padoa-Schioppa', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Eugenio Domingo Solans', value='Solans', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Jörg Asmussen', value='Asmussen', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Sirkka Hämäläinen', value='Hämäläinen', regex=True) 
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Luis de Guindos', value='de Guindos', regex=True) 
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Christian Noyer', value='Noyer', regex=True) 
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Philip R. Lane', value='Lane', regex=True)              
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Christine Lagarde', value='Lagarde', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Isabel Schnabel', value='Schnabel', regex=True)  
    dfb["Speaker"] = dfb["Speaker"].replace(to_replace='Fabio Panetta', value='Panetta', regex=True)                  

    return dfb

def createContinuousMeasureTMV(df_in,colStr,timeStr,agg_level_,order):
    
    dum_mat_T = pd.get_dummies(df_in[colStr])
    dum_mat_T['Sent_ID'] = df_in['Sent_ID']
    dum_mat_T[agg_level_] = df_in[agg_level_]
    dum_mat_T = dum_mat_T.rename(columns={"future": "future_dum", "past": "past_dum", "pres": "pres_dum" })
    dum_mat_T[order] = df_in[order]
    
    # future interactions
    timeStr_in = timeStr + "_dum"
    dum_mat_T_fut = dum_mat_T[dum_mat_T[timeStr_in]==1].copy()
    dum_mat_T_int_fut = dum_mat_T_fut[order].copy()
    if timeStr == "future":
        intlist = [s + '_int_fut_tmv' for s in order]
    if timeStr == "past":
        intlist = [s + '_int_pst_tmv' for s in order]    
    dum_mat_T_int_fut.columns = intlist
    dum_mat_T_int_fut[agg_level_] = dum_mat_T_fut[agg_level_].copy()
    df_in_shares_fut = dum_mat_T_int_fut.groupby(agg_level_).mean().copy()
    df_in_shares_fut = df_in_shares_fut.reset_index()   
    
    return df_in_shares_fut

def tenseAggregate(df):
    
    df_all = df.copy() # keep the non-finite verbs
    
    # new dataframe just with finite verbs - all tables are based on this denominator
    dfb = df[df['finite']=="yes"].copy()
    
    # create simplified verb lists
    past_list = ['past', 'pastPerf', 'pastPerfProg', 'pastProg']
    pres_list = ['pres', 'presPerf', 'presPerfProg', 'presProg']
    future_list = ['futureI', 'futureIIProg', 'futureII', 'futureIProg']
    
    # conditional may not really be important
    cond_list = ['condI', 'condIProg', 'condII', 'condIIProg']
    
    # the conditional 2 group points to the past, conditional 1 group points to the future
    past_list2 = ['past', 'pastPerf','pastPerfProg','pastProg', 'condII', 'condIIProg']
    future_list2 = ['futureI', 'futureIIProg', 'futureII', 'futureIProg', 'condI', 'condIProg']
    
    # create first simplified tense variable
    dfb.loc[dfb['tense'].isin(past_list), 'tense2'] = 'past'
    dfb.loc[dfb['tense'].isin(pres_list), 'tense2'] = 'pres'
    dfb.loc[dfb['tense'].isin(future_list), 'tense2'] = 'future'
    dfb.loc[dfb['tense'].isin(cond_list), 'tense2'] = 'cond'
    
    # create first simplified tense variable
    dfb.loc[dfb['tense'].isin(past_list2), 'tense3'] = 'past'
    dfb.loc[dfb['tense'].isin(pres_list), 'tense3'] = 'pres'
    dfb.loc[dfb['tense'].isin(future_list2), 'tense3'] = 'future'
    
    ## CREATE A REFINED MEASURE OF PRESENT TENSE USING TEMPOWORDNET 

    dfb.loc[:,'tense4'] = dfb['tense3'].copy()

    dfb.loc[((dfb['Prob_of_being_Future'] > 0.95) & (dfb['tense3'] == "pres")) , 'tense4'] = "future"

    # create first simplified tense variable
    df_all.loc[df_all['tense'].isin(past_list), 'tense2'] = 'past'
    df_all.loc[df_all['tense'].isin(pres_list), 'tense2'] = 'pres'
    df_all.loc[df_all['tense'].isin(future_list), 'tense2'] = 'future'
    df_all.loc[df_all['tense'].isin(cond_list), 'tense2'] = 'cond'
    
    # create first simplified tense variable
    df_all.loc[df_all['tense'].isin(past_list2), 'tense3'] = 'past'
    df_all.loc[df_all['tense'].isin(pres_list), 'tense3'] = 'pres'
    df_all.loc[df_all['tense'].isin(future_list2), 'tense3'] = 'future'
    
    ## CREATE A REFINED MEASURE OF PRESENT TENSE USING TEMPOWORDNET 

    df_all.loc[:,'tense4'] = df_all['tense3'].copy()

    df_all.loc[((df_all['Prob_of_being_Future'] > 0.95) & (df_all['tense3'] == "pres")), 'tense4'] = "future"
    
    return dfb, df_all
    
def basicTMVandTopicOperations_general(df,pattern_in_fname,K): 
    
    # NOTE:
    # - the topics do not vary at the verb-phrase level, only the sentence level
    # - this means sum(future|topic) can include multiple observations on future verb-phrases from the same sentence
    # - this may be an issue, in the sense that sum(future|topic) may be inflated by multiple future verb-phrases in a given sentence
    # - further, the same topic can include verb-phrases from different tenses, meaning sentences can count towards different totals
    # - potential solution: assign a sentence to a given tense *if* it includes at least one example of this tense
    # - but this would probably lead to all sentences being classified as present, and almost all sentences being classified as future/past (you just need one verb)
    # - alternative solution: assign sentence to the tense with the *most* verb-phrases 
    # - but this would lead to almost all tenses being assigned present, and the few sentences classified as "future" or "past" might be quite odd constructions
    # - conclusion: it is probably best just to leave it as it is
    
    # Example representation of the data...
    #
    # DATE      SPEECH      SENTENCE    VERB    TOPIC
    # -----------------------------------------------
    # 2000      speech1     S1          1       8
    # 2000      speech1     S1          2       8
    # 2000      speech1     S2          1       9
    # ...
    # 2000      speech2     S1          1       10
    # ...
    # 2006      speech5     S9          4       4
    
    # for each speech and sentence, identify the largest topic (conditional on it being greater than a cut-off %)
    # if there is no topic greater than a cut-off %, assign the topic to zero
  
    df.loc[:,'Speech'] = df.loc[:,'File_ID'].copy() 
    
    chk = [re.search(pattern_in_fname,s)[0] for s in df['Sent_ID']]
    chk = [s.replace("_","") for s in chk]
    
    df.loc[:,'Year'] = [int(s[0:4]) for s in chk]
    df.loc[:,'Month'] = [int(s[4:6]) for s in chk]
    df.loc[:,'Day'] = [int(s[6:8]) for s in chk]
    
    df.loc[:,'Quarter'] = np.ceil(df['Month']/3)
    df.loc[:,'YM_num'] = df['Year'] + (df['Month']-1)/12
    df.loc[:,'YQ_num'] = df['Year'] + (df['Quarter']-1)/4
    
    df.loc[:,'Datetime'] = pd.to_datetime(df.loc[:,'Year'].copy().apply(str) + "/" + df.loc[:,'Month'].copy().apply(str) + "/" + df.loc[:,'Day'].copy().apply(str), format='%Y%m%d', errors='ignore')
    
    ## -----------------------------------------------------------
    ## "FIRST-PAST-THE-POST WITH QUORUM" SENTENCE-TOPIC ASSIGNMENT
    ## -----------------------------------------------------------
    
    # implies a sentence can only be about one topic
    
    # apply a max function to the topics
    topicnms = list(range(1, K+1))
    topicnms = ["t_" + str(e) for e in topicnms]
    topics = df[topicnms].copy()
    
    df.loc[:,'topics_win'] = topics.max(axis=1)
    df.loc[:,'topics_id'] = topics.idxmax(axis=1) # NOTE: you need all of the topics in ascending order for the id to map to the topics
    # NOTE: this does NOT make the mistake of assigning the first column a zero index, when it needs to be 1
    
    # extra step to replace with (non-existent) topic = 0 if the winning topic < 20%
    df.loc[df['topics_win'] < 0.2, 'topics_id'] = 0
    
    ## ---------------------------------------------------
    ## TOP THREE TOPICS (GREATER THAN A QUORUM) ASSIGNMENT
    ## ---------------------------------------------------
    
    sorttopics1 = pd.DataFrame(np.sort(topics)).copy()
    sorttopics1.columns = topicnms
    sorttopics2 = pd.DataFrame(np.argsort(topics)+1)

    top3 = sorttopics2[sorttopics2.columns[-3:]].copy()
    top3.columns = ['win3','win2','win1']
    df['win3'] = top3['win3'].copy()
    df['win2'] = top3['win2'].copy()
    df['win1'] = top3['win1'].copy() # this is just the maximum
    
    dfb, df_all = tenseAggregate(df)
    
    return dfb, df_all

def basicTMVOperations_general(df,pattern_in_fname):
    
    df.loc[:,'Speech'] = df.loc[:,'File_ID'].copy() 
    
    chk = [re.search(pattern_in_fname,s)[0] for s in df['Sent_ID']]
    chk = [s.replace("_","") for s in chk]
    
    df.loc[:,'Year'] = [int(s[0:4]) for s in chk]
    df.loc[:,'Month'] = [int(s[4:6]) for s in chk]
    df.loc[:,'Day'] = [int(s[6:8]) for s in chk]
    
    df.loc[:,'Quarter'] = np.ceil(df['Month']/3)
    df.loc[:,'YM_num'] = df['Year'] + (df['Month']-1)/12
    df.loc[:,'YQ_num'] = df['Year'] + (df['Quarter']-1)/4
    
    df.loc[:,'Datetime'] = pd.to_datetime(df.loc[:,'Year'].copy().apply(str) + "/" + df.loc[:,'Month'].copy().apply(str) + "/" + df.loc[:,'Day'].copy().apply(str), format='%Y%m%d', errors='ignore')
    
    dfb, df_all = tenseAggregate(df)
    
    return dfb, df_all

def order_tmv_output(corpuspreparedformatelocation,tmvlocation):
        
    #need to make an acceptable tense list
    #reason - lack of cleaning of punctuation leads to errors in TMV output, causing too many columns
    #to be created. these are offset from each other, causing errors in creation of new variables
    #so drop (rare) rows with tense errors. these could be kept if punctuation were cleaned first
    tense_list = [ 'pres', 'past', '-', 'futureI', 'condI', 'condII', 'presPerf', \
                   'pastPerf', 'futureIIProg', 'futureII', 'condIIProg', \
                   'presPerfProg', 'pastPerfProg', 'futureIProg', 'condIProg', \
                   'pastProg', 'presProg', 'main' ]
    
    #create empty dataframe for starting the append
    df_join = pd.DataFrame(data=None)   
    
    empty_speeches_list = list()   
    for filename in os.listdir(corpuspreparedformatelocation): # file names come from corpus_prepared_for_mate
        # this ensures consistency between corpora 
        # but will cause the loop to break if you haven't applied TMV to all the files
        
        filenamenoext = os.path.splitext(filename)[0]
        print(filenamenoext)
        
        with open(tmvlocation + filenamenoext + '.html', 'r', encoding="utf8") as file:
            
            dfs = pd.read_html(file, header=0)
            
            # saves as list, need to access first element to get the dataframe    
            df = dfs[0]
            
            # drop all wrong tenses
            df = df[df['tense'].isin(tense_list)]
            
            # drop any wrongly added columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            # create a variable to save the ID of the speech, minus the ".html"
            df["filename"] = filenamenoext
            
            # save sentence number for creating sentence and speech ID (not unique - multiple verbs)
            df['sent_nr'] = "S" + df['sent nr'].astype(str)
            df['Sent_ID'] = df[['filename', 'sent_nr']].agg('_'.join, axis=1)
            
            # count verbs for making unique ID of speech, sentence, verb
            df['count'] = df.groupby((df['sent nr'] != df['sent nr'].shift(1)).cumsum()).cumcount()+1
            df['Verb_count'] = "V"+df['count'].astype(str)
            df=df.drop(['count'], axis=1)
            df['Unique_ID'] = df[['Sent_ID', 'Verb_count']].agg('_'.join, axis=1)
            
            if df.empty:
                empty_speeches_list.append(filenamenoext) 
                
            # join each df to the aggregate df_join
            frames = [df_join, df]
            df_join = pd.concat(frames)
            
    return df_join

def metaDataMergeECBStatements(df):
    
    df2 = pd.read_excel(r"./data/ListofPresidents.xlsx")

    #for subsetting on years
    #df2['Year'] = [(x[4:8]) for x in df2['Speech']]
    df['Year'] = [(pd.to_numeric(x[0:4])) for x in df['filename']]
    df['Month'] = [(pd.to_numeric(x[6:7])) for x in df['filename']]
    df['YM_num'] = df['Year'] + (df['Month']-1)/12
    
    df2['YM_num'] = df2['Year'] + (df2['Month']-1)/12
    df2=df2.drop(['Year','Month'],axis=1)
    
    df=df.merge(df2, on='YM_num', how='left')
    df=df.rename(columns={"President":"Speaker"})
    df=df.drop(['merge'],axis=1)
    
    return df

def topicMerge(df,dataTopics,suffix):
    
    # NOTE:
    # want to input files of the form:
    # rn: 1998_06_09_S.60
    # these are the statements
        
    chk = dataTopics['rn'].str.split(pat='.',expand=True)
    dataTopics['Statement'] = chk[0]
    dataTopics['sent nr'] = chk[1]
        
    # restrict to the STATEMENTS
    chk[3] = [s[-2:] for s in chk[0]]
    dataTopics = dataTopics[chk[3]==suffix].copy()
    
    print("")
    print("loading topic information from " + str(len(np.unique(dataTopics.Statement))) + " statements")
    print("loading topic information from " + str(len(np.unique([ s.split(suffix)[0] for s in dataTopics.Statement]))) + " statement days")
    print("")
        
    dataTopics.loc[:,'sent nr'] = dataTopics['sent nr'].astype(int).copy()
    dataTopics = dataTopics.sort_values(by = ['Statement','sent nr']).copy()
        
    print("")
    print("loading TMV information from " + str(len(np.unique([s.split(suffix)[0] for s in df.filename]))) + " statement days")
    print("")
    
    df['sent nr'] = df['sent nr'].astype(int).copy()
    dataTopics['sent nr'] = dataTopics['sent nr'].astype(int).copy()
        
    dfmerged2 = pd.merge(df, dataTopics, left_on = ['filename','sent nr'], right_on = ['Statement','sent nr'], how = 'left', indicator = 'merge2', validate = 'm:1') # 
    # note that the topic probabilities are at the sentence level
    # the tmv output is at the tense-expression level
    # therefore the topic probabilities are repeated across the tense-expressions for given sentences
    dfmerged2 = dfmerged2.sort_values(by = ['Statement','sent nr']).copy()
        
    dfmerged2['Statement'] = dfmerged2['filename'].copy()
    
    ## NOTE: some sentences do not get topic scores (zero tokens post tokenisation)

    return dfmerged2
    
def match_tmv_tempoword(df):
    
    import numpy as np
    print("")
    print("loading TMV output from " + str(len(np.unique(df.filename))) + " files")
    print("")
    
    ## LOAD "FUTURE" VERBS
    data = pd.read_csv("./output/tempowordnet/verbs_95_L_edited.csv") 
    
    #####################
    ## GET INFINITIVES ##
    #####################
    
    from nltk.stem.wordnet import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatizer.lemmatize('is', 'v')
    
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
        
    # return dfmerged not dfmerged2    
        
    return dfmerged
    
# sanity check exercise
# load a sentence from the data pre-MATE parser
# compare it to the sent column for the relevant Sent_ID from the df
def sentencefinder(originalspeechespath,fileofinterest,snm):
    print(fileofinterest)
    docs = open(originalspeechespath + fileofinterest,'r',encoding="utf8")
    for i, line in enumerate(docs):
        if i == snm - 1:
            print(line)

def sanityCheckTMV(df,originalfilespath,dum_case):
    
    # the below loop compares 5 random sentences from the dataset (to help spot bugs)
    cut = df['Sent_ID'].sample(n = 5, replace = False) 
    
    cut_l = [s.split("_S",1)[0] for s in cut]
        
    cut_s = [s.split("_S",1)[1] for s in cut]
    
    if dum_case == "S":
        cut_s = [s.split("_S",1)[1] for s in cut_s]
        cut_l = [s + "_S" for s in cut_l]
        
    counter = 1
    for a, b in zip(cut_l,cut_s):
        print("")
        print("===== ===== ===== ===== =====")
        print("Example #" + str(counter))
        print("===== ===== ===== ===== =====")
        print("")
        sentencefinder(originalfilespath,a + ".txt",int(b))
        
        fname = a + "_S" + str(b)
        dfout = df.loc[df['Sent_ID'] == fname]
        print(dfout['sent'].iloc[0])
        
        print(" ")
        print("Verbal complexes identified")
        print(dfout["verbal complex"])
        
        counter = counter + 1   