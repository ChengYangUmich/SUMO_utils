# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:36:22 2022

@author: 28417
"""
# importing sys
import sys
# add the path where the CY_sumo locates 
sys.path.append("C:\\Users\\28417\\OneDrive - Umich\\CY_SUMO\\src")
from CY_SUMO import CY_SUMO, create_param_dict
# add the path where the SUMO_utils.py locates 
sys.path.append("C:\\Users\\28417\\OneDrive - Umich\\SUMO_utils\\src")
from SUMO_utils import SUMO_utils
import os
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Packages needed for Global Sensitivity Analysis
from SALib.sample import saltelli
from SALib.analyze import sobol

# Define the model inputs and their bounds
SA_inputs = {
    'num_vars': 3,
    'names': ['Sumo__Plant__CSTR3__param__DOSP', 
              'Sumo__Plant__CSTR4__param__DOSP', 
              'Sumo__Plant__CSTR5__param__DOSP'],  # The DO setpoints for three tanks 
    'bounds': [[0, 4],
                [0, 4],
                [0, 4]]
}

# Generate samples
param_values = saltelli.sample(SA_inputs, 128, calc_second_order=False)

# Visualize how samples are collected 
ax = plt.axes(projection='3d')
ax.scatter3D(param_values[:,0], param_values[:,1], param_values[:,2], 'blue')
plt.savefig('..\Pics\SA_inputs.jpg')

# Create steady-state input dictionary 
param_dict = {}
for i in range(len(param_values)):
    temp_dict = {}
    for j, a_var in enumerate(SA_inputs['names']):
        temp_dict[a_var] = param_values[i,j] 
    param_dict[f'Trial{i+1}'] = temp_dict

# Run model
# Get current path 
current_path = os.getcwd()
# Initiate name string of the sumo .dll core    
model = os.path.join(current_path,"AOplant.dll")
# Create a list of sumo incode variables to track 
sumo_variables = ["Sumo__Plant__Effluent1__SNHx"]
# Create a CY_SUMO object 
test = CY_SUMO(model= model,sumo_variables=sumo_variables,param_dic=param_dict)
test.steady_state(save_table = True, 
                  save_name = "SA_result.xlsx", 
                  save_xml = False)

# Extract the simulation reuslts 
Y = np.array(test.SS_table["Sumo__Plant__Effluent1__SNHx"])
# # Perform analysis
Si = sobol.analyze(SA_inputs, Y, calc_second_order=False)

# Print the first-order sensitivity indices
print(Si)





fig, axs = plt.subplots(1,2,figsize= (8,4))
T = Si.plot(ax=axs)
for an_ax in T:
    an_ax.set_xlabel('DO setpoints')
    an_ax.set_ylabel('Sensitivity Index')
    an_ax.set_xticklabels(['Tank3','Tank4','Tank5'])
fig.tight_layout()
fig.savefig('..\Pics\SobolIndex.jpg')

fig, axs = plt.subplots(1,3,figsize= (8,3))
for i,an_ax in enumerate(axs):
    an_ax.scatter(param_values[:,i],Y)
    an_ax.set_xlabel('DO setpoints, mg/L')
    an_ax.set_ylabel('Effluent ammonia, mg-N/L')
    an_ax.set_title(f'Tank {i+3}')
fig.tight_layout()
fig.savefig('..\Pics\AOplantScatter.jpg')
