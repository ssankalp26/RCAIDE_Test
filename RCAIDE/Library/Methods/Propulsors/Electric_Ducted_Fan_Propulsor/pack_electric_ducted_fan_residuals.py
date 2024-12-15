# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/pack_electric_ducted_fan_residuals.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke   

# ---------------------------------------------------------------------------------------------------------------------- 
#  pack electric ducted_fan network residuals
# ----------------------------------------------------------------------------------------------------------------------  

def pack_electric_ducted_fan_residuals(propulsor,segment):  
    motor         = propulsor.motor
    ducted_fan    = propulsor.ducted_fan 
    q_motor       = segment.state.conditions.energy[propulsor.tag][motor.tag].torque
    q_ducted_fan  = segment.state.conditions.energy[propulsor.tag][ducted_fan.tag].torque 
    segment.state.residuals.network[propulsor.tag  + '_ducted_fan_motor_torque'] = q_motor - q_ducted_fan
    return 
