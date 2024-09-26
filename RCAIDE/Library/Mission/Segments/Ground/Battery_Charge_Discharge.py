## @ingroup Library-Missions-Segments-Ground
# RCAIDE/Library/Missions/Segments/Ground/Battery_Charge_or_Discharge.py
# 
# 
# Created:  Jul 2023, M. Clarke 
 
from RCAIDE.Framework.Core import  Units
import  numpy as  np
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Missions-Segments-Ground 
def initialize_conditions(segment):  
    """Sets the specified conditions which are given for the segment type.

    Assumptions: 
    During recharging, the charge time associated with the largest capacity battery pack is used 
    
    Source:
    N/A

    Inputs:
    segment.overcharge_contingency              [-]
    battery.                                    [-]

    Outputs: 
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """    
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions   
    time =  0 
    for network in segment.analyses.energy.vehicle.networks:
        for bus in  network.busses:
            time           =  np.max((1-segment.state.initials.conditions.energy[bus.tag].SOC[-1] / bus.charging_c_rate )*Units.hrs  , time)
            
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_nondim  = segment.state.numerics.dimensionless.control_points
    
    #segment.state.
    charging_time      = t_nondim * ( time ) + t_initial
    
    segment.state.conditions.frames.inertial.time[:,0] = charging_time[:,0] 

