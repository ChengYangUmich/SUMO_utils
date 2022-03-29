# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 16:47:26 2022

@author: 28417
"""

# importing sys
import sys
# add the path where the CY_sumo locates 
sys.path.append("C:\\Users\\28417\\OneDrive - Umich\\CY_SUMO\\src")
from sumoscheduler import SumoScheduler
from sumoscheduler import Duration as dur 
import os
import pandas as pd 
import numpy as np
import datetime
# Import CY_SUMO class 
from CY_SUMO import CY_SUMO, create_param_dict

"""
This is an example script to generate needed excel file from CY_SUMO object. 
Multiple dynamic simulations with a set of different combinations of inputs are run. 

"""
dynamic_inputs = {'Trial1':{'xml':'MABRplant.xml',
                            'stop_time':1*dur.day,
                            'data_comm_freq':1*dur.hour,
                            'param_dic':{'Sumo__Plant__Sideflowdivider1__param__Qpumped_target':5},
                            'input_fun':{"Sumo__Plant__Influent1__param__TKN": lambda t: 32 + (42-32)/(1+np.exp(-5*(t-0.01))),
                                         "Sumo__Plant__Influent1__param__TCOD": lambda t: 400 + 50*np.sin(20*t)},
                            'tsv_file': None}
                            ,
                  'Trial2':{'xml':'MABRplant.xml',
                            'stop_time':1*dur.day,
                            'data_comm_freq':1*dur.hour,
                            'param_dic':{'Sumo__Plant__Sideflowdivider1__param__Qpumped_target':13},
                            'input_fun':{"Sumo__Plant__Influent1__param__TKN": lambda t: 32 + (42-32)/(1+np.exp(-5*(t-0.01))),
                                         "Sumo__Plant__Influent1__param__TCOD": lambda t: 400 + 50*np.sin(20*t)},
                            'tsv_file': None}
                  }


# Get current path 
current_path = os.getcwd()
# Initiate name string of the sumo .dll core    
model = os.path.join(current_path,"MABRplant.dll")
# Create a list of sumo incode variables to track 
sumo_variables = ["Sumo__Time",
                  "Sumo__Plant__Effluent1__SNHx",
                  "Sumo__Plant__Effluent1__SNOx",
                  "Sumo__Plant__Effluent1__TCOD",  
                  "Sumo__Plant__MBBR2__XNITO"]  # MABR nitrofier biomass concentration 

# Create a CY_SUMO object 
test = CY_SUMO(model= model,
               sumo_variables=sumo_variables)
test.dynamic_run(dynamic_inputs,save_name="../raw.xlsx")