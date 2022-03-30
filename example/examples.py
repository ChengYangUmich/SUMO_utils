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
import matplotlib.pyplot as plt
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

# # print names of sheets in the excel 
# print(test.dyn_sheet_names)
# #  print names of sumo variables in each sheet 
# print(test.dyn_var_list)

# Processing steady-state excel files
# Specify steady-state input excel-raw  
ss_excel = "raw_steady_state.xlsx"
# Specify the name for the cleaned-up excel file from `raw_steady_state.xlsx`
new_ss_excel = "new_steady_state.xlsx"
temp = test.read_steady_state(steady_state_excel=ss_excel, new_excel=new_ss_excel)

# ######################################################################### Quick plots  
# # The same x-y plots from each sheet and are combined into one axes - `workbook_plot()`  
# fig, axs = plt.subplots(2,1,figsize = (8,6))
# plt.rcParams['font.size'] = '14' # Set global fontsize 

# ax = axs[0]
# x_name = 'Sumo__Time'
# y_name = 'Sumo__Plant__Effluent1__SNHx'
# lines = test.workbook_plot(x_name,y_name,ax = ax) 
# # (Optional) Aesthetic editing
# ax.set_xlabel('Time')
# ax.set_ylabel('Ammonia, mg-N/L')

# ax = axs[1]
# x_name = 'Sumo__Time'
# y_name = 'Sumo__Plant__Effluent1__SNOx'
# lines = test.workbook_plot(x_name,y_name,ax = ax)
# ax.set_xlabel('Time')
# ax.set_ylabel('Nitrate, mg-N/L')

# fig.tight_layout()
# fig.savefig('.\Pics\workbookplot.jpg')

# # The doulbe-y axes plot - `sheet_plot_yyplot`
# fig, axs = plt.subplots(1,1,figsize = (8,3))
# plt.rcParams['font.size'] = '14' # Set global fontsize 
# # Specify inputs 
# ax = axs
# sheet_name = 'Trial1'
# x_name = 'Sumo__Time'
# y1_name = 'Sumo__Plant__Influent1__param__TKN'
# y2_name = 'Sumo__Plant__Effluent1__SNHx'
# # Plotting 
# L1,L2,ax_twin = test.sheet_plot_yyplot(sheet_name=sheet_name, x_name = x_name, 
#                                        y1_name = y1_name,y2_name = y2_name, 
#                                        ax = ax)
# # labels editting 
# ax.set_xlabel("Time")
# ax.set_ylabel("Influent TKN, mg-N/L", color =test.cmap1[0])
# ax_twin.set_ylabel("Effluent Ammonia, mg-N/L", color =test.cmap1[1])

# # Align ticks
# ax.grid(True)
# ax_twin.grid(True)
# ax.set_yticks(np.linspace(ax.get_ybound()[0], ax.get_ybound()[1], 6))
# ax_twin.set_yticks(np.linspace(ax_twin.get_ybound()[0], ax_twin.get_ybound()[1], 6))      
# fig.tight_layout()
# # Save figure 
# fig.savefig('.\Pics\yyplot.jpg')

# # Add a new line/scatter to the yyplot - `sheet_plot_add_line()` or `sheet_plot_add_scatter()` 
# fig, axs = plt.subplots(1,1,figsize = (8,3))
# plt.rcParams['font.size'] = '14' # Set global fontsize 
# # e.g. plot effluent nitrate to the right-y axes
# # Specify inputs 
# ax = axs
# x_name = 'Sumo__Time'
# y_name = 'Sumo__Plant__Effluent1__SNOx'
# sheet_name = 'Trial1'
# # Plot 
# test.sheet_plot_add_line(sheet_name,x_name,y_name, ax = ax, color = test.cmap1[0],label = 'Nitrate')

# # e.g. plot effluent nitrate to the right-y axes
# # Specify inputs 
# ax = axs
# x_name = 'Sumo__Time'
# y_name = 'Sumo__Plant__Effluent1__SNHx'
# sheet_name = 'Trial1'
# # Plot 
# test.sheet_plot_add_scatter(sheet_name,x_name,y_name, ax = ax, color = test.cmap1[1],label = 'Ammonia')
# ax.grid()
# ax.legend()
# ax.set_xlabel('Time')
# ax.set_ylabel('Concentrations, mg-N/L')
# fig.tight_layout()
# # Save figure 
# fig.savefig('.\Pics\LineAndScatter.jpg')


