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
    
    #Iterate over the corrupted rows and do errorhandling depending on the userinput
    for i in range(len(corr)):
        
        #Forward fill
        if fmode in fmodeStr[0]:
           
            #Run loop to go backwards until a valid row is found
            for j in range(len(df[0:corr[i]])):
                
                #Define last row
                lastRow = np.array(df.iloc[corr[i]-(j+1),:], dtype=object)
                    
                #Replace row with former valid row
                if -1 not in lastRow:
                    df.iloc[corr[i],:] = df.iloc[corr[i]-(j+1),:]
                    break

                #End of for j loop
       
        #Backward fill
        elif fmode in fmodeStr[1]:
            
            #Run loop to go forwards until a row until a valid row is found
            for j in range(len(df[corr[i]:])):
                
                #Define next row
                nextRow = np.array(df.iloc[corr[i]+(j+1),:], dtype=object)
   
                #Replace row with next valid row
                if -1 not in nextRow:
                    df.iloc[corr[i],:] = df.iloc[corr[i]+(j+1),:]
                    break
                
        if fmode in fmodeStr[2]:
            #Delete corrupted rows
            
            df = df.drop(corr[i])
        
        #End of for i loop
        
    #Print warning
    if warning:
        print("""
!WARNING!
{} error 
deleting corrupted lines at: {}""".format(fmodeold,corr+1))
    
    #Define data and tvec        
    data = np.array(df.iloc[:,6:10])
    
    tvec = np.array(df.iloc[:,0:6], dtype=object)
            
    return tvec,data
            