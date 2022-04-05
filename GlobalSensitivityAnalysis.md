# Global Sensitivity Analysis for SUMO projects 
This is a tutorial and template for conducting Global sensitivity analysis [`CY_SUMO`](https://github.com/ChengYangUmich/CY_SUMO). 
In this tutorial, we will walk through together an example that are provided in this repo (`.\example\globalSA.py\`) and template scripts can be revised based on users' needs.  
 > **Template script:** [Here]() 
 > 
 > **Author:** Cheng Yang, University of Michigan 
 > 
 > **Version:** 2022_04_04

> **References:**
> **Theory:** Sobol, I. M. (2001). Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates. Mathematics and computers in simulation, 55(1-3), 271-280. 
> 
> **Python package:** [SALib](https://salib.readthedocs.io/en/latest/index.html)

# Preparation 
> ## Materials (what needed to run steady-state simulations with CY_SUMO):
> - Digital twin license from Dynamita 
> - A functional SUMO project (`XXX.sumo`) in GUI, where the following items could be generated and copied to the directory where python scripts locate: 
>     - `sumoproject.dll` - the SUMO computational core.
>     -  `XXX.xml` - an xml file that stores all current values/information of SUMO comuputation 
> *Note*: In this example, the related files are stored in [`.\example\GlobalSensitivityAnalysis\`](https://github.com/ChengYangUmich/SUMO_utils/tree/main/example/GlobalSensitivityAnalysis)
> ## Dependencies: 
> The following dependencies are *required* to run this template:
> - `sumo.sumoscheduler` and its dependencies.  --> available as the './src/sumoscheduler.py'
> - [`numpy`](https://numpy.org/doc/stable/user/index.html)
> - [`pandas`](https://pandas.pydata.org/)
> - [`os`](https://docs.python.org/3/library/os.html)
> - [`datatime`](https://docs.python.org/3/library/datetime.html) 
> - [`time`](https://docs.python.org/3/library/time.html) 
> - [`SALib`](https://salib.readthedocs.io/en/latest/index.html)
> - [`matplotlib.pyplot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html) 

#   An Example 
> ## SUMO model
> In this example, we will perform a Sobol’ sensitivity analysis (global) of DO setpoints in three aerated tanks of the MLE process, shown below. 
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/A2O.JPG" alt="FineTempPic" style="height: 300px; width:1000px;"/>  
> The SUMO model is available in [`.\example\GlobalSensitivityAnalysis\`](https://github.com/ChengYangUmich/SUMO_utils/tree/main/example/GlobalSensitivityAnalysis). 
> 
> *Note*: This example is simply to provide a template, settings used may not be practical in reality. 
>  
>  ## Sensitivity Objective 
>  Identifying which DO setpoint in the last three tanks has the greatest influent on the effluent ammonia. 
>  
>  ## Code Implementation
>  ### Importing Packages and modules  
> ```python 
> import os
> import pandas as pd 
> import numpy as np
> import datetime
> import matplotlib.pyplot as plt
> # Packages needed for Global Sensitivity Analysis
> from SALib.sample import saltelli
> from SALib.analyze import sobol
> # Self-written module 
> from CY_SUMO import CY_SUMO, create_param_dict
> ```
> ### Defining the Sensitivity Analysis Settings 
> ``` python
> SA_inputs = {
>    'num_vars': 3,
>    'names': ['Sumo__Plant__CSTR3__param__DOSP', 
>              'Sumo__Plant__CSTR4__param__DOSP', 
>              'Sumo__Plant__CSTR5__param__DOSP'],  # The DO setpoints for three tanks 
>    'bounds': [[0, 4],
>               [0, 4],
>               [0, 4]]
> }
> ```
> ### Generate Samples 
> ```python
> param_values = saltelli.sample(SA_inputs, 128, calc_second_order=False) 
> ```
> Here, param_values is a NumPy matrix. If we run param_values.shape, we see that the matrix is 640 by 3. The Saltelli sampler generated 640 samples. 
> By default, the Saltelli sampler generates `N * (2D+2)` samples in default. If the keyword argument `calc_second_order=False`, then the generator will exclude second-order indices, resulting in a smaller sample matrix, as in this example , total samples is `N*(D+2)` where N = 128 (the number of samples) and and D =  3 (the number of model inputs). For details, please refer the reference paper and [wikipedia:varianace-based sensitivity analysis](https://en.wikipedia.org/wiki/Variance-based_sensitivity_analysis). 
> ### Run model 
> ```python
>  # Create steady-state input dictionary 
> param_dict = {}
> for i in range(len(param_values)):
>     temp_dict = {}
>     for j, a_var in enumerate(SA_inputs['names']):
>         temp_dict[a_var] = param_values[i,j] 
>     param_dict[f'Trial{i+1}'] = temp_dict
> 
> # Run model
> # Get current path 
> current_path = os.getcwd()
> # Initiate name string of the sumo .dll core    
> model = os.path.join(current_path,"AOplant.dll")
> # Create a list of sumo incode variables to track 
> sumo_variables = ["Sumo__Plant__Effluent1__SNHx"]
> # Create a CY_SUMO object 
> test = CY_SUMO(model= model,sumo_variables=sumo_variables,param_dic=param_dict)
> test.steady_state(save_table = True, 
>                  save_name = "SA_result.xlsx", 
>                  save_xml = False)
> ```  
> ### Perform Analysis
> ```python
> # Extract the simulation reuslts 
> Y = np.array(test.SS_table["Sumo__Plant__Effluent1__SNHx"])
> # # Perform analysis
> Si = sobol.analyze(SA_inputs, Y, calc_second_order=False)
> ```
> ### Visualize Results
> #### Visualize how samples are collected 
> ```python
> ax = plt.axes(projection='3d')
> ax.scatter3D(param_values[:,0], param_values[:,1], param_values[:,2], 'blue')
> plt.savefig('..\Pics\SA_inputs.jpg')
> ```
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/SA_inputs.jpg" alt="FineTempPic" style="height: 300px; width:300px;"/>  
> 
> #### Visualize the relationship between x's and y in the samples 
> ```python
> fig, axs = plt.subplots(1,3,figsize= (8,3))
> for i,an_ax in enumerate(axs):
>     an_ax.scatter(param_values[:,i],Y)
>     an_ax.set_xlabel('DO setpoints, mg/L')
>     an_ax.set_ylabel('Effluent ammonia, mg-N/L')
>     an_ax.set_title(f'Tank {i+3}')
> fig.tight_layout()
> fig.savefig('..\Pics\AOplantScatter.jpg')
> ```
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/AOplantScatter.jpg" alt="FineTempPic" style="height: 300px; width:800px;"/>  
>
> #### Visualize the sobol indices as results of the global sensitivity analysis 
> It looks like the last tank DO explains the most variances in the effluent ammonia. If the total-order indices are substantially larger than the first-order indices, then there is likely higher-order interactions occurring.Therefore, strong interactions could be seen among tanks.   
> ```python
> fig, axs = plt.subplots(1,2,figsize= (8,4))
> T = Si.plot(ax=axs)
> for an_ax in T:
>     an_ax.set_xlabel('DO setpoints')
>     an_ax.set_ylabel('Sensitivity Index')
>     an_ax.set_xticklabels(['Tank3','Tank4','Tank5'])
> fig.tight_layout()
> fig.savefig('..\Pics\SobolIndex.jpg')
> ```
> <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/SobolIndex.jpg" alt="FineTempPic" style="height: 300px; width:700px;"/>  
