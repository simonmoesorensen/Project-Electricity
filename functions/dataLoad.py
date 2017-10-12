# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:11:49 2017

INPUT:
    
    filename: String, the full name of the datafile
    fmode: String, specifying how to handle corrupted measurements.
        Can be:
            "forward fill" - Replace corrupted row with former valid row
            "backward fill" - Replace corrupted row with next valid row
            "drop" - Delete corrupted row
    
OUTPUT:
    
    tvec: N x 6 matrix where each row is a time vector
    data: N x 4 matrix where each row is a set of measurements
    
USAGE:
    
    tvec,data = load_measurements(filename,fmode)
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

#Import modules
import pandas as pd
import numpy as np

#Function
def load_measurements(filename, fmode):
    
    #Initial variables
    corrLine = []
    corrRow = []
    fmodeStr = ["forward fill","backward fill","drop"]
    dropAll = False
    
    #Load the datafile into DataFrame
    dataFrame = pd.read_csv(filename,header=None,
        names=["year", "month", "day", "hour", "minute", "second", "zone1", "zone2", "zone3", "zone4"])
    
    #Save dataFrame variable
    dataFrameBac = dataFrame

        
    #Check rows for corrupted measurements
    for i in range(len(dataFrame)+1):
            
        #Define the row
        try:    
            row = np.array(dataFrame.iloc[i,:], dtype=object)
        except IndexError:
            continue

        #If condition to check if there are corrupted measurements
        if not -1 in row:
            continue
        
        #Add row as corrupted
        corrRow.append(i)
        
        #Add line as corrupted (for print)
        corrLine.append(i+1)
        
        #Check fmode, ignore upper- or lowercase
        #foward fill
        if fmode.lower() in fmodeStr[0]:
        
            #Run loop to go back a row until a valid row is found
            for j in range(len(dataFrame[0:i])):
                
                #Define the last row
                try:
                    lastRow = np.array(dataFrame.iloc[i-(j+1),:], dtype=object)
                
                #If it is the first row, set condition to delete all corrupted
                #measurements
                except IndexError:
                    #Drop all corrupted measurements instead
                    dropAll = True
                    break
                    
                    
                #Replace row with former valid row
                if -1 not in lastRow:
                    dataFrame.iloc[i,:] = dataFrame.iloc[i-(j+1),:]
                    break

            #End of for j loop
        
        #backward fill
        elif fmode.lower() in fmodeStr[1]:
            
            #Run loop to go forward a row until a valid row is found
            for j in range(len(dataFrame[i:])):
            
                #Check if last row is corrupted
                if -1 in np.array(dataFrame.iloc[(len(dataFrame)-1):]):
                    #Drop all corrupted measurements instead
                    dropAll = True
                    break    
                
                #Define next row
                nextRow = np.array(dataFrame.iloc[i+(j+1),:], dtype=object)
   
                #Replace row with next valid row
                if -1 not in nextRow:
                    dataFrame.iloc[i,:] = dataFrame.iloc[i+(j+1),:]
                    break

            #End of for j loop
            
    #End of for i loop
            
    #Define tvec and data variables, but check if we should drop all corrupted first
    if dropAll:
        dataFrame = dataFrameBac.drop(corrRow)
        
        print("""
!WARNING!
{} error 
deleting corrupted lines at: {}""".format(fmode,corrLine))
        
    if fmode.lower() in fmodeStr[2]:
        dataFrame = dataFrame.drop(corrRow)
        
    data = np.array(dataFrame.iloc[:,6:10])
    
    tvec = np.array(dataFrame.iloc[:,0:6], dtype=object)
    
    return (tvec,data)