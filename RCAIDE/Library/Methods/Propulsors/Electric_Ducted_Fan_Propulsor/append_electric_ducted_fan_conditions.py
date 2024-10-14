# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/append_electric_ducted_fan_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports  
from RCAIDE.Framework.Mission.Common                             import Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append electric ducted fan network conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_electric_ducted_fan_conditions(propulsor,segment,bus,add_additional_network_equation):
    '''
    
    
    
    '''
    ones_row    = segment.state.ones_row
                
    segment.state.conditions.energy[bus.tag][propulsor.tag]                               = Conditions()  
    segment.state.conditions.energy[bus.tag][propulsor.tag].throttle                      = 0. * ones_row(1)      
    segment.state.conditions.energy[bus.tag][propulsor.tag].commanded_thrust_vector_angle = 0. * ones_row(1)  
    segment.state.conditions.energy[bus.tag][propulsor.tag].thrust                        = 0. * ones_row(3) 
    segment.state.conditions.energy[bus.tag][propulsor.tag].power                         = 0. * ones_row(1) 
    segment.state.conditions.energy[bus.tag][propulsor.tag].moment                        = 0. * ones_row(3)   

    if add_additional_network_equation:                       
        ducted_fan   = propulsor.ducted_fan
        cp_init      = ducted_fan.cruise.design_power_coefficient
        segment.state.unknowns[ propulsor.tag  + '_ducted_fan_cp']               = cp_init * ones_row(1)  
        segment.state.residuals.network[ propulsor.tag  + '_ducted_fan_motor_torque'] = 0. * ones_row(1)        
    return