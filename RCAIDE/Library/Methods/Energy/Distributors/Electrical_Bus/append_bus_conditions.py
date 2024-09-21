# RCAIDE/Methods/Energy/Sources/Battery/Common/append_battery_conditions.py
# 
# 
# Created: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  METHODS
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery 
def append_bus_conditions(bus,segment): 
    """ Appends the initial bus conditions
        
        Assumptions:
        N/A
    
        Source:
        N/A
    
        Inputs:  
       
        Outputs:
           
        Properties Used:
        None
        """
    ones_row                                                = segment.state.ones_row

    segment.state.conditions.energy[bus.tag]                = Conditions()
    segment.state.conditions.energy[bus.tag].power_draw     = 0 * ones_row(1)  
    segment.state.conditions.energy[bus.tag].current_draw   = 0 * ones_row(1)
     
    return    