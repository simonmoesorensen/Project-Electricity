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

def displayMenu(options):
    """

    INPUT:
        options: An array of strings

    OUTPUT:
        menu: an integer of the user's choice

    USAGE:
        menu = displayMenu(options)
    """

    #Print menu
    for i in range(len(options)):
        print("{}. {}".format(i+1,options[i]))

    #Initial variable
    choice = 0

    #Get menu choice
    while not choice in np.arange(1,len(options)+1):
        choice = inputNumber("Please choose a menu item: ")
        if choice > len(options) or choice <= 0:
            print("\nChoice out of menu range")

    return choice

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
