# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_aircraft_MOI.py 
# 
# Created:  September 2024, A. Molloy

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Library.Methods.Stability.Moment_of_Inertia import compute_cuboid_moment_of_inertia, compute_cylinder_moment_of_inertia, compute_fuselage_moment_of_inertia, compute_wing_moment_of_inertia

import RCAIDE
import numpy as  np 

# ------------------------------------------------------------------        
#  Component moments of inertia (MOI) tensors
# ------------------------------------------------------------------  
def calculate_aircraft_MOI(vehicle, CG_location): 
    ''' sums the moments of inertia of each component in the aircraft.

    Assumptions:
    - All other components than those listed are insignificant

    Source:
 
    Inputs:
    - vehicle
    - Center of gravity

    Outputs:
    - Total aircraft moment of inertia tensor

    Properties Used:
    N/A
    '''    
    
    # ------------------------------------------------------------------        
    # Setup
    # ------------------------------------------------------------------      
    # Array to hold the entire aircraft's inertia tensor
    total_MOI = np.zeros((3, 3)) 
    total_mass = 0
    # ------------------------------------------------------------------        
    #  Fuselage(s)
    # ------------------------------------------------------------------      
    for fuselage in vehicle.fuselages:
        I, mass = compute_fuselage_moment_of_inertia(fuselage, CG_location)
        total_MOI += I
        total_mass += mass
        print(fuselage.tag + " MOI added. Mass = "+str(mass))
    
    # ------------------------------------------------------------------        
    #  Wing(s)
    # ------------------------------------------------------------------      
    for wing in vehicle.wings:
        I, mass = compute_wing_moment_of_inertia(wing, wing.mass_properties.mass,  CG_location)
        total_MOI += I
        total_mass += mass
        print(wing.tag + " MOI added. Mass = "+str(mass))
    
    # ------------------------------------------------------------------        
    #  Energy network
    # ------------------------------------------------------------------      
    I_network = np.zeros([3, 3]) 
    for network in vehicle.networks:
        # Electric network
        for bus in network.busses:
            for propulsor in bus.propulsors:
                for item , tag in  propulsor.items():
                    if isinstance(item, RCAIDE.Library.Components.Propulsors.Converters.Rotor):
                        pass
                    if isinstance(item,RCAIDE.Library.Components.Propulsors.Converters.DC_Motor):
                        I, mass = compute_cylinder_moment_of_inertia(item.origin,item.mass_properties.mass, 0, 0, 0,0, CG_location)
                        I_network += I
                        total_mass += mass                        
                        print(item.tag + " MOI added. Mass = "+str(mass))
                for battery in bus.batteries: 
                    I_network += compute_cuboid_moment_of_inertia(battery.origin, battery.mass_properties.mass, 0, 0, 0, 0, 0, 0, CG_location)
                    print(battery.tag + " MOI added. Mass = "+str(mass))
        # Fuel network
        for fuel_line in network.fuel_lines:
            # Propulsor
            for propulsor in fuel_line.propulsors: 
                if isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turbofan ):
                    I, mass= compute_cylinder_moment_of_inertia(propulsor.origin, propulsor.mass_properties.mass, propulsor.engine_length, propulsor.nacelle.diameter/2, 0, 0, CG_location)                    
                    I_network += I
                    total_mass += mass                    
                    print(propulsor.tag + " MOI added. Mass = "+str(mass))
            
            # Fuel tank       
            for fuel_tank in fuel_line.fuel_tanks:
                if isinstance(fuel_tank,RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks.Central_Fuel_Tank ): 
                    I, mass = compute_cuboid_moment_of_inertia(fuel_tank.origin, fuel_tank.fuel.mass_properties.mass, fuel_tank.length, fuel_tank.width, fuel_tank.height, 0, 0, 0, CG_location)
                    I_network += I
                    total_mass += mass
                    print(fuel_tank.tag + " MOI added. Mass = "+str(mass))
                if isinstance(fuel_tank,RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks.Wing_Fuel_Tank): 
                    I, mass = compute_wing_moment_of_inertia(vehicle.wings["main_wing"], fuel_tank.fuel.mass_properties.mass, CG_location, fuel_flag=True)
                    I_network += I
                    total_mass += mass                    
                    print(fuel_tank.tag + " MOI added. Mass = "+str(mass))
                else:
                    pass # TO DO
                        
    total_MOI += I_network    
    
    return(total_MOI,  total_mass)  