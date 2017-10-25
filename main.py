# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 19:52:28 2017

This script does things...    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""
import pandas as pd

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
                        "Quit."])

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
                tvec,data = load_measurements(filename,fmode) #Try to load data
                
                #Save raw data in old variables
                tvecOld = tvec
                dataOld = data
                
                dataLoaded = True #Set data as loaded
                
                print("-----Data loaded succesfully-----")
                break
                
            except FileNotFoundError:
                if filename == "exit":
                    break
                
                filename = inputStr("File not found, please enter a valid name: ")

#Aggregate data
    elif menu == 2:
        #Check if data is loaded
        if not dataLoaded:
            print("\nPlease load data first")
            continue
        
        menu2 = int(displayMenu(["Consumption per minute (no aggregation)",
                            "Consumption per hour",
                            "Consumption per day",
                            "Consumption per month",
                            "Hour-of-day consumption (hourly average)"]))
        
        period = periodStr[(menu2)-1] #define period
        
        tvec,data = aggregate_measurements(tvecOld,dataOld,period) #Aggregate data, but always agg from raw data
        
        #Check if it is preferable to convert units
        if (data > 10000).any().any():
            data = data/1000
            unit = "Kilowatt-hour"
        
#Display statistics
    elif menu == 3:
        #Check if data is loaded
        if not dataLoaded:
            print("\nPlease load data first")
            continue
        
        print_statistics(tvec,data) #Show statistics
        
        print("\nConsumption per {} | Unit: {}".format(period,unit))

#Visualize data
    elif menu == 4:
        #See if user wants each zone or all zones
        print("\nPlease decide whether to plot for each or all zones \n")
        menu2 = displayMenu(["Each zone","All zones"])
        
        #Assign plot data to what the user specified
        if menu2 == 2:
            pltData = data.sum(axis=1)
        else:
            pltData = data
        
        #Define plot parameters
        figsize = (9,5.0625)
        title = "Consumption per {}".format(period)
        
        #Define x-axis
        pltX = tvec.apply(lambda x: ' '.join(x.astype(str)), axis=1)
        
        #Check type and rename index depending on this
        if isinstance(pltData,pd.DataFrame):    
            pltData = pltData.set_index([pltX])
        else:
            pltData = pltData.rename(pltX)
        
        if len(pltData) < 25:
            plot1 = pltData.plot(kind='bar',figsize=figsize,title=title)
        else:
            plot1 = pltData.plot(figsize=figsize,title=title)

        #Add options to plot
        plt.xlabel("Date") #Add x-label
        plt.xticks(rotation=45)
        plt.ylabel(unit) #Add y-label
        
        plt.show(plot1) #Display the plots
        
        #Add pie-chart
        plot2 = data.sum().rename("Sum").plot(kind='pie',
                        title="Distribution of electricity consumption",
                        figsize=(8,8),autopct='%.2f',fontsize=16) #Define pie chart
        
        plt.show(plot2) #Display

#Show data
    elif menu == 5:
        print(tvec.join(data))
        print("\nUnit: {}".format(unit))

#Quit
    elif menu == 6:
        break
            
                
                
            