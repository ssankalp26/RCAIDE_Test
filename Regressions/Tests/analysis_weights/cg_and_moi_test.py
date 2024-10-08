# Regression/scripts/Tests/analysis_weights/cg_and_moi_test.py
# 
# Created:  Oct 2024, A. Molloy
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# cg_and_moi_test.py

from RCAIDE.Framework.Core                                                     import Units,  Data ,  Container  
from RCAIDE.Library.Methods.Weights.Correlation_Buildups                       import Common
from RCAIDE.Library.Methods.Stability.Moment_of_Inertia.calculate_aircraft_MOI import calculate_aircraft_MOI
from RCAIDE.Library.Methods.Stability.Center_of_Gravity                        import compute_vehicle_center_of_gravity
from RCAIDE.Library.Methods.Stability.Moment_of_Inertia                        import compute_cuboid_moment_of_inertia

import numpy as  np
import RCAIDE
import sys   

sys.path.append('../../Vehicles')

# the analysis functions
from Lockheed_C5a           import vehicle_setup as transport_setup
from Cessna_172             import vehicle_setup as general_aviation_setup

def main(): 
    Transport_Aircraft_Test()
    General_Aviation_Test()
    return

def Transport_Aircraft_Test():
    vehicle = transport_setup()
    
    # update fuel weight to 60%
    vehicle.networks.fuel.fuel_lines.fuel_line.fuel_tanks.wing_fuel_tank.fuel.mass_properties.mass = 0.6 * vehicle.networks.fuel.fuel_lines.fuel_line.fuel_tanks.wing_fuel_tank.fuel.mass_properties.mass

    # ------------------------------------------------------------------
    #   Weight Breakdown 
    # ------------------------------------------------------------------  
    weight_analysis                               = RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weight_analysis.vehicle                       = vehicle
    weight_analysis.method                        = 'Raymer'
    weight_analysis.settings.use_max_fuel_weight  = False  
    results                                       = weight_analysis.evaluate() 
    
    # ------------------------------------------------------------------
    #   CG Location
    # ------------------------------------------------------------------    
    compute_vehicle_center_of_gravity( weight_analysis.vehicle) 
    CG_location      =  weight_analysis.vehicle.mass_properties.center_of_gravity
    
    # ------------------------------------------------------------------
    #   Operating Aircraft MOI
    # ------------------------------------------------------------------    
    MOI, total_mass = calculate_aircraft_MOI(weight_analysis.vehicle, CG_location)

    # ------------------------------------------------------------------
    #   Payload MOI
    # ------------------------------------------------------------------    
    Cargo_MOI, mass =  compute_cuboid_moment_of_inertia(CG_location, 99790*Units.kg, 36.0, 3.66, 3, 0, 0, 0, CG_location)
    MOI             += Cargo_MOI
    total_mass      += mass
    
    print(weight_analysis.vehicle.tag + ' Moment of Intertia')
    print(MOI)
    accepted  = np.array([[32345317.83576559 , 2824293.44847796  , 3423062.2751829 ],
                          [ 2824293.44847796 , 42743291.89239228  ,      0.        ],
                          [ 3423062.2751829  ,       0.       ,  61946007.2916059 ]])
    MOI_error     = MOI - accepted

    # Check the errors
    error = Data()
    error.Ixx   = MOI_error[0, 0]
    error.Iyy   = MOI_error[1, 1]
    error.Izz   = MOI_error[2, 2]
    error.Ixz   = MOI_error[2, 0]
    error.Ixy   = MOI_error[1, 0]

    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6) 
    
    return  
 

def General_Aviation_Test(): 
    # ------------------------------------------------------------------
    #   Weight Breakdown 
    # ------------------------------------------------------------------  
    weight_analysis                               = RCAIDE.Framework.Analyses.Weights.Weights_General_Aviation()
    weight_analysis.vehicle                       = general_aviation_setup() 
    results                                       = weight_analysis.evaluate() 
    
    # ------------------------------------------------------------------
    #   CG Location
    # ------------------------------------------------------------------    
    compute_vehicle_center_of_gravity(weight_analysis.vehicle) 
    CG_location      = weight_analysis.vehicle.mass_properties.center_of_gravity
    
    # ------------------------------------------------------------------
    #   Operating Aircraft MOI
    # ------------------------------------------------------------------    
    MOI, total_mass = calculate_aircraft_MOI(weight_analysis.vehicle, CG_location) 

    print(weight_analysis.vehicle.tag + ' Moment of Intertia')
    print(MOI)
    
    accepted  = np.array([[1290.55346634 ,  43.52720306  , 43.52720306],
                          [  43.52720306 , 980.82840051  ,  0.      ],
                          [  43.52720306 ,   0.     ,    2194.18580632]])
    
    MOI_error     = MOI - accepted

    # Check the errors
    error = Data()
    error.Ixx   = MOI_error[0, 0]
    error.Iyy   = MOI_error[1, 1]
    error.Izz   = MOI_error[2, 2]
    error.Ixz   = MOI_error[2, 0]
    error.Ixy   = MOI_error[1, 0]

    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)   
    
    return

if __name__ == '__main__':
    main()
