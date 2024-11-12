## @ingroup Library-Missions-Segments-Ground
# RCAIDE/Library/Missions/Segments/Ground/Battery_Charge_or_Discharge.py
# 
# 
# Created:  Jul 2023, M. Clarke 
import RCAIDE 
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

    if isinstance(segment, RCAIDE.Framework.Mission.Segments.Ground.Battery_Recharge):
        for network in segment.analyses.energy.vehicle.networks:
            time =  0 
            for bus in  network.busses:
                if not 'initial_battery_state_of_charge' in segment:  
                    end_of_flight_soc = 1
                    for battery_module in segment.state.conditions.energy.bus.battery_modules:
                        end_of_flight_soc = min(end_of_flight_soc,battery_module.cell.state_of_charge[-1])
                else:
                    end_of_flight_soc =  segment.initial_battery_state_of_charge
                
                time           =  max(((segment.cutoff_SOC-end_of_flight_soc) / bus.charging_c_rate )*Units.hrs  , time) 
                time           += segment.cooling_time
            t_initial = segment.state.conditions.frames.inertial.time[0,0]
            t_nondim  = segment.state.numerics.dimensionless.control_points
            charging_time      = t_nondim * ( time ) + t_initial 
            segment.state.conditions.frames.inertial.time[:,0] = charging_time[:,0]

    else:

        t_initial = segment.state.conditions.frames.inertial.time[0,0]
        t_nondim  = segment.state.numerics.dimensionless.control_points
        time      = t_nondim * ( segment.time ) + t_initial
        segment.state.conditions.frames.inertial.time[:,0] = time[:,0]