# RCAIDE/Library/Methods/Propulsor/Ducted_Fan_Propulsor/translate_conditions_to_dfdc_cases.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Framework.Core import Data  

# ---------------------------------------------------------------------------------------------------------------------- 
# Translate Conditions to DFDC Cases 
# ----------------------------------------------------------------------------------------------------------------------    
def translate_conditions_to_dfdc_cases(dfdc_analysis):
    """  
 
    """    
    # set up aerodynamic Conditions object
    template = dfdc_analysis.settings.filenames.results_template 
    v_infs   = dfdc_analysis.training.freestream_velocity     
    altitude = dfdc_analysis.training.altitude        
    RPMs     = dfdc_analysis.training.RPM           
    
    for i in range(len(v_infs)): 
        for j in range(len(RPMs)):   
            for k in range(len(altitude)):     
                case            = Data()
                case.tag        = template.format(v_infs[i],RPMs[j],altitude[k]) 
                case.velocity   = v_infs[i]
                case.RPM        = RPMs[j]
                case.altitude   = altitude[k]
                dfdc_analysis.append_case(case) 
    return 