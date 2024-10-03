# RCAIDE/Methods/Weights/Correlation_Buildups/Common/operating_empty_weight.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.Transport import compute_operating_empty_weight as compute_operating_empty_weight_transport

# ---------------------------------------------------------------------------------------------------------------------- 
# Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle,
                                   settings=None,
                                   method_type='RCAIDE', 
                                   update_fuel_weight = True):
    """
    """
    output =  compute_operating_empty_weight_transport(vehicle,settings,method_type,update_fuel_weight) 

    return output
