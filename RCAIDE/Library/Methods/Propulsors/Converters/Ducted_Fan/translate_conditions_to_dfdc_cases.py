# RCAIDE/Library/Methods/Propulsor/Ducted_Fan_Propulsor/translate_conditions_to_dfdc_cases.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
import  RCAIDE
from RCAIDE.Framework.Core import Data ,Units

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
    tip_mach = dfdc_analysis.training.tip_mach 
    
    for i in range(len(v_infs)): 
        for j in range(len(tip_mach)):   
            for k in range(len(altitude)):     
                case            = Data()
    
                atmosphere      = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
                atmo_data       = atmosphere.compute_values(altitude[k]) 
                a               = atmo_data.speed_of_sound[0,0] 
                rpm             = ((tip_mach[j]*a) /dfdc_analysis.geometry.tip_radius)/Units.rpm
                case.tag        = template.format(v_infs[i],rpm,altitude[k]) 
                case.velocity   = v_infs[i]
                case.RPM        = rpm
                case.altitude   = altitude[k]
                dfdc_analysis.append_case(case) 
    return 