# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 19:52:28 2017

This script does things...

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

#Modules
import pandas as pd
import time
import numpy as np

#Import functions
from functions.userinput import displayMenu,inputStr
from functions.dataLoad import load_measurements
from functions.dataAggregation import aggregate_measurements
from functions.statistics import print_statistics


#Import plots and make them look pretty
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')



#Initial variables
dataLoaded = False
fmodeStr = ["forward fill","backward fill","drop"]
period = "minute"
periodStr = ["minute","hour","day","month","hour of the day"]
unit = "Watt-hour"
AggData = 1

print("""
=======================================================================
Welcome to the "Analysis of household electricity consumption"-program
This program can analyse your consumption of electricity in your house!
=======================================================================""")

while True:

    print("")
    #Initial menu
    menu = displayMenu(["Load data",
                        "Aggregate data",
                        "Display statistics",
                        "Visualize electricity consumption",
                        "Show data",
                        "Quit"])

#Load data
    if menu == 1:
        print("")

        #Display a selection of fmodes
        menu2 = int(displayMenu(["Fill forward (replace corrupt measurement with latest valid measurement)",
                             "Fill backward (replace corrupt measurement with next valid measurement)",
                             "Delete corrupt measurements",
                             "Exit"]))
        if menu2 == 4:
            continue

        #Define fmode
        fmode = fmodeStr[(menu2)-1]

        print("""\nType "exit" to exit""")

        #Get filename
        filename = inputStr("Please enter the name of your datafile (with extension, if any): ")

        #Check for valid filename and exit condition
        while True:
            try:
                start = time.time() #Time
                tvec,data = load_measurements(filename,fmode) #Try to load data
                #Save raw data in old variables
                tvecOld = tvec
                dataOld = data

                dataLoaded = True #Set data as loaded
                end = time.time() #Time
                print("Time spent loading data:",round(end-start,4),"seconds")
                print("-----Data loaded succesfully-----")
                break

            except FileNotFoundError:
                if filename == "exit":
                    break

                filename = inputStr("File not found, please enter a valid name: ")
        
        
        
#Aggregate data
    elif menu == 2 and dataLoaded:
        start = time.time()        
        menu = int(displayMenu(["Consumption per minute (no aggregation)",
                            "Consumption per hour",
                            "Consumption per day",
                            "Consumption per month",
                            "Hour-of-day consumption (hourly average)",
                            "Back"]))
        if menu == 6: #Go back
            continue
        
        #Prevent AggData to be defined as 6 by checking menu first
        AggData = menu
        
        period = periodStr[(AggData)-1] #define period

        tvec,data = aggregate_measurements(tvecOld,dataOld,period) #Aggregate data, but always agg from raw data

        #Check if it is preferable to convert units
        if (data > 10000).any().any():
            data = data/1000
            unit = "Kilowatt-hour"
        
        end = time.time()
        print("Time spent aggregating data:",round(end-start,4),"seconds")

#Display statistics
    elif menu == 3 and dataLoaded:

        print_statistics(tvec,data) #Show statistics

        print("\nConsumption per {} | Unit: {}".format(period,unit))

#Visualize data
    elif menu == 4 and dataLoaded:
        start = time.time()
        #See if user wants each zone or all zones
        print("\nPlease decide whether to plot for each or all zones \n")
        menu2 = displayMenu(["Each zone","All zones","Back"])
        
        if menu2 == 3: #Go back if user decides to
            continue
        
        #Assign plot data to what the user specified
        if AggData == 1:
            print("""\n====================================!!WARNING!!====================================
You are about to generate plots of a very large amount of data.
It is recommended to at least aggregate the data for an hourly consumption
before generating a plot, since the loading time could take several minutes.
====================================!!WARNING!!====================================\n""")
            WarnMenu = displayMenu(["Yes","No"])
            
            #Skip code if user regrets
            if WarnMenu == 2:
                continue
            else:
                print("\nYou might as well go finish your bachelor's degree. It will be done loading at that time\n")
        
        #Define the plotting data
        if menu2 == 2:
            pltData = data.sum(axis=1)
        elif menu2 == 1:
            pltData = data

        #Define plot parameters
        figsize = (9,5.0625)
        title = "Consumption per {}".format(period)

        #Define x-axis and delete 0's
        if AggData != 5:
            pltX = tvec.apply(lambda x: ' '.join(x.astype(str)), axis=1)
            
            xAxis = [] #Placeholder
        
            for i in range(len(pltX)):
                row = np.array(pltX[i].split(" ")) #Create row of strings in np array
                mask = np.arange(len(row)-AggData,len(row)) #Create array of indicies to delete
                row = np.delete(row,mask) #Delete 0 values
                rowStr = " ".join(row) #Join row
                xAxis.append(rowStr) #Append to axis variable
            
            xLabel = "Date"
                
        else:
            xAxis = tvec
            xLabel = "Hour of the day"

        #Check type and rename index depending on this
        if isinstance(pltData,pd.DataFrame):
            pltData = pltData.set_index([xAxis])
        else:
            pltData = pltData.rename(xAxis)

        if len(pltData) < 25:
            plot1 = pltData.plot(kind='bar',figsize=figsize,title=title)
        else:
            plot1 = pltData.plot(figsize=figsize,title=title)

        #Add options to plot
        plt.xlabel(xLabel) #Add x-label
        plt.xticks(rotation=45)
        plt.ylabel(unit) #Add y-label

        plt.show(plot1) #Display the plots

        #Add pie-chart
        plot2 = data.sum().rename("").plot(kind='pie',
                        title="Distribution of electricity consumption",
                        figsize=(8,8),autopct='%.2f%%',fontsize=16) #Define pie chart

        plt.show(plot2) #Display
        end = time.time()
        print("Time spent generating plots:",round(end-start,4),"seconds")

#Show data
    elif menu == 5 and dataLoaded:
        print(tvec.join(data))
        print("\nUnit: {}".format(unit))

#Quit
    elif menu == 6:
        break

#No data loaded
    else:
        print("ERROR! No data loaded. Please load data.")
