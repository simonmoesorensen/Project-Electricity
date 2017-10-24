# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 19:00:00 2017

INPUT:
    
OUTPUT:
    
USAGE:
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

def aggregate_measurements(tvec, data, period):
    
    #Ignore cases
    period = period.lower()
    
    #Join tvec and data
    df = tvec.join(data)
    
    #Aggregate data for hourly consumption
    if period == "hour":
        
        #Group by hours
        df_g = df.groupby(['year','month','day','hour'])
                   
        #Get the dataframe of aggregated data
        df_a = df_g['zone1','zone2','zone3','zone4'].sum()
    
    elif period == "day":
        
        #Group by days
        df_g = df.groupby(['year','month','day'])
                   
        #Get the dataframe of aggregated data
        df_a = df_g['zone1','zone2','zone3','zone4'].sum()
    
    elif period == "month":
        
        #Group by days
        df_g = df.groupby(['year','month'])
                   
        #Get the dataframe of aggregated data
        df_a = df_g['zone1','zone2','zone3','zone4'].sum()
        
    elif period == "hour of the day":
        
        #Group by hour of the day
        df_g = df.groupby(['hour'])
                   
        #Get the dataframe of aggregated data
        df_a = df_g['zone1','zone2','zone3','zone4'].sum()
    
    #Define data and tvec seperately
    data_a = df_a.iloc[:,6:10]
    
    tvec_a = df_a.iloc[:,0:6]
        
    return tvec_a, data_a

tvec_a, data_a = aggregate_measurements(tvec,data,"hour of the day")