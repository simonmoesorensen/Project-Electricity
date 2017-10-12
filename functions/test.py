# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 20:59:13 2017

INPUT:
    
OUTPUT:
    
USAGE:
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""
#Import modules
import pandas as pd
import numpy as np

def firstn(n):
     num = 0
     while num < n:
         yield num
         num += 1

sum_of_first_n = sum(firstn(1000000))