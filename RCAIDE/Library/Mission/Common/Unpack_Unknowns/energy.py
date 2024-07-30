## @ingroup Library-Missions-Common-Unpack_Unknowns
# RCAIDE/Library/Missions/Common/Unpack_Unknowns/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke
import  RCAIDE
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Unpack_Unknowns
def fuel_line_unknowns(segment,fuel_lines):
    assigned_control_variables = segment.assigned_control_variables
    state           = segment.state 

    # Throttle Control 
    if 'throttle' in segment:
        for fuel_line in fuel_lines:
            for propulsor in fuel_line.propulsors: 
                state.conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0] = segment.throttle 
    elif assigned_control_variables.throttle.active:                
        for i in range(len(assigned_control_variables.throttle.assigned_propulsors)):
            propulsor_tags = assigned_control_variables.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for fuel_line in fuel_lines:
                    if propulsor_tags[j] in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tags[j]].throttle = state.unknowns["throttle_" + str(i)]   
     
    # Thrust Vector Control 
    if assigned_control_variables.thrust_vector_angle.active:                
        for i in range(len(assigned_control_variables.thrust_vector_angle.assigned_propulsors)): 
            propulsor_tags = assigned_control_variables.thrust_vector_angle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for fuel_line in fuel_lines:
                    if propulsor_tags[j] in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tags[j]].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]    
    return 

def bus_unknowns(segment,busses): 
    assigned_control_variables = segment.assigned_control_variables
    state           = segment.state 

    # Throttle Control 
    if 'throttle' in segment:
        for bus in busses:
            for propulsor in bus.propulsors: 
                state.conditions.energy[bus.tag][propulsor.tag].throttle[:,0] = segment.throttle 
    elif assigned_control_variables.throttle.active:                
        for i in range(len(assigned_control_variables.throttle.assigned_propulsors)): 
            propulsor_tags = assigned_control_variables.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for bus in busses:
                    if propulsor_tags[j] in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tags[j]].throttle = state.unknowns["throttle_" + str(i)]  
     
    # Thrust Vector Control 
    if assigned_control_variables.thrust_vector_angle.active:                
        for i in range(len(assigned_control_variables.thrust_vector_angle.assigned_propulsors)): 
            propulsor_tags = assigned_control_variables.thrust_vector_angle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for bus in busses:
                    if propulsor_tags[j] in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tags[j]].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]
    
    # Pitch Command
    if type(segment) ==  RCAIDE.Framework.Mission.Segments.Transition.Constant_Acceleration_Constant_Pitchrate_Constant_Altitude or  \
       type(segment) ==  RCAIDE.Framework.Mission.Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb:  
            for bus in busses:
                for propulsor in bus.propulsors:
                    if type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Electric_Rotor:
                        if type(propulsor.rotor) ==  RCAIDE.Library.Components.Propulsors.Converters.Prop_Rotor: 
                            beta_f         = propulsor.rotor.cruise.design_collective_pitch 
                            t_nondim       = segment.state.numerics.dimensionless.control_points
                            pitch_command  = t_nondim *   beta_f 
                            state.conditions.energy[bus.tag][propulsor.tag].rotor.pitch_command =  pitch_command 
                      
    return 
     
 
    
 
    
