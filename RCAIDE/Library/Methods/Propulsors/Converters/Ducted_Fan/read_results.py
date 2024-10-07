# RCAIDE/Library/Methods/Propulsor/Ducted_Fan_Propulsor/read_results.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Framework.Core import Data, Units  
import numpy as np
import  os 
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
    run_folder        = dfdc_analysis.settings.filenames.run_folder
    v_infs            = dfdc_analysis.training.freestream_velocity               
    RPMs              = dfdc_analysis.training.RPM
    len_v             = len(v_infs)
    len_rpm           = len(RPMs)

    results                                             = Data()
    results.geometry                                    = Data() 
    results.geometry.rotor_twist_distribution           = np.zeros(Nr)
    results.geometry.rotor_chord_distribution           = np.zeros(Nr)
    results.geometry.rotor_radius_distribution          = np.zeros(Nr) 
    results.geometry.rotor_non_dim_radius_distribution  = np.zeros(Nr) 
    results.geometry.rotor_solidity_distribution        = np.zeros(Nr)
    results.geometry.stator_twist_distribution          = np.zeros(Nr)
    results.geometry.stator_chord_distribution          = np.zeros(Nr)
    results.geometry.stator_radius_distribution         = np.zeros(Nr) 
    results.geometry.stator_non_dim_radius_distribution = np.zeros(Nr) 
    results.geometry.stator_solidity_distribution       = np.zeros(Nr)
    results.geometry.design_power_coefficient           = 0
    results.geometry.design_thrust_coefficient          = 0  
    results.performance                                 = Data()
    results.performance.thrust                          = np.zeros((len_v,len_rpm))  
    results.performance.power                           = np.zeros((len_v,len_rpm))  
    results.performance.efficiency                      = np.zeros((len_v,len_rpm)) 
    results.performance.torque                          = np.zeros((len_v,len_rpm)) 
    results.performance.thrust_coefficient              = np.zeros((len_v,len_rpm))  
    results.performance.power_coefficient               = np.zeros((len_v,len_rpm)) 
    results.performance.advance_ratio                   = np.zeros((len_v,len_rpm))
    results.performance.figure_of_merit                 = np.zeros((len_v,len_rpm))    
 
    geometry_filename   =   os.path.abspath(run_folder + os.path.sep+ ducted_fan.tag + '_geometry.txt')            
    with open(geometry_filename,'r') as geometry_file: 
            geometry_lines                       = geometry_file.readlines() 
            results.geometry.hub_radius          = float(geometry_lines[27][12:23].strip())
            results.geometry.tip_radius          = float(geometry_lines[27][35:44].strip()) 
                
            for n_r in range(Nr):
                results.geometry.rotor_radius_distribution[n_r]         = float(geometry_lines[36 + Nr + n_r][0:12].strip())
                results.geometry.rotor_non_dim_radius_distribution[n_r] = float(geometry_lines[36 + Nr + n_r][12:22].strip())
                results.geometry.rotor_chord_distribution[n_r]          = float(geometry_lines[36 + Nr + n_r][22:35].strip())
                results.geometry.rotor_twist_distribution[n_r]          = float(geometry_lines[36 + Nr + n_r][35:44].strip()) * Units.degrees
                results.geometry.rotor_solidity_distribution[n_r]       = float(geometry_lines[36 + Nr + n_r][44:56].strip())
    
    for i in range(len_v): 
        for j in range(len_rpm):
            results_filename   =  os.path.abspath(run_folder + os.path.sep+ results_template.format(v_infs[i],RPMs[j]) )  
            with open(results_filename,'r') as case_results_file: 
                case_lines                       = case_results_file.readlines() 
                results.performance.thrust[i,j]              = float(case_lines[8][13:26].strip())
                results.performance.power[i,j]               = float(case_lines[8][39:52].strip())
                results.performance.efficiency[i,j]          = float(case_lines[8][65:76].strip()) 
                results.performance.torque[i,j]              = float(case_lines[10][39:52].strip())        
                results.performance.thrust_coefficient[i,j]  = float(case_lines[13][7:20].strip())        
                results.performance.power_coefficient[i,j]   = float(case_lines[13][27:39].strip())   
                results.performance.advance_ratio[i,j]       = float(case_lines[13][45:57].strip())    

    return results
