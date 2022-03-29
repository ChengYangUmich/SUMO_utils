# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:21:26 2022

@author: Cheng Yang, University of Michigan
"""

import os 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

class SUMO_utils():
    """
    This is a module that contains convenient method for processing and analyzing excel file generated with CY_SUMO.
    
    Author: Cheng Yang, Unversitiy of Michigan, Ann Arbor, MI
    
    Inputs: 
    ------------------------
    (Mandatory)
    
    """
    
    def __init__(self):
        self.current_path = os.getcwd()
    
    def read_dynamic(self, dynamic_excel, new_excel = None):
        # Store name string of the dynamic file
        self.dynamic_excel = dynamic_excel
        # Create pandas excel object for internal usage  
        self.dyn_xls = pd.ExcelFile(self.dynamic_excel)
        # Collect sheet names of the excel 
        self.dynamic_sheet_names = self.dyn_xls.sheet_names
        
        # Start reading excel 
        # Create a dictionary for storage 
        self.dyn_dic = {}
        for sheetID, a_sheet in enumerate(self.dynamic_sheet_names):
            print(f"Processing Sheet  {a_sheet}--- {sheetID+1}/{len(self.dyn_xls.sheet_names)} ")
            temp_df= pd.read_excel(self.dyn_xls, sheet_name=a_sheet)
            # Drop the first column, because they are simple index 
            temp_df = temp_df.drop(columns = ['Unnamed: 0'])
            # Get the columns names of the temp_df, and convert it into a list object
            self.dyn_var_list = list(temp_df.columns)
            # Convert columns that are string into float64
            self.dyn_dic[a_sheet] = self._clean_str_var(temp_df)
        
        # Save the processed data into new_excel 
        if (new_excel != None) and (new_excel.endswith('.xlsx')):
            with pd.ExcelWriter(new_excel) as writer:
                for a_key in list(self.dyn_dic.keys()):
                    a_df = self.dyn_dic[a_key]
                    sheet_name = f"{a_key}"
                    a_df.to_excel(writer, sheet_name)
            print(f"---------{new_excel} was saved successfully--------")
        
        # Update the dyn_var_list after all processing are done
        self.dyn_var_list = list(self.dyn_dic[a_sheet].columns)
        
        return self.dyn_dic           
        
    def _clean_str_var(self,temp_df):
        clean_df = temp_df.copy()
        # Collect columns whose values are string 
        for a_str_var in self.dyn_var_list:
            # Create new columns in the clean_df
            x = clean_df[a_str_var][0]
            if isinstance(x, str):
            # Get how many layers (n_) a real array has
                _, n_ = self._convert_str_to_list(x)
                # Create new column names, e.g. 'SUMO_biofilm' into ['SUMO_biofilm_0', 'SUMO_biofilm_1', ...]  
                new_cols = [a_str_var + "_" + str(a_n_) for a_n_ in range(n_)]
                # Create columns in the clean_df
                for a_new_col in new_cols:
                    clean_df[a_new_col] = np.nan
                # Fill in values in the new columns created in clean_df by iterating over rows in the df   
                for row_id, row_value in enumerate(clean_df[a_str_var]):
                    float_array,n_ = self._convert_str_to_list(row_value)
                    for m in range(n_):
                        clean_df.loc[row_id,new_cols[m]]=float_array[m]
                clean_df = clean_df.drop(columns = a_str_var)    
        return clean_df

    def _convert_str_to_list(self, a_str):
        # RealArrays are in the form of a string e.g. '[1,2,3,4]', convert it into a list of np.float, e.g.[1,3,4,5]
        a_str = a_str.strip("[")
        a_str = a_str.strip("]")        
        a_str = a_str.split(', ')
        n = len(a_str)
        a_list = [np.float(a_var) for a_var in a_str]
        return a_list, n
        
        