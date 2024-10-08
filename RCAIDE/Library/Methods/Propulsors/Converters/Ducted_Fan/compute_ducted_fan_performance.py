# RCAIDE/Library/Methods/Propulsors/Converters/Rotor/compute_ducted_fan_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from RCAIDE.Framework.Core                              import Data , Units, orientation_product, orientation_transpose   

# package imports
import  numpy as  np 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Generalized Rotor Class
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Propulsion-Converters
def compute_ducted_fan_performance(propulsor,state,disributor,center_of_gravity= [[0.0, 0.0,0.0]]):
    """Analyzes a general ducted_fan given geometry and operating conditions.

    Assumptions:
    per source

    Source:
    
    Inputs: 

    Outputs: 
    """

    # Unpack ducted_fan blade parameters and operating conditions 
    conditions            = state.conditions
    ducted_fan            = propulsor.ducted_fan
    propulsor_conditions  = conditions.energy[disributor.tag][propulsor.tag]
    commanded_TV          = propulsor_conditions.commanded_thrust_vector_angle
    ducted_fan_conditions = propulsor_conditions[ducted_fan.tag]
     
    tip_mach            = ducted_fan_conditions.tip_mach             
    operating_altitude  = ducted_fan_conditions.operating_altitude  
    inflow_velocity     = ducted_fan_conditions.inflow_velocity
    
    omega = ducted_fan_conditions.omega 
    n     = omega/(2.*np.pi)   # Rotations per second
    D     = ducted_fan.tip_radius * 2
    
    # Unpack freestream conditions
    rho     = conditions.freestream.density[:,0,None] 
    Vv      = conditions.frames.inertial.velocity_vector 

    # Number of radial stations and segment control point
    B        = ducted_fan.number_of_blades
    Nr       = len(ducted_fan.number_of_radian_station)
    ctrl_pts = len(Vv)
     
    # Velocity in the rotor frame
    T_body2inertial         = conditions.frames.body.transform_to_inertial
    T_inertial2body         = orientation_transpose(T_body2inertial)
    V_body                  = orientation_product(T_inertial2body,Vv)
    body2thrust,orientation = ducted_fan.body_to_prop_vel(commanded_TV) 
    T_body2thrust           = orientation_transpose(np.ones_like(T_body2inertial[:])*body2thrust)
    V_thrust                = orientation_product(T_body2thrust,V_body)

    # Check and correct for hover
    V         = V_thrust[:,0,None]
    V[V==0.0] = 1E-6
    
    
    ctrl_pts = len(inflow_velocity)  
    pts = (inflow_velocity,tip_mach,operating_altitude)

    
    thrust         = ducted_fan.surrogates.thrust(pts)            
    power          = ducted_fan.surrogates.power(pts)                 
    efficiency     = ducted_fan.surrogates.efficiency(pts)            
    torque         = ducted_fan.surrogates.torque(pts)                
    Ct             = ducted_fan.surrogates.thrust_coefficient(pts)    
    Cp             = ducted_fan.surrogates.power_coefficient(pts)     
    advance_ratio  = ducted_fan.surrogates.advance_ratio(pts)
    

    Cq       = torque/(rho*(n*n)*(D*D*D*D*D)) 
    # calculate coefficients    
    thrust_prop_frame      = np.zeros((ctrl_pts,3))
    thrust_prop_frame[:,0] = thrust[:,0]
    thrust_vector          = orientation_product(orientation_transpose(T_body2thrust),thrust_prop_frame)
 
    # Compute moment 
    moment_vector           = np.zeros((ctrl_pts,3))
    moment_vector[:,0]      = ducted_fan.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = ducted_fan.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = ducted_fan.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust_vector) 
     
    outputs                                       = Data( 
                torque                            = torque,
                thrust                            = thrust_vector,  
                power                             = power,
                moment                            = moment, 
                rpm                               = omega /Units.rpm ,   
                tip_mach                          = tip_mach, 
                efficiency                        = efficiency,         
                number_radial_stations            = Nr,
                advance_ratio                     = advance_ratio, 
                orientation                       = orientation, 
                speed_of_sound                    = conditions.freestream.speed_of_sound,
                density                           = conditions.freestream.density,
                velocity                          = Vv,     
                omega                             = omega,  
                thrust_per_blade                  = thrust/B,
                thrust_coefficient                = Ct, 
                torque_per_blade                  = torque/B,
                torque_coefficient                = Cq,
                power_coefficient                 = Cp,  
        ) 
    
    conditions.energy[disributor.tag][propulsor.tag][ducted_fan.tag] = outputs   
    
    return  
