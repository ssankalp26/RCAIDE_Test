# caclulate_aircraft_MOI.py   
from RCAIDE.Framework.Core import Units,  Data ,  Container
from RCAIDE.Library.Methods.Stability.Moment_of_Inertia import compute_cuboid_moment_of_inertia, compute_cylinder_moment_of_inertia, compute_fuselage_moment_of_inertia, compute_wing_moment_of_inertia

import RCAIDE
import numpy as  np 

# ------------------------------------------------------------------        
#  Component moments of inertia (MOI) tensors
# ------------------------------------------------------------------  
def caclulate_aircraft_MOI(vehicle, CG_location): 
    
    total_MOI = np.zeros(3)
    
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
            for propulsor in bus.properties:
                if type(propulsor) == RCAIDE.Library.Components.Propulsors.Converters.Propeller:
                    I_network += compute_cylinder_moment_of_inertia()
                if type(propulsor) == RCAIDE.Library.Components.Propulsors.Converters.DC_Motor:
                    I_network += compute_cylinder_moment_of_inertia()
                if type(propulsor) == RCAIDE.Library.Components.Energy.Batteries:
                    I_network += compute_cuboid_moment_of_inertia()
    total_MOI += I_network
    
    return(total_MOI)  
