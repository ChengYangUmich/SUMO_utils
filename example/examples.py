# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:54:32 2022

@author: 28417
"""

# importing sys
import sys
# add the path where the SUMO_utils.py locates 
sys.path.append("C:\\Users\\28417\\OneDrive - Umich\\SUMO_utils\\src")
import os
import pandas as pd 
import numpy as np
import datetime
import matplotlib as plt
# Import SUMO_utils class 
from SUMO_utils import SUMO_utils

"""
This is an example script to demonstrate how to use SUMO_utils.
 

"""
# Processing dynamic excel files 
# Specify dynamic input excel-raw  
dyn_excel = "raw_dyn.xlsx" 
# Specify the name for the cleaned-up excel file from `raw_dyn.xlsx`
new_dyn_excel = "new_dyn.xlsx"

# Initiate a SUMO_utils object 
test = SUMO_utils()
# Read the dynamic 
test.read_dynamic(dyn_excel,new_excel = new_dyn_excel)
# print sheet_names in the excel 
print(test.dynamic_sheet_names)
# print 
y = test.read_dynamic(new_dyn_excel)
# Exame the the dyn_dic 
