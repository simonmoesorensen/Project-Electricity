# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 03:58:30 2017

This file contains multiple functions that contribute to userinput

@author: Simon Moe Sørensen, moe.simon@gmail.com
"""
import numpy as np

def inputStr(prompt):
    """
    Userinput that only allows strings

    INPUT:
        prompt: String

    OUTPUT:
        str: The inputted string

    USAGE:
        inputStr("Please enter a string: ")

    """
    while True:
        try:
            str = input(prompt)
            break
        except ValueError:
            print("Not a valid string. Please try again")
    return str

def inputNumber(prompt):
    """
    Userinput that only allows any number and converts them to float values

    INPUT:
        prompt: any number

    OUTPUT:
        num = Float

    USAGE:
        inputStr("Please enter a number: ")
    """
    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            print("Not valid number. Please try again")
    return num

def displayMenu(options):
    """
    DISPLAYMENU Displays a menu of options, ask the user to choose an item
    and returns the number of the menu item chosen.

    Usage: choice = displayMenu(options)

    Input options Menu options (array of strings)
    Output choice Chosen option (integer)


    Author: Mikkel N. Schmidt, mnsc@dtu.dk, 2015
    """

    # Display menu options
    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))

    # Get a valid menu choice
    choice = 0

    while not(np.any(choice == np.arange(len(options))+1)):
       choice = inputNumber("Please choose a menu item: ")

    return choice
