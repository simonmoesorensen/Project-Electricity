# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 17:04:20 2017

A setup script that creates an .exe file of the project inside the "build" folder

USAGE:
    From terminal or cmd, write:
        python setup.py bdist_msi <- for windows installer
        python setup.py bdist_mac <- for mac installer (only works if run from on mac os)

@author: Simon Moe Sørensen, moe.simon@gmail.com
"""

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_mods = ['numpy.core._methods', 'numpy.lib.format', 
                   'matplotlib.backends.backend_qt5agg']

packages = ["functions","numpy","matplotlib.pyplot","matplotlib","pandas"]

build_exe_options = {"packages": packages, "excludes": ["tkinter"], 
                     "includes":additional_mods}



base = None

setup(  name = "Analysis of household electricity consumption",
        version = "1.0",
        author = "Simon Moe Sørensen",
        description = "This program analyses data of a household's electricity consumption",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
