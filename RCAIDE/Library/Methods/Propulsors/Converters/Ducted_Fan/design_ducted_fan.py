# RCAIDE/Framework/Analyses/Propulsion/Ducted_Fan_Design_Code.py
#  
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Analyses.Propulsion.Ducted_Fan_Design_Code import Ducted_Fan_Design_Code
from RCAIDE.Framework.Core import Units ,Data ,redirect   
from RCAIDE.Library.Plots  import *       
from scipy.interpolate     import RegularGridInterpolator
 
# python imports   
from shutil import rmtree
from .write_geometry                     import  write_geometry
from .write_input_deck                   import  write_input_deck
from .run_dfdc_analysis                  import  run_dfdc_analysis
from .translate_conditions_to_dfdc_cases import  translate_conditions_to_dfdc_cases
from .read_results                       import  read_results
import os

# ----------------------------------------------------------------------------------------------------------------------
#  design_ducted_fan
# ---------------------------------------------------------------------------------------------------------------------- 
def design_ducted_fan(ducted_fan):
    
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
    
    
    # create performance surrogates 
    raw_data = results.performance
    thrust             = clean_data(raw_data.thrust,raw_data.converged_solution)               
    power              = clean_data(raw_data.power,raw_data.converged_solution)                
    efficiency         = clean_data(raw_data.efficiency,raw_data.converged_solution)           
    torque             = clean_data(raw_data.torque,raw_data.converged_solution)               
    thrust_coefficient = clean_data(raw_data.thrust_coefficient,raw_data.converged_solution)   
    power_coefficient  = clean_data(raw_data.power_coefficient,raw_data.converged_solution)    
    advance_ratio      = clean_data(raw_data.advance_ratio,raw_data.converged_solution)        
    figure_of_merit    = clean_data(raw_data.figure_of_merit,raw_data.converged_solution)     

    V_inf             = dfdc_analysis.training.freestream_velocity               
    RPM               = dfdc_analysis.training.RPM         
    altitude          = dfdc_analysis.training.altitude
    
    surrogates =  Data()
    surrogates.thrust              = RegularGridInterpolator((V_inf,RPM,altitude),thrust               ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.power               = RegularGridInterpolator((V_inf,RPM,altitude),power                ,method = 'linear',   bounds_error=False, fill_value=None)
    surrogates.efficiency          = RegularGridInterpolator((V_inf,RPM,altitude),efficiency           ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.torque              = RegularGridInterpolator((V_inf,RPM,altitude),torque               ,method = 'linear',   bounds_error=False, fill_value=None)
    surrogates.thrust_coefficient  = RegularGridInterpolator((V_inf,RPM,altitude),thrust_coefficient   ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.power_coefficient   = RegularGridInterpolator((V_inf,RPM,altitude),power_coefficient    ,method = 'linear',   bounds_error=False, fill_value=None)
    surrogates.advance_ratio       = RegularGridInterpolator((V_inf,RPM,altitude),advance_ratio        ,method = 'linear',   bounds_error=False, fill_value=None)      
    surrogates.figure_of_merit     = RegularGridInterpolator((V_inf,RPM,altitude),figure_of_merit      ,method = 'linear',   bounds_error=False, fill_value=None)
    
    ducted_fan.performance_surrogates =  surrogates
    return

def clean_data(data,convergence_matrix):
    
    
    return clean_data