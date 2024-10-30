## @ingroup Library-Missions-Common-Unpack_Unknowns
# RCAIDE/Library/Missions/Common/Unpack_Unknowns/orientation.py
# 
# 
# Created:  Jul 2023, M. Clarke

from RCAIDE.Framework.Core import  Units

# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Unpack_Unknowns
def orientation(segment): 
        
    ctrls    = segment.assigned_control_variables 

    # Body Angle Control    
    if ctrls.body_angle.active: 
        if  ctrls.body_angle.initial_guess_values !=  None:
            segment.state.conditions.frames.body.inertial_rotations[:,1]  = ctrls.body_angle.initial_guess_values[0][0]
        else:  
            segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.state.unknowns.body_angle[:,0] * 0 
    else:
        segment.state.conditions.frames.body.inertial_rotations[:,0] = segment.angle_of_attack            

    if ctrls.bank_angle.active: 
        if  ctrls.bank_angle.initial_guess_values !=  None:
            segment.state.conditions.frames.body.inertial_rotations[:,0]  = ctrls.bank_angle.initial_guess_values[0][0]
        else:          
            segment.state.conditions.frames.body.inertial_rotations[:,0] = segment.state.unknowns.bank_angle[:,0]
    else:
        segment.state.conditions.frames.body.inertial_rotations[:,0] = segment.bank_angle
        
    #segment.state.conditions.frames.body.inertial_rotations[:,2] =  segment.state.conditions.frames.planet.true_heading[:,0] -  segment.sideslip_angle # INCORRER
    segment.state.conditions.frames.body.inertial_rotations[:,2] =  segment.state.conditions.frames.planet.true_heading[:,0] # WORKS
    
    # Velocity Control
    if ctrls.velocity.active:
        if  ctrls.velocity.initial_guess_values !=  None:
            segment.state.conditions.frames.inertial.velocity_vector[:,0]  = ctrls.velocity.initial_guess_values[0][0]
        else:  
            segment.state.conditions.frames.inertial.velocity_vector[:,0] = segment.state.unknowns.velocity[:,0]
        
    # Altitude Control
    if ctrls.altitude.active:
        if  ctrls.altitude.initial_guess_values !=  None:
            segment.state.conditions.frames.inertial.position_vector[:,2]  = -ctrls.altitude.initial_guess_values[0][0]
        else:  
            segment.state.conditions.frames.inertial.position_vector[:,2] = -segment.state.unknowns.altitude[:,0]
        
    return 
            
            
            