# RCAIDE/Library/Missions/Segments/Untrimmed/Untrimmed.py
# 
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------   
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    A fixed speed and altitude

    Source:
    N/A

    Inputs:
    segment.altitude                               [meters]
    segment.air_speed                              [meters/second]
    segment.linear_acceleration_x                         [meters/second^2]
    segment.sideslip_angle                         [radians]
    segment.linear_acceleration_z                         [meters/second^2]

    Outputs:
    conditions.frames.inertial.acceleration_vector [meters/second^2]
    conditions.frames.inertial.velocity_vector     [meters/second]
    conditions.frames.inertial.position_vector     [meters]
    conditions.freestream.altitude                 [meters]
    conditions.frames.inertial.time                [seconds]

    Properties Used:
    N/A
    """      
    
    # unpack
    alt                    = segment.altitude
    air_speed              = segment.air_speed  
    sideslip               = segment.sideslip_angle
    linear_acceleration_x  = segment.linear_acceleration_x
    linear_acceleration_y  = segment.linear_acceleration_y 
    linear_acceleration_z  = segment.linear_acceleration_z
    angular_acceleration_x = segment.angular_acceleration_x
    angular_acceleration_y = segment.angular_acceleration_y
    angular_acceleration_z = segment.angular_acceleration_z
    
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
    
    # pack
    air_speed_x                                                           = np.cos(sideslip)*air_speed 
    air_speed_y                                                           = np.sin(sideslip)*air_speed 
    segment.state.conditions.freestream.altitude[:,0]                     = alt
    segment.state.conditions.frames.inertial.position_vector[:,2]         = -alt # z points down
    segment.state.conditions.frames.inertial.velocity_vector[:,0]         = air_speed_x
    segment.state.conditions.frames.inertial.velocity_vector[:,1]         = air_speed_y
    segment.state.conditions.frames.inertial.acceleration_vector          = np.array([[linear_acceleration_x,linear_acceleration_y,linear_acceleration_z]]) 
    segment.state.conditions.frames.inertial.angular_acceleration_vector  = np.array([[angular_acceleration_x,angular_acceleration_y,angular_acceleration_z]]) 