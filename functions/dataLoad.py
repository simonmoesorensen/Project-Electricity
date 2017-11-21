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
    fmodeStr = ["forward fill","backward fill","drop"]

    #Load the datafile into DataFrame (variable name: df)
    df = pd.read_csv(filename,header=None,
        names=["year", "month", "day", "hour", "minute", "second", "zone1", "zone2", "zone3", "zone4"])

    #Replace -1 with NaN values
    df = df.replace(-1,np.NaN)

    #Check if first or last row is corrupted and compare to errorhandling mode
    #if special case is found, change to drop mode and print warning
    if df.iloc[0,:].isnull().any() and fmode in fmodeStr[0]:
        #Change to drop mode
        fmodeold = fmode
        fmode = "drop"
        #Print warning
        warning = True

    elif df.iloc[len(df)-1,:].isnull().any() and fmode in fmodeStr[1]:
        #Change to drop mode
        fmodeold = fmode
        fmode = "drop"
        #Print warning
        warning = True

    #Do errorhandling
    if fmode == "forward fill":
        #Use pandas forward fill
        df = df.ffill()

    elif fmode == "backward fill":
        #Use pandas backfill
        df = df.bfill()

    elif fmode == "drop":
        #Use pandas drop missing values
        df = df.dropna()

    #Print warning
    if warning:
        print("""
!WARNING!
{} error
dropping all corrupted rows""".format(fmodeold))

    #Define data and tvec as a pandas dataFrame
    data = df.iloc[:,6:10]

    tvec = df.iloc[:,0:6]

    return tvec,data
