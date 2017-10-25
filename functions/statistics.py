# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 18:09:30 2017

INPUT:
    
    tvec: N x 6 matrix where each row is a time vector
    data: N x 4 matrix where each row is a set of measurements
    
OUTPUT:
    
    Screen output: a table of descriptive statistics
    
                   mean  min  25%   50%   75%    max
        Zone                                        
        1      
        2      
        3      
        4     
        All   
    
USAGE:
    
    print_statistics(tvec,data)
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

def print_statistics(tvec,data):
    
    #Define the relevant statistics
    dStats=['min','25%','50%','75%','max']
    
    #Get descriptive statistics of data, zone-wise
    statzone = data.describe().T[dStats].rename(
            index={'zone1': 1, 'zone2': 2, 'zone3': 3, 'zone4': 4})
        #The line above gets the statistics, transposes it, while only selecting 
        #the relevant statistics. Then it renames the zones to integers
    
    #Get descriptive statistics of all zones
    statall = data.sum(axis=1).describe().T[dStats].rename("All")
        #The line above does practically the same, however it is a Series and
        #has different renaming syntax
    
    #Add together
    stat = statzone.append(statall)
    
    #Assign index name
    stat.index.name = "Zone"
    
    print("\n",stat)
