# RCAIDE/Framework/Analyses/Propulsion/Ducted_Fan_Design_Code.py
#  
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units ,Data ,redirect   
from RCAIDE.Library.Plots  import *       
 
# python imports   
from shutil import rmtree
from RCAIDE.Framework.Analyses.Propulsion.Ducted_Fan_Design_Code import Ducted_Fan_Design_Code
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
        dfdc_results = run_dfdc_analysis(dfdc_analysis,print_output)

    # translate results
    results = read_results(dfdc_analysis)

    if not dfdc_analysis.settings.keep_files:
        rmtree( run_folder )
        
        
    # TO DO: BUILD SURROGATES AND STORE OF ducted fan data structure    
        
       
    return