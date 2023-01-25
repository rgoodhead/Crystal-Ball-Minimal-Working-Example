# -*- coding: utf-8 -*-
"""

Created on Sat Dec 19 09:45:07 2020

@author: R. GOODHEAD

formerly called "func_sutime_basic_data_operations.py"
renamed for consistency 

"""

import pandas as pd
import numpy as np
from numpy import nanmean
import re
import os

def is_file_empty(file_name):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.isfile(file_name) and os.path.getsize(file_name) == 0

def sutimeLoader(corpuspreparedformatelocation,sutimefileslocation):
    
    ## WARNING:
    ## I enforce consistency between the loaded TMV files and the files from corpus_prepared_for_mate
    ## some of the files in the MATE parsed folders from Dropbox include foreign language speeches
    ## rather than manually delete them, I choose to only load files that are also in corpus_prepared_for_mate
    ## the code will break if there is a file in corpus_prepared_for_mate that is NOT in tmv/xml
    ## however, this is probably a good thing - you need all the files gathered first

    df_join = pd.DataFrame(data=None)   

    for filename in os.listdir(corpuspreparedformatelocation):
        # this ensures consistency between corpora 
        # but will cause the loop to break if you haven't applied SUTime to all the files
        
        filenamenoext = os.path.splitext(filename)[0]
        
        empty_file_list = list()
        if is_file_empty(sutimefileslocation + filenamenoext + '.txt') == True:
            print("WARNING: SUTime output file empty - " + filenamenoext)
            empty_file_list.append(filenamenoext)
        else: 
            print(filenamenoext)
            with open(sutimefileslocation + filenamenoext + '.txt','r', encoding="utf8") as file:
                    
                df = pd.read_csv(file, header=0, delimiter=" <TIMEX3 ")
                # find the segment between quotation marks following type
                # need to use list comprehension to do this in pandas
                df['date_type'] = [re.findall(r'type=(.*?".*?)"', x) for x in df['TIMEX']]
                #convert the list to string in each place
                df['date_type'] = [','.join(map(str, x)) for x in df['date_type']]
                #drop the leading quotation mark
                df['date_type'] = [(x[1:]) for x in df['date_type']]
                # value
                df['value_type'] = [re.findall(r'value=(.*?".*?)"', x) for x in df['TIMEX']]
                df['value_type'] = [','.join(map(str, x)) for x in df['value_type']]
                df['value_type'] = [(x[1:]) for x in df['value_type']]
                # mod - like early/late
                df['mod_type'] = [re.findall(r'mod=(.*?".*?)"', x) for x in df['TIMEX']]
                df['mod_type'] = [','.join(map(str, x)) for x in df['mod_type']]
                df['mod_type'] = [(x[1:]) for x in df['mod_type']]
                # range of dates if one exists
                df['range_type'] = [re.findall(r'range=(.*?".*?)"', x) for x in df['TIMEX']]
                df['range_type'] = [','.join(map(str, x)) for x in df['range_type']]
                df['range_type'] = [(x[1:]) for x in df['range_type']]
                #get the actual entry, for doing types of future_ref
                df['entry_actual'] = [re.findall(r'(?<=>).*?<', x) for x in df['TIMEX']]
                df['entry_actual'] = [','.join(map(str, x)) for x in df['entry_actual']]
                df['entry_actual'] = [(x[:-1]) for x in df['entry_actual']]
                
                if len(df) > 0:
                    df.loc[:,'File_ID'] = filenamenoext # separate file ID
                    df.loc[:,'Sent_Num'] = [int(re.split("_S",t)[1]) for t in [re.findall("_S\d+$",s)[0] for s in df['Sent_ID']].copy()] # separate sentence number
                    
                    # overwrite Sent_ID (n.b. in rare occurrences the file name was changed but this is not reflected in the output - this step corrects this issue - the name is the filename)
                    df.loc[:,'Sent_ID'] = [ filenamenoext + "_S" + str(s) for s in df.loc[:,'Sent_Num']]
                    
                frames = [df_join, df]
                df_join = pd.concat(frames)
        
    if len(empty_file_list) > 0:
        print("WARNING:")
        print("the following SUTime output files are empty - ")
        print(empty_file_list)
        
    df = df_join.copy()
    
    return df

def sutimeDateTreatment(df):
    
    # relating to the /speech/, and not the reference
    # DatetimeSpeech64
    # Year, Month, Day, YM_num, YQ_num
    # Datetime

    # dates relating to the /reference/, not the speech itself
    # Datetime64
    # Year2, Month2, Day2, YM_num2, YQ_num2
    # Datetime2

    # drop durations, etc. keep only dates
    # NOTE - should we look at durations more?
    df = df[df['date_type']=="DATE"].copy()
    
    # convert decade references to the first year
    df.loc[:,'value_type'] = [x.replace("X", "0") for x in df['value_type']]
    # NOTE: this cause problems in cases such as
    # Index: 82, value_type 	1998 INTERSECT (1994-XX-XX,XXXX-5-31,PT-17475432H)
    # though these are actually dropped
    
    # drop season modifiers
    df.loc[:,'value_type'] = [x.replace("-SU", "") for x in df['value_type']]
    df.loc[:,'value_type'] = [x.replace("-AU", "") for x in df['value_type']]
    df.loc[:,'value_type'] = [x.replace("-FA", "") for x in df['value_type']]
    df.loc[:,'value_type'] = [x.replace("-WI", "") for x in df['value_type']]
    df.loc[:,'value_type'] = [x.replace("-SP", "") for x in df['value_type']]
    
    pres_list = ['PRESENT_REF']
    past_list = ['PAST_REF']
    future_list = ['FUTURE_REF']
    time_list = ['PRESENT_REF', 'PAST_REF', 'FUTURE_REF']
    
    # create a new variable with categorical
    # NOTE: 
    # df['value_type'] includes e.g. both PRESENT_REF and 1997-02-07
    # df['new_col'] will replace 1997-02-07 with NaN
    df.loc[df['value_type'].isin(pres_list), 'new_col'] = 'PRESENT_REF'
    df.loc[df['value_type'].isin(past_list), 'new_col'] = 'PAST_REF'
    df.loc[df['value_type'].isin(future_list), 'new_col'] = 'FUTURE_REF'

    ############################################
    ## CONVERT NUMERICAL DATES TO CATEGORICAL ##   
    ############################################
    
    # create a new variable with the values, keep only numerical (categorical replaced with NaN)
    df['new_value'] = df['value_type'].copy()
    df.loc[df['new_value'].isin(time_list),'new_value'] = np.nan
    
    # split off the categorical into new dataframe
    df_cat = df[df['new_value'].isna()].copy() # df_cat contains the PRESENT_REF, PAST_REF, FUTURE_REF, as assigned by SUTime
    
    # keep only numerical
    df = df[df['new_value'].notna()].copy() # df contains the e.g. 1997-02-07, not the PRESENT_REF
    
    # convert to string for purpose of trimming off extra characters
    df.loc[:,'new_value2'] = [str(x) for x in df['new_value']].copy()
    df.loc[:,'new_value2'] = [x[0:10] for x in df['new_value2']].copy()
    
    # get rid of dates that are "intersect" with another type of expression
    sep = ' '
    df.loc[:,'new_value2'] = [x.split(sep, 1)[0] for x in df['new_value2']].copy()
    
    # catch negative dates or other oddities and drop them
    df.loc[:,'minus_check'] = [x[0] for x in df['new_value2']].copy()
    
    # drop any "date" which is not in the 1000s or 2000s
    acceptable_list = ['2','1']
    df = df[df['minus_check'].isin(acceptable_list)].copy()
    df = df.drop(columns=['minus_check'])
    # split out date
    chk = df['new_value2'].str.split(pat='-', n=-1, expand=True)
    df['chk0'] = chk[0]
    df['chk1'] = chk[1]
    df['chk2'] = chk[2]

    # if year is non missing but month and day are, set them to be 01 01
    df['chk1'] = df['chk1'].fillna("01")
    df['chk2'] = df['chk2'].fillna("01")

    # make a list of acceptable days of the month
    acceptable_dates = ['01', '02', '03', '04', '05', '06', '07',
                    '08', '09', '10', '11', '12', '13', '14',
                    '15', '16', '17', '18', '19', '20', '21',
                    '22', '23', '24', '25', '26', '27', '28', # Rob: mistake spotted here 2020/09/30, missing comma
                    '29', '30', '31']
    # NOTE: some of these just have "W" - why?

    # replace any non-days with the first of the month
    df.loc[:,'chk2'] = np.where(~df['chk2'].isin(acceptable_dates), '01', df['chk2']) 
    
    # list of quarters
    q1_list = ['Q1']
    q2_list = ['Q2']
    q3_list = ['Q3']
    q4_list = ['Q4']

    # replace any quarters with the first month of the quarter
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q1_list), '01', df['chk1'])
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q2_list), '04', df['chk1']) 
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q3_list), '07', df['chk1']) 
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q4_list), '10', df['chk1'])

    # make list of weeks in quarter (only has to be rough + remember leap years)
    # problem is the weeks of the year can vary in terms of associated month
    # so convert them to quarter (which doesn't change) and then to 
    # month as per the code immediately above. Is this too ad hoc?
    q1_listm = ['W00', 'W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W07', 'W08', 'W09', # ROB: added 'W00' here
                'W10', 'W11', 'W12', 'W13']
    q2_listm = ['W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W20', 'W21', 'W22', 
                'W23', 'W24', 'W25', 'W26']
    q3_listm = ['W27', 'W28', 'W29', 'W30', 'W31', 'W32', 'W33', 'W34', 'W35',
                'W36', 'W37', 'W38', 'W39']
    q4_listm = ['W40', 'W41', 'W42', 'W43', 'W44', 'W45', 'W46', 'W47', 'W48', 
                'W49', 'W50', 'W51', 'W52', 'W53']

    # replace any weeks with the first month of the quarter they are in
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q1_listm), '01', df['chk1'])
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q2_listm), '04', df['chk1']) 
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q3_listm), '07', df['chk1']) 
    df.loc[:,'chk1'] = np.where(df['chk1'].isin(q4_listm), '10', df['chk1'])
    
    df.loc[:,'Year2'] = pd.to_numeric(df['chk0'], errors="coerce")

    df.loc[:,'Month2'] = pd.to_numeric(df['chk1'], errors="coerce")
    # Rob: there is one value that is not picked up, 1987-W00-1?

    df.loc[:,'Day2'] = pd.to_numeric(df['chk2'], errors="coerce")

    df.loc[:,'Quarter2'] = np.ceil(df['Month2']/3)
    df.loc[:,'YM_num2'] = df['Year2'] + (df['Month2']-1)/12
    df.loc[:,'YQ_num2'] = df['Year2'] + (df['Quarter2']-1)/4
    
    # WEEKEND ISSUE
    # very rare
    ln_bug = len(df) - len(df.loc[df['chk1'] != "WE",:])
    if ln_bug > 0:
        print("WARNING! weekend bug in date")
        print("number of cases affected: " + str(ln_bug))
        
    df = df.loc[df['chk1'] != "WE",:].copy()
    
    df.loc[:,'Datetime2'] = pd.to_datetime(df['chk0'] + "/" + df['chk1'] + "/" + df['chk2'], format='%Y%m%d', errors='ignore')

    indt = df['chk0'] + "-" + df['chk1'] + "-" + df['chk2']
    outd = [ np.datetime64(ss,'D') for ss in indt ]
    df['Datetime64'] = outd.copy()
    
    df = df.drop(columns=['chk0','chk1','chk2'])
    
    return df, df_cat

def additionalCleaningSteps(df):
    ## CLEAN OUT EXTREME YEARS
    # year cleaning codes (cut out extreme observations)
    # may want to change this
    df = df[df['Year2']<2050]
    df = df[df['Year2']>1899]
    df = df[df['Date_diff_int']<20000]
    
    df['Date_diff_int2'] = df['Date_diff_int']
    
    # convert continuous dates to categorical references
    conditions = [
        (df['Date_diff_int2'] > 0),
        (df['Date_diff_int2'] == 0)]   
    choices = ['FUTURE_REF', 'PRESENT_REF']    
    df['Date_diff_int2'] = np.select(conditions, choices, default='PAST_REF') 
    
    return df

def dataOperations_general(df,pattern_in_fname):
    
    # NOTE:
    # - this function will work if the date is in the filename
    # - if it is of form YYYYMMDD, pattern_in_fname should be "\d{8}"
    # - if it is of form YYYY_MM_DD, pattern_in_fname should be "\d{4}_\d{2}_\d{2}"
    
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
    
    indt = df.loc[:,'Year'].copy().apply(str) + "-" + [s.zfill(2) for s in df.loc[:,'Month'].copy().apply(str)] + "-" + [s.zfill(2) for s in df.loc[:,'Day'].copy().apply(str)]
    
    df.loc[:,'DatetimeSpeech64'] = [ np.datetime64(ss,'D') for ss in indt ].copy()
    
    df, df_cat = sutimeDateTreatment(df)
       
    tmp = df['Datetime64'].values.astype('datetime64[D]') - df['DatetimeSpeech64'].values.astype('datetime64[D]')
    df['Date_diff_int'] = tmp.astype(int).copy()
        
    df.loc[:,'Date_diff64_D'] = tmp.astype('timedelta64[D]').astype('int64')
    df.loc[:,'Date_diff64_M'] = df['Date_diff64_D'].astype('timedelta64[M]').astype('int64')
    df.loc[:,'Date_diff64_Y'] = df['Date_diff64_D'].astype('timedelta64[Y]').astype('int64') 
        
    ###############################
    ## ADDITIONAL CLEANING STEPS ##
    ###############################
    
    df = additionalCleaningSteps(df)
    
    df.loc[:,'sutime_type'] = "numerical"
    df_cat.loc[:,'sutime_type'] = "categorical"
    
    # merge back in categorical
    df_new = df.append(df_cat)
        
    # create unified variable and fill in na with values of categorical
    df_new.loc[:,'merged_cat'] = df_new['Date_diff_int2'].copy()
    df_new.loc[:,'merged_cat'] = df_new['merged_cat'].fillna(df_new['new_col']).copy()
        
    # sort the data
    df_new = df_new.sort_values(by=['Corpus','Year','Month','Day','Sent_Num'])
      
    return df_new

def futureDifferentiation(df_cat_in):

    df_cat_f_in = df_cat_in[df_cat_in['new_col']=='FUTURE_REF']
    
    short_list = """short\s*run|short\s*term|short\s*-\s*run|short\s*-\s*term|near\s*term|near\s*-\s*term|short\s*horizons|shorter\s*horizons|the\s*near\s*future|near\s*future"""

    med_list = """medium\s*run|medium\s*term|medium\s*-\s*run|medium\s*-\s*term"""

    long_list = """long\s*run|long\s*term|longer\s*run|longer\s*term|long\s*horizons|longer\s*horizons|long\s*-\s*run|long\s*-\s*term|longer\s*-\s*run|longer\s*-\s*term"""

    shortmed_list = """short\s*to\s*medium\s*-\s*term|short\s*to\s*medium\s*term|short\s*to\s*medium-run|short\s*to\s*medium\s*run"""

    medlong_list = """medium\s*to\s*long\s*-\s*term|medium\s*to\s*long\s*term|medium\s*to\s*long\s*-\s*run|medium\s*to\s*long\s*run"""

    # ROB: THIS IS TOO GRANULAR - I ADD SHORTMED TO SHORT, MEDLONG TO MED
    short_list = short_list + "|" + shortmed_list
    med_list = med_list + "|" + medlong_list
    
    df_cat_f_in['future_split'] = "FUT_AMBIG"
    df_cat_f_in.loc[df_cat_f_in["entry_actual"].str.contains(short_list, case = False),'future_split'] = "FUT_SHORT"
    df_cat_f_in.loc[df_cat_f_in["entry_actual"].str.contains(med_list, case = False),'future_split'] = "FUT_MED"
    df_cat_f_in.loc[df_cat_f_in["entry_actual"].str.contains(long_list, case = False),'future_split'] = "FUT_LONG"
    
    df2 = pd.get_dummies(df_cat_f_in['future_split'])
    df2['Sent_ID'] = df_cat_f_in['Sent_ID']
    df_cat_f_in = df_cat_f_in.merge(df2, left_on = 'Sent_ID', right_on = 'Sent_ID')

    df_cat_f_in['Meeting']= [x[:-2] for x in df_cat_f_in['Speech']]

    conditions = [
        (df_cat_f_in["future_split"] == 'FUT_SHORT'),
        (df_cat_f_in["future_split"] == 'FUT_SHORTMED'),
        (df_cat_f_in["future_split"] == 'FUT_MED'),
        (df_cat_f_in["future_split"] == 'FUT_MEDLONG'),
        (df_cat_f_in["future_split"] == 'FUT_AMBIG')]   
    choices = [1, 1.5, 2, 2.5, np.nan]    
    df_cat_f_in['horizon'] = np.select(conditions, choices, default=3)

    df4_out = df_cat_f_in.groupby(['Meeting']).agg({'FUT_AMBIG':'sum', 'FUT_LONG':'sum', 'FUT_MED':'sum',
                                            'FUT_SHORT':'sum', 'future_split':'count',
                                            'horizon':nanmean})

    df4_out = df4_out.reset_index().copy()

    df4_out['share_ambig'] = df4_out['FUT_AMBIG'] / df4_out['future_split']
    df4_out['share_long'] = df4_out['FUT_LONG'] / df4_out['future_split']
    df4_out['share_med'] = df4_out['FUT_MED'] / df4_out['future_split']
    df4_out['share_short'] = df4_out['FUT_SHORT'] / df4_out['future_split']
    df4_out['share_unambig'] = 1 - df4_out['share_ambig']
    
    return df4_out, df_cat_f_in

def openLine(fileofinterest,sentenceofinterest,originalspeechespath_):
    docs = open(originalspeechespath_ + fileofinterest + ".txt",'r',encoding="utf8")
    linestore = []
    for i, line in enumerate(docs):
        if i == sentenceofinterest - 1:
            linestore.append(line)
    linestore = linestore[0]
    
    return linestore

def findNth(ini_str,substr):
    
    # finding nth occurrence of substring 
    inilist = [i for i in range(0, len(ini_str)) if ini_str[i:].startswith(substr)] 
    return inilist

def referenceFinder(lookline,case,occurrence,verbose,info):
    
    ix = findNth(lookline,case) # this will always find the first instance... what if there are two?
    ix = ix[occurrence] 
    
    chk_center = lookline[max(ix-2-3,0):min(len(lookline),ix+6+3)] # ( 2001 )
    chk_left = lookline[max(ix-7-3,0):min(len(lookline),ix+6+3)] # 1998 , 2001 )
    chk_right = lookline[max(ix-1-3,0):min(len(lookline),ix+13+3)] # 2001 , 2007 )
    
    referencedum = 0
    pattern = re.compile("(\((\s+)*[1-9][0-9][0-9][0-9](\s+)*\))|(,(\s+)*[1-9][0-9][0-9][0-9](\s+)*\))|(\([1-9][0-9][0-9][0-9](\s+)*,)|(\((\s+)*[1-9][0-9][0-9][0-9](\s+)*,(\s+)*[1-9][0-9][0-9][0-9](\s+)*)|((\s+)*[1-9][0-9][0-9][0-9](\s+)*,(\s+)*[1-9][0-9][0-9][0-9](\s+)*\))")
    if pattern.search(chk_center) or pattern.search(chk_left) or pattern.search(chk_right):
        referencedum = 1   
        print("reference detected: " + info[0] + " " + info[1] + " " + lookline[max(ix-10,0):min(len(lookline),ix+10)])

    return referencedum

def referenceIsolate(fileofinterest,sentenceofinterest,entry_actual,count_series,originalspeechespath,verbose):
    
    try:
        linestore = openLine(fileofinterest,sentenceofinterest,originalspeechespath)
    except:
        print("WARNING: Fed Greenbook filenames too short - added an ad hoc correction!")
        print("affects file: " + fileofinterest)
        fileofinterest_x = fileofinterest[1:len(fileofinterest)-4] + "*.txt"
        linestore = openLine(fileofinterest,sentenceofinterest,originalspeechespath)
        
    referencedum = 0
    
    pattern = re.compile("^[1-9][0-9][0-9][0-9]$")
    
    info = [fileofinterest]
    info.append(str(sentenceofinterest))
    
    if pattern.match(entry_actual):
        #print(fileofinterest)
        #print(sentenceofinterest)
        referencedum = referenceFinder(linestore,entry_actual,count_series,verbose,info)
        
    return referencedum            

def financialTermFinder(lookline,case,occurrence,verbose,info):
    
    ix = findNth(lookline,case) # this will always find the first instance... what if there are two?
    ix = ix[occurrence] 
    
    chk_center = lookline[max(ix-1,0):min(len(lookline),ix+32)] # (2001)
    chk_center = re.sub(r"-"," ",chk_center)
    
    financialtermdum = 0
    pattern = re.compile( "overnight rate|"
                          "overnight interest rate|"
                          "overnight repo|"
                          "overnight repurchase agreements|"
                          "overnight market rate|"
                          "overnight market|"
                          "over night rate|"
                          "long run rate|"
                          "long run interest rate|"
                          "long run bond|"
                          "long run debt|"
                          "long run unemployment|"
                          "long run unemployed|"
                          "long term bond|"
                          "long term rate|"
                          "long term interest rate|"
                          "long term debt|"
                          "long term unemployment|"
                          "long term unemployed|"
                          "longer run rate|"
                          "longer run interest rate|"
                          "longer run debt|"
                          "longer run unemployment|"
                          "longer run unemployed|"
                          "longer term rate|"
                          "longer term interest rate|"
                          "longer term debt|"
                          "longer term unemployment|"
                          "longer term unemployed|"
                          "short run rate|"
                          "short run interest rate|"
                          "short term rate|"
                          "short term interest rate|"
                          "short run bond|"
                          "short term bond|"
                          "short run debt|"
                          "short term debt|"
                          "short term money market|"
                          "short term paper|"
                          "shorter run rate|"
                          "shorter run interest rate|"
                          "shorter term rate|"
                          "shorter term interest rate|"
                          "shorter run debt|"
                          "shorter term debt|"
                          "shorter run corpo|"
                          "shorter term corpo|"
                          "medium run rate|"
                          "medium term rate|"
                          "medium term interest rate|"
                          "medium run debt|"
                          "medium term debt|"
                          "long term refinancing op|"
                          "longer term refinancing op|"
                          "current account", re.IGNORECASE)
    if pattern.search(chk_center):
        financialtermdum = 1   
        print("financial term detected: " + info[0] + " " + info[1] + " " + lookline[max(ix-10,0):min(len(lookline),ix+32)])

    return financialtermdum

def financialTermIsolate(fileofinterest,sentenceofinterest,entry_actual,count_series,originalspeechespath_,verbose):
    
    linestore = openLine(fileofinterest,sentenceofinterest,originalspeechespath_)
    
    financialtermdum = 0
    
    # need to make this case insensitive
    pattern = re.compile("^overnight$|"
                         "^long run$|"
                         "^long term$|"
                         "^longer run$|"
                         "^longer term$|"
                         "^short run$|"
                         "^short term$|"
                         "^shorter run$|"
                         "^shorter term$|"
                         "^medium run$|"
                         "^medium term$|"
                         "^current$", re.IGNORECASE)
    
    # WARNING: 
    # - there used to be a "bug" here (removed 15/03/2022)
    # - because the final term is "^current$|", instead of "^current$", this "filtering" function does not work as intended
    # - it will *always* match everything that goes in, because of the final "|"
    # - however, the second stage filtering still does its job, so there is no ultimate error
    # - for legacy reasons I am keeping this code with the bug, because it changes nothing
    
    info = [fileofinterest]
    info.append(str(sentenceofinterest))
    
    if pattern.match(entry_actual):
        
        financialtermdum = financialTermFinder(linestore,entry_actual,count_series,verbose,info)
        
    return financialtermdum   

def futureDifferentiation_acrossCorpora(df_cat_in,event_string):

    df_cat_f_in = df_cat_in[df_cat_in['new_col']=='FUTURE_REF'].copy()

    short_list = """short\s*run|short\s*term|short\s*-\s*run|short\s*-\s*term|near\s*term|near\s*-\s*term|short\s*horizons|shorter\s*horizons|the\s*near\s*future|near\s*future"""

    med_list = """medium\s*run|medium\s*term|medium\s*-\s*run|medium\s*-\s*term"""

    long_list = """long\s*run|long\s*term|longer\s*run|longer\s*term|long\s*horizons|longer\s*horizons|long\s*-\s*run|long\s*-\s*term|longer\s*-\s*run|longer\s*-\s*term"""

    shortmed_list = """short\s*to\s*medium\s*-\s*term|short\s*to\s*medium\s*term|short\s*to\s*medium-run|short\s*to\s*medium\s*run"""

    medlong_list = """medium\s*to\s*long\s*-\s*term|medium\s*to\s*long\s*term|medium\s*to\s*long\s*-\s*run|medium\s*to\s*long\s*run"""

    # ROB: THIS IS TOO GRANULAR - I ADD SHORTMED TO SHORT, MEDLONG TO MED
    short_list = short_list + "|" + shortmed_list
    med_list = med_list + "|" + medlong_list
    
    df_cat_f_in['future_split'] = "FUT_AMBIG"
    df_cat_f_in.loc[df_cat_f_in["entry_actual"].str.contains(short_list, case = False),'future_split'] = "FUT_SHORT"
    df_cat_f_in.loc[df_cat_f_in["entry_actual"].str.contains(med_list, case = False),'future_split'] = "FUT_MED"
    df_cat_f_in.loc[df_cat_f_in["entry_actual"].str.contains(long_list, case = False),'future_split'] = "FUT_LONG"
    
    df2 = pd.get_dummies(df_cat_f_in['future_split'])
    df2.loc[:,'Sent_ID'] = df_cat_f_in['Sent_ID'].copy()
    df_cat_f_in = df_cat_f_in.merge(df2, left_on = 'Sent_ID', right_on = 'Sent_ID')

    conditions = [
        (df_cat_f_in["future_split"] == 'FUT_SHORT'),
        (df_cat_f_in["future_split"] == 'FUT_SHORTMED'),
        (df_cat_f_in["future_split"] == 'FUT_MED'),
        (df_cat_f_in["future_split"] == 'FUT_MEDLONG'),
        (df_cat_f_in["future_split"] == 'FUT_AMBIG')]   
    choices = [1, 1.5, 2, 2.5, np.nan]    
    df_cat_f_in.loc[:,'horizon'] = np.select(conditions, choices, default=3)
    
    return df_cat_f_in

def createContinuousMeasureSUTimeGranular(df_in,df_T,topicInfo,colStr,suffixStr,timeStr,event_string):
    
    dum_mat = pd.get_dummies(df_in[colStr])
    dum_mat.loc[:,'Sent_ID'] = df_in['Sent_ID'].copy()
    dum_mat.loc[:,'File_ID'] = df_in['File_ID'].copy()
    dum_mat.loc[:,'Sent_nr'] = df_in['Sent_nr'].copy()
    dum_mat.loc[:,event_string] = df_in[event_string].copy()
    
    dum_mat = dum_mat.rename(columns={"FUT_SHORT": "FUT_SHORT_dum", 
                                      "FUT_MED": "FUT_MED_dum", 
                                      "FUT_LONG": "FUT_LONG_dum",
                                      "FUT_AMBIG": "FUT_AMBIG_dum"})
    
    dum_mat_T = dum_mat.merge(df_T[['Sent_nr','File_ID']+topicInfo["order"]], left_on = ['Sent_nr','File_ID'], right_on = ['Sent_nr','File_ID'], how = 'left', validate = 'm:1') # 

    # future interactions
    timeStr_in = timeStr + "_dum"
    dum_mat_T_fut = dum_mat_T.loc[dum_mat_T[timeStr_in]==1,:].copy()
    dum_mat_T_int_fut = dum_mat_T_fut[topicInfo["order"]].copy()
    if timeStr == "FUT_SHORT":
        intlist = [s + '_int_fut_sht_' + suffixStr for s in topicInfo["order"]]
    if timeStr == "FUT_MED":
        intlist = [s + '_int_fut_med_' + suffixStr for s in topicInfo["order"]] 
    if timeStr == "FUT_LONG":
        intlist = [s + '_int_fut_lng_' + suffixStr for s in topicInfo["order"]]  
    if timeStr == "FUT_AMBIG":
        intlist = [s + '_int_fut_amb_' + suffixStr for s in topicInfo["order"]]  
        
    dum_mat_T_int_fut.columns = intlist
    dum_mat_T_int_fut.loc[:,event_string] = dum_mat_T_fut[event_string].copy()

    df_in_shares_fut = dum_mat_T_int_fut.groupby(event_string).mean().copy()
    df_in_shares_fut = df_in_shares_fut.reset_index().copy()   
    
    return df_in_shares_fut

def mergeIntTermsGranular(df_cat_f_in,df_T,topicInfo,event_string):
        
    df_new_shares_fut_sht_out = createContinuousMeasureSUTimeGranular(df_cat_f_in,df_T,topicInfo,'future_split','cat_grn',"FUT_SHORT",event_string)
    df_new_shares_fut_med_out = createContinuousMeasureSUTimeGranular(df_cat_f_in,df_T,topicInfo,'future_split','cat_grn',"FUT_MED",event_string)
    df_new_shares_fut_lng_out = createContinuousMeasureSUTimeGranular(df_cat_f_in,df_T,topicInfo,'future_split','cat_grn',"FUT_LONG",event_string)
    df_new_shares_fut_amb_out = createContinuousMeasureSUTimeGranular(df_cat_f_in,df_T,topicInfo,'future_split','cat_grn',"FUT_AMBIG",event_string)

    int_terms_grnlr_out = df_new_shares_fut_sht_out
    int_terms_grnlr_out = int_terms_grnlr_out.merge(df_new_shares_fut_med_out, left_on = [event_string], right_on = [event_string], how = 'outer', validate = 'm:1') 
    int_terms_grnlr_out = int_terms_grnlr_out.merge(df_new_shares_fut_lng_out, left_on = [event_string], right_on = [event_string], how = 'outer', validate = 'm:1') 
    int_terms_grnlr_out = int_terms_grnlr_out.merge(df_new_shares_fut_amb_out, left_on = [event_string], right_on = [event_string], how = 'outer', validate = 'm:1') 

    return int_terms_grnlr_out

# need to get the main effects also
def mainEffectGranular(df_cat_f_in,event_string):
    
    dum_mat = pd.get_dummies(df_cat_f_in['future_split'])
    dum_mat.loc[:,'Sent_ID'] = df_cat_f_in['Sent_ID'].copy()
    dum_mat.loc[:,event_string] = df_cat_f_in[event_string].copy()
    dum_mat.loc[:,'Sent_nr'] = df_cat_f_in['Sent_nr'].copy()

    dum_mat = dum_mat.rename(columns={"FUT_SHORT": "FUT_SHORT_dum", 
                                      "FUT_MED": "FUT_MED_dum", 
                                      "FUT_LONG": "FUT_LONG_dum",
                                      "FUT_AMBIG": "FUT_AMBIG_dum"})

    dum_mat = dum_mat.groupby([event_string]).agg({'FUT_SHORT_dum':'mean','FUT_MED_dum':'mean',
                                     'FUT_LONG_dum':'mean','FUT_AMBIG_dum':'mean'}).reset_index()
    
    dum_mat = dum_mat.rename(columns={"FUT_SHORT_dum": "me_fut_sht_cat_grn", 
                                      "FUT_MED_dum": "me_fut_med_cat_grn", 
                                      "FUT_LONG_dum": "me_fut_lng_cat_grn",
                                      "FUT_AMBIG_dum": "me_fut_amb_cat_grn"})
    
    return dum_mat
