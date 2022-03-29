# Tutorial for SUMO_utils
Detailed Tutorial for using SUMO_utils. In this tutorial, we will walk through together examples that are provided in this repo (`.\example\examples.py\`) and template scripts can be revised based on users' needs.  
 > Author: Cheng Yang, University of Michigan 
 > 
 > Version: 2022_03_29

## Table of contents

## Checklist in the `SUMO_utils/example/`
> - `examples.py`: The template python script showing how to use SUMO_utils. 
> - `raw_dyn.xlsx`: An example output excel file from `CY_SUMO.dynamic_run()`  
>   - In this excel, it has two sheets, namely `Trial1` and `Trial2` 
>   - In each sheet, it has 8 sumo_variables. Except that `Sumo__Plant__MBBR2__XNITO` is in a string format, others are in np.float <img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/raw_dyn_excel.JPG" alt="FineTempPic" style="height: 100px; width:600px;"/>  
>   - After processing, results are stored in `new_dyn.xlsx`<img src="https://github.com/ChengYangUmich/SUMO_utils/blob/main/example/Pics/new_dyn_excel.JPG" alt="FineTempPic" style="height: 100px; width:1000px;"/>  
>   The `Sumo__Plant__MBBR2__XNITO` is seperated into  four variables, namely `Sumo__Plant__MBBR2__XNITO_0` to `Sumo__Plant__MBBR2__XNITO_3`
> - `FilesToGenerateExcel` *(optional)*: A folder of scripts to generate needed excel files. To understand details in these scripts please refer to the [tutorial](https://github.com/ChengYangUmich/CY_SUMO/blob/main/Tutorial.md)  in `CY_SUMO`
> 
> 
