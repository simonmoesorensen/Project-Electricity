# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 19:00:00 2017

INPUT:
    
    tvec: N x 6 matrix where each row is a time vector
    data: N x 4 matrix where each row is a set of measurements
    period: A string being one of the following
        - "month"
        - "day"
        - "hour"
        - "hour of the day"
        - "minute"
    
OUTPUT:

    tvec_a: M x 6 matrix where each row is a time vector
    data_a: M x 4 matrix where each row is a set of aggregated measurements
    
USAGE:
    
    tvec_a, data_a = aggregate_measurements(tvec,data,period)
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

import numpy as np

def aggregate_measurements(tvec, data, period):
    
    #Ignore cases
    period = period.lower()
    
    #Join tvec and data
    df = tvec.join(data)
    
    #Initial variable
    stack = np.full([1,6],-1)
    
    #Aggregate data for hourly consumption
    if period == "hour":
        
        #Group by hours
        df_g = df.groupby(['year','month','day','hour'])

    elif period == "day":
        
        #Group by days
        df_g = df.groupby(['year','month','day'])
    
    elif period == "month":
        
        #Group by days
        df_g = df.groupby(['year','month'])
        
    elif period == "hour of the day":
        
        #Group by hour of the day
        df_g = df.groupby(['hour'])
                   
    #Get the dataFrame of aggregated data
    agg = df_g['zone1','zone2','zone3','zone4'].sum()
    
    #Get time vectors
    if period != "hour of the day":   
        for row in range(len(agg)):
            #Define row as an array
            row = np.array(agg.iloc[row].name)
            
            #Add the missing collumns for time
            miss = np.full([6-np.size(row)],0)
            
            #Append so we get the same size array of time and stack
            time = np.append(row,miss)
            
            #Stack time and 'stack' 
            stack = np.vstack((stack,time))
        

        #Remove placeholder from stack
        stack = np.delete(stack,0,axis=0)
    
        #Joining together time vectors and data in dataFrame_final
        df_f = np.array(np.hstack([stack,np.array(agg)]),dtype=object)
    
        #Define data_a and tvec_a seperately
        data_a = df_f[:,6:10]
        
        tvec_a = df_f[:,0:6]
    
    else:
        #Define time as the intervals 00:00 - 01:00
        time = np.arange(0,24).reshape(24,1)
        
        #Join together the time vector and data vector
        df_f = np.array(np.hstack([time,np.array(agg)]),dtype=object)
        
        #Define data_a and tvec_a seperately
        data_a = df_f[:,1:5]
        tvec_a = df_f[:,0]
    
    #Check if period is minute and do no aggregation
    if period == "minute":
        data_a = data
        tvec_a = tvec
        
    return tvec_a, data_a
