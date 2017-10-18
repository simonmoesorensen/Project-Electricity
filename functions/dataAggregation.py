# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 19:00:00 2017

INPUT:
    
OUTPUT:
    
USAGE:
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""
import numpy as np

def aggregate_measurements(tvec, data, period):
    
    #Aggregate data for hourly consumption
    if period == "hour":
        
        #Aggregate data
        for i in range(max(tvec[:,3])):
            
            #Define the indicies of rows
            inRow = np.where(tvec[:,3] == i)
            
            #Aggregate data
            row = np.sum(data[inRow,:],axis=1)
    
    return (tvec_a, data_a)