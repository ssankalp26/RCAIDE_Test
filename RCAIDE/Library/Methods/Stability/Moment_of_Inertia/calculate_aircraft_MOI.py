# caclulate_aircraft_MOI.py   
from RCAIDE.Library.Methods.Stability.Moment_of_Inertia import compute_cuboid_moment_of_inertia, compute_cylinder_moment_of_inertia, compute_fuselage_moment_of_inertia, compute_wing_moment_of_inertia

import RCAIDE
import numpy as  np 

# ------------------------------------------------------------------        
#  Component moments of inertia (MOI) tensors
# ------------------------------------------------------------------  
def caclulate_aircraft_MOI(vehicle, CG_location): 
    
    total_MOI = np.zeros(3) # Array to hold the entire aircraft's inertia tensor
    
    # ------------------------------------------------------------------        
    #  Fuselage(s)
    # ------------------------------------------------------------------      
    for fuselage in vehicle.fuselages:
        total_MOI += compute_fuselage_moment_of_inertia(fuselage, CG_location)
    
    # ------------------------------------------------------------------        
    #  Wing(s)
    # ------------------------------------------------------------------      
    for wing in vehicle.wings:
        total_MOI += compute_wing_moment_of_inertia(wing, CG_location)
    
    # ------------------------------------------------------------------        
    #  Electric network
    # ------------------------------------------------------------------      
    I_network = np.zeros(3) 
    for network in vehicle.network:
        for bus in network.busses:
            for propulsor in bus.propulsors:
                for item , tag in  propulsor.items():
                    if isinstance(item, RCAIDE.Library.Components.Propulsors.Converters.Rotor):
                        pass 
                    if isinstance(item,RCAIDE.Library.Components.Propulsors.Converters.DC_Motor):
                        I_network += compute_cylinder_moment_of_inertia(item.origin,item.mass_properties.mass, need_length, need_radius, 0,0, CG_location)
                for battery in bus.batteries: 
                    I_network += compute_cuboid_moment_of_inertia(battery.origin, battery.mass_properties.mass, need_length, need_width, need_height, 0, 0, 0, CG_location)

        for fuel_line in network.fuel_lines:
            for propulsor in fuel_line.propulsors: 
                for item , tag in  propulsor.items():
                    if isinstance(item,RCAIDE.Library.Components.Propulsors.Turbofan):
                        pass # TO DO 
                for fuel_tank in fuel_line.fuel_tanks:
                    if isinstance(fuel_tank,RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks.Central_Fuel_Tank ): 
                        I_network += compute_cuboid_moment_of_inertia(fuel_tank.origin, fuel_tank.mass_properties.mass, fuel_tank.length, fuel_tank.width, fuel_tank.height, 0, 0, 0, CG_location)
                    if isinstance(fuel_tank,RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks.Wing_Fuel_Tank ): 
                        I_network += compute_wing_moment_of_inertia(vehicle.wings["main_wing"], CG_location, fuel_flag=True)
                    else:
                        pass # TO DO 
                        
    total_MOI += I_network    
    
    return(total_MOI)  
