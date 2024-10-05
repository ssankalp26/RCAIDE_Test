# RCAIDE/Library/Methods/Propulsor/Ducted_Fan_Propulsor/read_results.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

import RCAIDE
from RCAIDE.Framework.Core import Data, Units  
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
# Read Results 
# ----------------------------------------------------------------------------------------------------------------------  
def read_results(dfdc_analysis):
    """ This functions reads the results from the results text file created 
    at the end of an DFDC function call

    Assumptions:
        None
        
    Source: 

    Inputs:
        None

    Outputs:
        results     

    Properties Used:
        N/A
    """     
    ducted_fan        = dfdc_analysis.geometry
    Nr                = ducted_fan.number_of_radial_stations
    results_template  = dfdc_analysis.settings.filenames.results_template 
    v_infs            = dfdc_analysis.training.freestream_velocity               
    RPMs              = dfdc_analysis.training.RPM
    len_v             = len(v_infs)
    len_rpm           = len(RPMs)

    results                                  = Data()
    results.geometry                         = Data() 
    results.geometry.twist_distribution      = np.zeros(Nr)
    results.geometry.chord_distribution      = np.zeros(Nr)
    results.geometry.radius_distribution     = np.zeros(Nr)
    results.geometry.number_of_blades        = np.zeros(Nr)
    results.geometry.solidity_distribution   = np.zeros(Nr)
    results.cruise.design_power_coefficient  = 0
    results.cruise.design_thrust_coefficient = 0  
    results.performance                      = Data()
    results.performance.thrust               = np.zero((len_v,len_rpm))  
    results.performance.power                = np.zero((len_v,len_rpm))  
    results.performance.efficiency           = np.zero((len_v,len_rpm)) 
    results.performance.torque               = np.zero((len_v,len_rpm)) 
    results.performance.thrust_coefficient   = np.zero((len_v,len_rpm))  
    results.performance.power_coefficient    = np.zero((len_v,len_rpm)) 
    results.performance.advance_ratio        = np.zero((len_v,len_rpm))
    results.performance.figure_of_merit      = np.zero((len_v,len_rpm))    

    geometry_filename   = ducted_fan.tag + '.txt'            
    with open(geometry_filename,'r') as geometry_file: 
            geometry_lines                       = geometry_file.readlines() 
            results.cruise.design_power_coefficient  = float(geometry_lines[8][10:16].strip())
            results.cruise.design_thrust_coefficient = float(geometry_lines[8][10:16].strip()) 
            for n_r in  range(Nr):
                results.geometry.twist_distribution      = float(geometry_lines[n_r + 8][10:16].strip())
                results.geometry.chord_distribution      = float(geometry_lines[n_r + 8][10:16].strip())
                results.geometry.radius_distribution     = float(geometry_lines[n_r + 8][10:16].strip())
                results.geometry.number_of_blades        = float(geometry_lines[n_r + 8][10:16].strip())
                results.geometry.solidity_distribution   = float(geometry_lines[n_r + 8][10:16].strip())
    
    for i in range(len_v): 
        for j in range(len_rpm):       
            results_filename   = results_template.format(v_infs[i],RPMs[j])  
            with open(results_filename,'r') as case_results_file: 
                case_lines                       = case_results_file.readlines()
                results.thrust[i,j]              = float(case_lines[8][10:16].strip())
                results.power[i,j]               = float(case_lines[8][31:37].strip())
                results.efficiency[i,j]          = float(case_lines[8][52:58].strip()) 
                results.torque[i,j]              = float(case_lines[8][52:58].strip())        
                results.thrust_coefficient[i,j]  = float(case_lines[9][10:16].strip())        
                results.power_coefficient[i,j]   = float(case_lines[9][10:16].strip())   
                results.advance_ratio[i,j]       = float(case_lines[9][10:16].strip())      
                results.figure_of_merit[i,j]     = float(case_lines[9][10:16].strip())    

    return results
