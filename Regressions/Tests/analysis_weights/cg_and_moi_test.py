# cg_and_moi_test.py   
from RCAIDE.Framework.Core import Units,  Data ,  Container  

import numpy as  np 
import sys

sys.path.append('../../Vehicles')
# the analysis functions

from Boeing_737             import vehicle_setup as transport_setup
from Cessna_172             import vehicle_setup as general_aviation_setup

def main(): 
    Transport_Aircraft_Test()
    BWB_Aircraft_Test()
    return

def Transport_Aircraft_Test() 
    vehicle = Lockheed_C5a.vehicle_setup()
    
    # ------------------------------------------------------------------
    #   Weight Breakdown
    # ------------------------------------------------------------------  
    weight_analysis =  RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weight_analysis.vehicle = vehicle
    weight_analysis.method  = 'RCAIDE' 
    results =  weight_analysis.evaluate() 
    print("Operating empty weight estimate for C-5a: "+str(results))
    
    # ------------------------------------------------------------------
    #   CG Location
    # ------------------------------------------------------------------    
    compute_vehicle_center_of_gravity(vehicle) 
    CG_location = vehicle.mass_properties.center_of_gravity
    CG_location_true = np.array([[29.5, 0, 0.547]]) #vehicle.mass_properties.center_of_gravity [[32.4,0,0]]
    print("C-5a CG location: "+str(CG_location))
    
    # ------------------------------------------------------------------
    #   Aircraft MOI
    # ------------------------------------------------------------------    
    MOI, total_mass = calculate_aircraft_MOI(vehicle, CG_location)

    # ------------------------------------------------------------------
    #   Cargo MOI
    # ------------------------------------------------------------------    
    Cargo_MOI, mass = compute_cuboid_moment_of_inertia(CG_location, 99790, 36.0, 3.66, 3, 0, 0, 0, CG_location)
    MOI += Cargo_MOI
    total_mass += mass

    print(MOI)
    print("MOI Mass: " + str(total_mass))
    sft2 = 1.355817
    C5a_true = np.array([[27800000 , 0, 2460000], [0, 31800000, 0], [2460000, 0, 56200000]]) * sft2
    error = (MOI - C5a_true) / C5a_true * 100
    print(error)
     
 
    return  

def EVTOL_Aircraft_Test(): 
    vehicle = evtol_setup()
    weight  = Electric.compute_operating_empty_weight(vehicle)
    
    return 
 

if __name__ == '__main__':
    main()
