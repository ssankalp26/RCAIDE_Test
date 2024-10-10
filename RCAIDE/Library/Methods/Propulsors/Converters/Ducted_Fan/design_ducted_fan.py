# RCAIDE/Library/Methods/Propulsors/Converters/Ducted_Fan.py
#  
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Analyses.Propulsion.Ducted_Fan_Design_Code import Ducted_Fan_Design_Code
from RCAIDE.Framework.Core import Data ,redirect   
from RCAIDE.Library.Plots  import *       
from scipy.interpolate     import RegularGridInterpolator
 
# python imports   
from shutil import rmtree
from .write_geometry                     import  write_geometry
from .write_input_deck                   import  write_input_deck
from .run_dfdc_analysis                  import  run_dfdc_analysis
from .translate_conditions_to_dfdc_cases import  translate_conditions_to_dfdc_cases
from .read_results                       import  read_results
from scipy.interpolate import interp1d
import os
import numpy as  np

# ----------------------------------------------------------------------------------------------------------------------
#  design_ducted_fan
# ---------------------------------------------------------------------------------------------------------------------- 
def design_ducted_fan(ducted_fan): 
    '''
    
    
    
    '''    
    dfdc_analysis                                   = Ducted_Fan_Design_Code() 
    dfdc_analysis.geometry                          = ducted_fan 
    run_folder                                      = os.path.abspath(dfdc_analysis.settings.filenames.run_folder)
    run_script_path                                 = run_folder.rstrip('dfdc_files').rstrip('/')    
    deck_template                                   = dfdc_analysis.settings.filenames.deck_template 
    print_output                                    = dfdc_analysis.settings.print_output  
    dfdc_analysis.current_status.deck_file          = deck_template.format(1)
 
    # translate conditions  
    translate_conditions_to_dfdc_cases(dfdc_analysis)  
    dfdc_analysis.settings.filenames.case  =  dfdc_analysis.geometry.tag +  '.case'
    # write the input files
    with redirect.folder(run_folder,force=False):
        write_geometry(dfdc_analysis,run_script_path)    
        write_input_deck(dfdc_analysis)   

        # RUN DFDC!
        _ = run_dfdc_analysis(dfdc_analysis,print_output)

    # translate results
    results = read_results(dfdc_analysis)

    if not dfdc_analysis.settings.keep_files:
        rmtree(run_folder) 
         
    # save blade geometry 
    ducted_fan.rotor.twist_distribution           = results.geometry.rotor_twist_distribution            
    ducted_fan.rotor.chord_distribution           = results.geometry.rotor_chord_distribution            
    ducted_fan.rotor.radius_distribution          = results.geometry.rotor_radius_distribution           
    ducted_fan.rotor.non_dim_radius_distribution  = results.geometry.rotor_non_dim_radius_distribution   
    ducted_fan.rotor.solidity_distribution        = results.geometry.rotor_solidity_distribution         
    ducted_fan.stator.twist_distribution          = results.geometry.stator_twist_distribution           
    ducted_fan.stator.chord_distribution          = results.geometry.stator_chord_distribution           
    ducted_fan.stator.radius_distribution         = results.geometry.stator_radius_distribution          
    ducted_fan.stator.non_dim_radius_distribution = results.geometry.stator_non_dim_radius_distribution  
    ducted_fan.stator.solidity_distribution       = results.geometry.stator_solidity_distribution   

    V_inf             = dfdc_analysis.training.freestream_velocity               
    tip_mach          = dfdc_analysis.training.tip_mach         
    altitude          = dfdc_analysis.training.altitude 
    
    ducted_fan.cruise.design_thrust             = results.performance.design_thrust            
    ducted_fan.cruise.design_power              = results.performance.design_power             
    ducted_fan.cruise.design_efficiency         = results.performance.design_efficiency        
    ducted_fan.cruise.design_torque             = results.performance.design_torque            
    ducted_fan.cruise.design_thrust_coefficient = results.performance.design_thrust_coefficient
    ducted_fan.cruise.design_power_coefficient  = results.performance.design_power_coefficient  
    
    # create performance surrogates 
    raw_data           = results.performance
    thrust             = clean_data(raw_data.thrust,V_inf,tip_mach,altitude,raw_data.converged_solution)               
    power              = clean_data(raw_data.power,V_inf,tip_mach,altitude,raw_data.converged_solution)                
    efficiency         = clean_data(raw_data.efficiency,V_inf,tip_mach,altitude,raw_data.converged_solution)           
    torque             = clean_data(raw_data.torque,V_inf,tip_mach,altitude,raw_data.converged_solution)               
    thrust_coefficient = clean_data(raw_data.thrust_coefficient,V_inf,tip_mach,altitude,raw_data.converged_solution)   
    power_coefficient  = clean_data(raw_data.power_coefficient,V_inf,tip_mach,altitude,raw_data.converged_solution)    
    advance_ratio      = clean_data(raw_data.advance_ratio,V_inf,tip_mach,altitude,raw_data.converged_solution)       
    
    surrogates =  Data()
    surrogates.thrust              = RegularGridInterpolator((V_inf,tip_mach,altitude),thrust               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.power               = RegularGridInterpolator((V_inf,tip_mach,altitude),power                ,method = 'linear',   bounds_error=False, fill_value=None)
    surrogates.efficiency          = RegularGridInterpolator((V_inf,tip_mach,altitude),efficiency           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.torque              = RegularGridInterpolator((V_inf,tip_mach,altitude),torque               ,method = 'linear',   bounds_error=False, fill_value=None)
    surrogates.thrust_coefficient  = RegularGridInterpolator((V_inf,tip_mach,altitude),thrust_coefficient   ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.power_coefficient   = RegularGridInterpolator((V_inf,tip_mach,altitude),power_coefficient    ,method = 'linear',   bounds_error=False, fill_value=None)
    surrogates.advance_ratio       = RegularGridInterpolator((V_inf,tip_mach,altitude),advance_ratio        ,method = 'linear',   bounds_error=False, fill_value=None)  
    
    ducted_fan.performance_surrogates =  surrogates
    return

def clean_data(raw_data,V_inf,tip_mach,altitude,convergence_matrix):
    threshold =  2
    cleaned_data =  np.zeros((len(V_inf),len(tip_mach),len(altitude)))
    for i in range(len(V_inf)): 
        for k in range(len(altitude)):
            
            raw_data_f1 = []
            indexes_f1  = []
            for idx, x in enumerate(raw_data[i, :, k]):
                if not np.isnan(x):
                    raw_data_f1.append(x)
                    indexes_f1.append(idx) 

            z_scores      = np.abs((np.array(raw_data_f1) - np.array(raw_data_f1).mean()) /np.array(raw_data_f1).std())
            filter_flag   =  z_scores < threshold
            raw_data_f2   = np.array(raw_data_f1)[filter_flag]
            indexes_f2    = np.array(indexes_f1)[filter_flag]
            filtered_alt  = altitude[indexes_f2]
            
            f = interp1d(filtered_alt, raw_data_f2, fill_value="extrapolate") 
            
            # Interpolate y values using the spline function
            cleaned_data[i, :, k] = f(altitude) 
    
    return cleaned_data

