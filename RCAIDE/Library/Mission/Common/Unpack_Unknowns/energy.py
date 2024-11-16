## @ingroup Library-Missions-Common-Unpack_Unknowns
# RCAIDE/Library/Missions/Common/Unpack_Unknowns/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
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
            for propulsor in fuel_line.assigned_propulsors: 
                state.conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0] = segment.throttle 
    elif assigned_control_variables.throttle.active:                
        for i in range(len(assigned_control_variables.throttle.assigned_propulsors)):
            propulsor_tags = assigned_control_variables.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for fuel_line in fuel_lines:
                    if propulsor_tags[j] in fuel_line.assigned_propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tags[j]].throttle = state.unknowns["throttle_" + str(i)]   
     
    # Thrust Vector Control 
    if assigned_control_variables.thrust_vector_angle.active:                
        for i in range(len(assigned_control_variables.thrust_vector_angle.assigned_propulsors)): 
            propulsor_tags = assigned_control_variables.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for fuel_line in fuel_lines:
                    if propulsor_tags[j] in fuel_line.assigned_propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tags[j]].commanded_thrust_vector_angle = state.unknowns["thrust_vector_" + str(i)]    
    return 

def bus_unknowns(segment):  
    ACV_T  =  segment.assigned_control_variables.throttle
    ACV_TA =  segment.assigned_control_variables.thrust_vector_angle
    
    for network in segment.analyses.energy.vehicle.networks: 
        if 'throttle' in segment: 
            for propulsor in network.propulsor: 
                segment.state.conditions.energy[propulsor.tag].throttle[:,0] = segment.throttle
            
        if ACV_T.active: 
            for i in range(len(ACV_T.assigned_propulsors)): 
                propulsor_group = ACV_T.assigned_propulsors[i]
                for propulsor_name in propulsor_group:  
                    segment.state.conditions.energy[propulsor_name].throttle = segment.state.unknowns["throttle_" + str(i)]  
    
       # Thrust Vector Control 
        if ACV_TA.active:                
            for i in range(len(ACV_TA.assigned_propulsors)): 
                propulsor_group = ACV_TA.assigned_propulsors[i]
                for propulsor_name in propulsor_group:  
                    segment.state.conditions.energy[propulsor_name].commanded_thrust_vector_angle = segment.state.unknowns["thrust_vector_" + str(i)]
    return 
     
 
    
