# Tutorial for SUMO_utils
Detailed Tutorial for using SUMO_utils. In this tutorial, we will walk through together examples that are provided in this repo (`.\example\examples.py\`) and template scripts can be revised based on users' needs.  

Functionality of this module includes: 
- Standardizing the data format for excel files generated by [`CY_SUMO`](https://github.com/ChengYangUmich/CY_SUMO),specifically handles the *RealArray* data type in SUMO. 
- Generating quick plots to visualize simulation results 
   
 > Author: Cheng Yang, University of Michigan 
 > 
 > Version: 2022_03_29

## Table of contents
1. [Checklist in the `SUMO_utils/example/`](#checklist)
2. [Code](#code)
   - [Dynamic Tables](#dyn_tab)
   - [Steady-state Tables](#ss_tab)
3. [Quick plots](#quickplot)
   - [`Workbook_plot()`](#workbook)
   - [`sheet_plot_yyplot()`](#yyplot)
   - [`sheet_plot_add_line()`& `sheet_plot_add_scatter()`](#add)
   - [`create_heatmap()`](#heatmap)



## Checklist in the `SUMO_utils/example/`<a name="checklist"></a>
> 1. `examples.py`: The template python script showing how to use SUMO_utils. 
> 2. `raw_dyn.xlsx`: An example output excel file from `CY_SUMO.dynamic_run()`.  
>   - This excel has two sheets, namely *Trial1* and *Trial2*.
>   - Each sheet has 8 sumo_variables. Except that `Sumo__Plant__MBBR2__XNITO` is in the `string` format, others are in the `np.float`format. <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/raw_dyn_excel.JPG" alt="FineTempPic" style="height: 100px; width:600px;"/>  
>   - After processing, results are stored in `new_dyn.xlsx`, which has 11 sumo_variables that are `np.float`. The `Sumo__Plant__MBBR2__XNITO` is seperated into  four variables, namely `Sumo__Plant__MBBR2__XNITO_0` to `Sumo__Plant__MBBR2__XNITO_3` <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/new_dyn_excel.JPG" alt="FineTempPic" style="height: 100px; width:1000px;"/>  
> 3. `raw_steady_state.xlsx`: An example output excel file from `CY_SUMO.steady_state()`.
>   - This excel has only one sheet.
>   - Each sheet has 9 sumo_variables. Except that `Sumo__Plant__MBBR2__XNITO` and `SS_cmd` are in the `string` format, others are in the `np.float`format. 
>   - After processing, results are stored in `new_ss.xlsx`, which has 11 sumo_variables that are `np.float`. The `SS_cmd` is dropped. The `Sumo__Plant__MBBR2__XNITO` is seperated into  four variables, namely `Sumo__Plant__MBBR2__XNITO_0` to `Sumo__Plant__MBBR2__XNITO_3.
> 4. `FilesToGenerateExcel` *(optional)*: A folder of materials and a python script `RunToCreateExcels.py` to generate needed excel files. To understand details in these scripts please refer to the [tutorial](https://github.com/ChengYangUmich/CY_SUMO/blob/main/Tutorial.md)  in `CY_SUMO`.
 
## Code<a name="code"></a>
> Import moduel 
> ```python 
> from SUMO_utils import SUMO_utils
> ```

### Dynamic Tables<a name="dyn_tab"></a>
> 1. Create a `SUMO_utils()` object 
> ```python
> test = SUMO_utils()
> ```
> 2. Specify the input excel and the cleaned-up output excel
> ```python
> dyn_excel = "raw_dyn.xlsx"  
> new_dyn_excel = "new_dyn.xlsx"
> ```
> 
> 3. Read and process table, the cleaned-up table will be stored as an Excel file whose name is `new_dyn_excel`.
> ```python 
> test.read_dynamic(dyn_excel, new_excel = new_dyn_excel)
> ```
>> **Attributes**- Only after `read_dynamic()` will the following attributes be initiated. 
>> - `dyn_sheet_names`: The sheet names in `raw_dyn.xlsx` 
>> - `dyn_dic`: The nested dictionary that stores data from the cleaned-up excel
>>    - `keys` are dynamic_sheet_names
>>    - `values` are pd.DataFrames containing data after processing from each dynamic sheet in `raw_dyn.xlsx`.  
>> - `dyn_var_list`: The list of sumo variables after cleaning up.    

### Steady-state Tables<a name="ss_tab"></a>
> 1. Create a `SUMO_utils()` object 
> ```python
> test = SUMO_utils()
> ```
> 2. Specify the input excel and the cleaned-up output excel
> ```python
> ss_excel = "raw_steady_state.xlsx" 
> new_ss_excel = "new_steady_state.xlsx"
> ```
> 
> 3. Read and process table, the cleaned-up table will be stored as an Excel file whose name is `new_ss_excel`.
> ```python 
> test.read_steady_state(steady_state_excel=ss_excel, new_excel=new_ss_excel)
> ```
>> **Attributes**- Only after `read_steady_state()` will the following attributes be initiated. 
>> - `ss_df`: The pandas.DataFrame that stores data from the cleaned-up excel 
>> - `ss_var_list`: The list of sumo variables after cleaning up. 


### Quick plots<a name="quickplot"></a> 
> #### `Workbook_plot()` <a name="workbook"></a> 
> - **This is a method to traverse through all sheets, extract the same x,y variables, and plot them together on one Axis.**
> - **How to use**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/example/examples.py#L48-L69).
> - **Source Code**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/src/SUMO_utils.py#L224-L257). 
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/workbookplot.jpg" alt="FineTempPic" style="height: 400px; width:600px;"/>

> #### `sheet_plot_yyplot()` <a name="yyplot"></a> 
> - **This is a method that focuses on one sheet and generates double-y-axes plot.**
> - **How to use**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/example/examples.py#L71-L96).
> - **Source Code**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/src/SUMO_utils.py#L259-L297). 
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/yyplot.jpg" alt="FineTempPic" style="height: 200px; width:600px;"/>

> #### `sheet_plot_add_line()` and `sheet_plot_add_scatter()` <a name="add"></a> 
> - **These are methods to generate one line or one set of scatters to an existing axis.**
> - **How to use**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/example/examples.py#L98-L124).
> - **Source Code**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/src/SUMO_utils.py#L299-L313). 
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/LineAndScatter.jpg" alt="FineTempPic" style="height: 200px; width:600px;"/>

> #### `create_heatmap()`<a name="heatmap"></a> 
> - **This a methods to generate 2D heatmaps for sensitivity analysis.** 
>> - There are two internal methods embeded: `heatmap()` and `annotate_heatmap()`.
>> - **Parameters**
>>    - `my_df`: pd.DataFrame, usually is the `self.ss_df`.
>>    - `x_name`, `y_name`, `z_name`, string, variable names in `my_df`.
>>    - `ax`: the axis to plot the heatmap.
>>    - `cbarlabel`: the label of the colorbar (z_variable). 
>>    - `cmap`: color map to use. Other options are available [here](https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html). 
>>    - `valfmt`: value format of numbers shown on the heatmap. 
> - **How to use**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/example/examples.py#L127-L139).
> - **Source Code**: please see [here](https://github.com/ChengYangUmich/SUMO_utils/blob/c64e5878c7aed2af1b72c9761e5ba8dec9b9111b/src/SUMO_utils.py#L431-L472). 
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/heatmap.jpg" alt="FineTempPic" style="height: 400px; width:600px;"/>
