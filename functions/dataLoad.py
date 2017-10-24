# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:05:23 2017

INPUT:
    
    filename: String, the full name of the datafile
    fmode: String, specifying how to handle corrupted measurements.
        Can be:
            "forward fill"
            "backward fill"
            "drop"
    
OUTPUT:
    
    tvec: N x 6 matrix where each row is a time vector
    data: N x 4 matrix where each row is a set of measurements
    
USAGE:
    
    tvec,data = load_measurements(filename,fmode)
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

import pandas as pd
import numpy as np

#Function
def load_measurements(filename, fmode):
    
    #Initial variables
    warning = False
    corr = []
    fmodeStr = ["forward fill","backward fill","drop"]
    
    #Ignore cases
    fmode = fmode.lower()
    
    #Load the datafile into DataFrame (variable name: df)
    df = pd.read_csv(filename,header=None,
        names=["year", "month", "day", "hour", "minute", "second", "zone1", "zone2", "zone3", "zone4"])
    
    #Define the measurement columns and create an np array
    m = np.array(df.iloc[:,6:10])
    
    #Find rows where -1 is present
    corr = np.unique(np.where(-1 == m)[0])
    
    #Check if first or last row is corrupted and compare to errorhandling mode
    
    if fmode in fmodeStr[0:2]:
        #Check if first row is corrupted
        if 0 in corr and (fmode in fmodeStr[0]):
            #Change to drop mode
            fmodeold = fmode
            fmode = "drop"
            #Print warning
            warning = True
        
        #Check if last row is corrupted
        if len(df)-1 in corr and (fmode in fmodeStr[1]):
            #Change to drop mode
            fmodeold = fmode
            fmode = "drop"
            #Print warning
            warning = True
        
    #Replace -1 with NaN values if 
    if fmode in fmodeStr[0:2]:
        df = df.replace(-1,np.NaN)
    
    if fmode == "forward fill":
        #Use pandas forward fill
        df = df.ffill()
    
    elif fmode == "backward fill":
        #Use pandas backfill
        df = df.bfill()
    
    if fmode == "drop":
        #Delete corrupted rows
        df = df.drop(corr)
   
    #Print warning
    if warning:
        print("""
!WARNING!
{} error 
deleting corrupted lines at: {}""".format(fmodeold,corr+1))
        
    #Define data and tvec as a pandas dataFrame     
    data = df.iloc[:,6:10]
    
    tvec = df.iloc[:,0:6]
        
    return tvec,data
        