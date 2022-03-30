# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:21:26 2022

@author: Cheng Yang, University of Michigan
"""

import os 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib

class SUMO_utils():
    """
    This is a module that contains convenient methods for processing and analyzing excel file generated with CY_SUMO.
    
    Author: Cheng Yang, Unversitiy of Michigan, Ann Arbor, MI
    
    
    
    
    Attributes: - Only important attributes are listed, attributes not mentioned 
                  here are for internal use.
    --------------
        `cmap1`: color map No. 1
    
    
    
    Methods: - Only important methods are listed, methods not mentioned 
                  here are for internal use.
    --------------
        `ready_dynamic()`: read and clean up CY_SUMO generated excel files
    """
    
    def __init__(self):
        self.cmap1 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', 
                      '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def read_dynamic(self, dynamic_excel, new_excel = None):
        """
        This is a method to read dynamic output excels from CY_SUMO().

        Parameters
        ----------
        dynamic_excel : STRING
            The name of the raw dynamic simulation output excel from CY_SUMO()， e.g. 'raw_dyn.xlsx' 
        new_excel : STRING, optional
            The name of the raw dynamic simulation output excel from CY_SUMO()， e.g. 'new_dyn.xlsx' . The default is None.

        Returns
        -------
        DICTIONARY
            A nested dictionary contains all information about dyanmic simulations after cleanup.
             - keys: sheet_names in `dynamic_excel`
             - values: pd.DataFrame, columns are sumo_variables, rows are values at different time stamps 

        """
        # Store name string of the dynamic file
        self.dynamic_excel = dynamic_excel
        # Create pandas excel object for internal usage  
        self.dyn_xls = pd.ExcelFile(self.dynamic_excel)
        # Collect sheet names of the excel 
        self.dyn_sheet_names = self.dyn_xls.sheet_names
        
        # Start reading excel 
        # Create a dictionary for storage 
        self.dyn_dic = {}
        for sheetID, a_sheet in enumerate(self.dyn_sheet_names):
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
    
    def read_steady_state(self, steady_state_excel, new_excel = None):
        """
        This is a method to read steady-state output excels from CY_SUMO().

        Parameters
        ----------
        steady_state_excel : STRING
            The name of the raw steady-state simulation output excel from CY_SUMO()， e.g. 'raw_steady_state.xlsx' 
        new_excel : STRING, optional
            The name of the raw dynamic simulation output excel from CY_SUMO()， e.g. 'new_steady_state.xlsx'  . The default is None.

        Returns
        -------
        self.ss_df
        pd.DataFrame
            A dataframe contains all information about steady-state simulations after clean-up.
             

        """
        # Store name string of the steady-state excel file
        self.ss_excel = steady_state_excel
        # Create pandas excel object for internal usage  
        self.ss_xls = pd.ExcelFile(self.ss_excel)
        # Collect sheet names of the excel 
        
        self.ss_df= pd.read_excel(self.ss_xls)
        # drop the column of 'SS_cmd'
        self.ss_df = self.ss_df.drop(columns = ['Unnamed: 0','SS_cmd'])
        self.ss_df = self._clean_str_var(self.ss_df)
        
        # Get the columns names of the temp_df, and convert it into a list object
        self.ss_var_list = list(self.ss_df.columns)

        
        # Save the processed data into new_excel 
        if (new_excel != None) and (new_excel.endswith('.xlsx')):
            self.ss_df.to_excel(new_excel)
            print(f"---------{new_excel} was saved successfully--------")
            
        return self.ss_df
        # # Start reading excel 
        # # Create a dictionary for storage 
        # self.dyn_dic = {}
        # for sheetID, a_sheet in enumerate(self.dyn_sheet_names):
        #     print(f"Processing Sheet  {a_sheet}--- {sheetID+1}/{len(self.dyn_xls.sheet_names)} ")
        #     temp_df= pd.read_excel(self.dyn_xls, sheet_name=a_sheet)
        #     # Drop the first column, because they are simple index 
        #     temp_df = temp_df.drop(columns = ['Unnamed: 0'])
        #     # Get the columns names of the temp_df, and convert it into a list object
        #     self.dyn_var_list = list(temp_df.columns)
        #     # Convert columns that are string into float64
        #     self.dyn_dic[a_sheet] = self._clean_str_var(temp_df)
        
        # # Save the processed data into new_excel 
        # if (new_excel != None) and (new_excel.endswith('.xlsx')):
        #     with pd.ExcelWriter(new_excel) as writer:
        #         for a_key in list(self.dyn_dic.keys()):
        #             a_df = self.dyn_dic[a_key]
        #             sheet_name = f"{a_key}"
        #             a_df.to_excel(writer, sheet_name)
        #     print(f"---------{new_excel} was saved successfully--------")
        
        # # Update the dyn_var_list after all processing are done
        # self.dyn_var_list = list(self.dyn_dic[a_sheet].columns)
        
        # return self.dyn_dic               
    
    def _clean_str_var(self,temp_df):
        """
        This is a internal function to format data structure in the dictionary `temp_df`.
        Specifically, in the `temp_df`, some columns are in string format. e.g. '[1,2,3,4]', which come from SUMO.xml-RealArray.
        Through this function, numbers in the RealArray are extracted and converted into np.float and form into a new columns.

        Parameters
        ----------
        temp_df : pd.dataFrame
            comes from each sheet in the CY_SUMO dynamic output excel 

        Returns
        -------
        clean_df : pd.dataFrame
            a clean pd.dataFrame which contains no string columns

        """
        clean_df = temp_df.copy()
        # Collect columns whose values are string 
        for a_str_var in list(clean_df.columns):
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
        
        """
        RealArrays are in the form of a string e.g. '[1,2,3,4]'. This method converts it into a list of np.float, e.g.[1,2,3,4]
        
        Parameters
        ----------
        a_str : STRING
            A string of a RealArray, e.g. '[0,1,2,3]'

        Returns
        -------
        a_list : LIST, 
            A list of np.float, e.g. [0,1,2,3]
        n : INT
            The number of elements in the lsit  

        """
        a_str = a_str.strip("[")
        a_str = a_str.strip("]")        
        a_str = a_str.split(', ')
        n = len(a_str)
        a_list = [np.float(a_var) for a_var in a_str]
        return a_list, n
        
    # Quickplots - overlaying results from different sheets 
    def workbook_plot(self, x_name,y_name, ax = None, **kwargs):
        """
        This is a method to traverse through all sheets, extract the same x,y variables, and plot them together on one Axis.  

        Parameters
        ----------
        x_name : STRING
            Could be query from `self.dyn_var_lsit`.
        y_name : STRING
            Could be query from `self.dyn_var_lsit`.
        ax : matplot,pyplot.axes, optional
            The axis in which lines are drawn. The default is None.If unspecified, it will use the current axis.
        **kwargs : 
            Other arguments as same in matplotlib.pyplot.plot() 

        Returns
        -------
        line_list : LIST
            a list of the plotted lines objects
            
        """
        
        if ax == None:
            ax = plt.gca()
        line_list = []
        for a_sheet in self.dyn_sheet_names:
            x = self.dyn_dic[a_sheet][x_name]
            y = self.dyn_dic[a_sheet][y_name]
            line_list.append(ax.plot(x,y,label = a_sheet,**kwargs))
        ax.grid(True)
        ax.legend()
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        return line_list
    
    # Quickplots - plots for one sheets 
    def sheet_plot_yyplot(self,sheet_name,x_name,y1_name,y2_name, ax,**kwargs):
        """
        This is a method that focuses on one sheet and generates double y axes plot.
        
        Parameters
        ----------
        sheet_name : STRING
            Could be query from `self.dyn_sheet_names`.
        x_name : STRING
            Could be query from `self.dyn_var_lsit`.
        y1_name : STRING
            Could be query from `self.dyn_var_lsit`.
        y2_name : STRING
            Could be query from `self.dyn_var_lsit`.
        ax : matplot,pyplot.axes, optional
            The axis in which lines are drawn. The default is None.If unspecified, it will use the current axis.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        line1: the left-y axis line 
        line2: the right-y axis line
        ax2: the axis generated that shared the same x-axis with the input `ax`. 

        """
        x = self.dyn_dic[sheet_name][x_name]
        y1 = self.dyn_dic[sheet_name][y1_name]
        y2 = self.dyn_dic[sheet_name][y2_name]
        
        ax2 = ax.twinx()
        line1 = ax.plot(x,y1,color = self.cmap1[0],**kwargs)
        line2 = ax2.plot(x,y2,self.cmap1[1], **kwargs)
        
        # Set ticks color 
        ax.tick_params(axis='y', colors=self.cmap1[0])
        ax2.tick_params(axis='y', colors=self.cmap1[1])
        return line1, line2, ax2
    
    def sheet_plot_add_line(self,sheet_name,x_name,y_name, ax = None,**kwargs):
        if ax == None:
            ax = plt.gca()
        x = self.dyn_dic[sheet_name][x_name]
        y = self.dyn_dic[sheet_name][y_name]
        line = ax.plot(x,y,**kwargs)
        return line
    
    def sheet_plot_add_scatter(self,sheet_name,x_name,y_name, ax = None,**kwargs):
        if ax == None:
            ax = plt.gca()
        x = self.dyn_dic[sheet_name][x_name]
        y = self.dyn_dic[sheet_name][y_name]
        line = ax.scatter(x,y,**kwargs)
        return line
    
    def heatmap(self, data, row_labels, col_labels, ax,
            cbar_kw={}, cbarlabel="", **kwargs):
        """
        Create a heatmap from a numpy array and two lists of labels.
    
        Parameters
        ----------
        data
            A 2D numpy array of shape (N, M).
        row_labels
            A list or array of length N with the labels for the rows.
        col_labels
            A list or array of length M with the labels for the columns.
        ax
            A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
            not provided, use current axes or create a new one.  Optional.
        cbar_kw
            A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
        cbarlabel
            The label for the colorbar.  Optional.
        **kwargs
            All other arguments are forwarded to `imshow`.
        """

    
        # Plot the heatmap
        im = ax.imshow(data, **kwargs)
    
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    
        # We want to show all ticks...
        ax.set_xticks(np.arange(data.shape[1]))
        ax.set_yticks(np.arange(data.shape[0]))
        # ... and label them with the respective list entries.
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)
    
        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=True, bottom=False,
                       labeltop=True, labelbottom=False)
    
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
                 rotation_mode="anchor")
    
        # Turn spines off and create white grid.
        # ax.spines[:].set_visible(False)
    
        ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
    
        return im, cbar


    def annotate_heatmap(self, im, data=None, valfmt="{x:.2f}",
                         textcolors=("black", "white"),
                         threshold=None, **textkw):
        """
        A function to annotate a heatmap.
    
        Parameters
        ----------
        im
            The AxesImage to be labeled.
        data
            Data used to annotate.  If None, the image's data is used.  Optional.
        valfmt
            The format of the annotations inside the heatmap.  This should either
            use the string format method, e.g. "$ {x:.2f}", or be a
            `matplotlib.ticker.Formatter`.  Optional.
        textcolors
            A pair of colors.  The first is used for values below a threshold,
            the second for those above.  Optional.
        threshold
            Value in data units according to which the colors from textcolors are
            applied.  If None (the default) uses the middle of the colormap as
            separation.  Optional.
        **kwargs
            All other arguments are forwarded to each call to `text` used to create
            the text labels.
        """
    
        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()
    
        # Normalize the threshold to the images color range.
        if threshold is not None:
            threshold = im.norm(threshold)
        else:
            threshold = im.norm(data.max())/2.
    
        # Set default alignment to center, but allow it to be
        # overwritten by textkw.
        kw = dict(horizontalalignment="center",
                  verticalalignment="center")
        kw.update(textkw)
    
        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
    
        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        texts = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)
    
        return texts
    
    def create_heatmap(self, my_df, x_name, y_name, z_name, ax, cbarlabel = None, cmap="YlGn",valfmt="{x:.3f}"): 
        """
        Create 2D heatmaps to visual 

        Parameters
        ----------
        my_df : TYPE
            DESCRIPTION.
        x_name : TYPE
            DESCRIPTION.
        y_name : TYPE
            DESCRIPTION.
        z_name : TYPE
            DESCRIPTION.
        ax : TYPE
            DESCRIPTION.
        cbarlabel : TYPE, optional
            DESCRIPTION. The default is None.
        cmap : TYPE, optional
            DESCRIPTION. The default is "YlGn".
        valfmt : TYPE, optional
            DESCRIPTION. The default is "{x:.3f}".

        Returns
        -------
        ax : TYPE
            DESCRIPTION.

        """
        targetmapdata = my_df.pivot_table(index = y_name, columns = x_name, values = z_name)
        Z = targetmapdata.to_numpy()
        x_ticks = np.unique(my_df[x_name])
        y_ticks = np.unique(my_df[y_name])
        # return Z, x_ticks, y_ticks
        if cbarlabel == None:
            cbarlabel = z_name
        im, cbar = self.heatmap(Z, col_labels=x_ticks, row_labels=y_ticks,ax = ax, cmap= cmap, cbarlabel= cbarlabel)
        self.annotate_heatmap(im,Z,valfmt=valfmt)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        
        return ax
