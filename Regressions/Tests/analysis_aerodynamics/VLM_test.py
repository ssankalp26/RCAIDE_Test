# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------     
import RCAIDE
from RCAIDE.Framework.Core import Units, Data   
from RCAIDE.Framework.Mission.Common                       import Results 
from RCAIDE.Library.Methods.Stability.Common               import compute_dynamic_flight_modes    
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method.evaluate_VLM import evaluate_no_surrogate
from RCAIDE.Library.Mission.Common.Update  import orientations
from RCAIDE.Library.Mission.Common.Unpack_Unknowns import orientation

# Routines   
import numpy as np
import sys 
import os
from copy import  deepcopy

sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Navion    import vehicle_setup 

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main(): 
    
    # vehicle data
    vehicle     = vehicle_setup() 
    g           = 9.81   
    m           = vehicle.mass_properties.max_takeoff 
    S           = vehicle.reference_area
    atmosphere  = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data   = atmosphere.compute_values(altitude = 5000*Units.feet )       
      
    
    # ------------------------------------------------------------------------------------------------------------------------  
    # Stick Fixed 
    # ------------------------------------------------------------------------------------------------------------------------       
    # ------------------------------------------------------------------------------------------------------------------------  
    # initialize run conditions                                         
    stick_fixed_conditions                                             = Results()
    stick_fixed_conditions.freestream.density[:,0]                     = atmo_data.density[0,0]
    stick_fixed_conditions.freestream.gravity[:,0]                     = g          
    stick_fixed_conditions.freestream.speed_of_sound[:,0]              = atmo_data.speed_of_sound[0,0] 
    stick_fixed_conditions.freestream.dynamic_viscosity[:,0]           = atmo_data.dynamic_viscosity[0,0] 
    stick_fixed_conditions.freestream.temperature                      = atmo_data.temperature[0,0] 
    stick_fixed_conditions.freestream.velocity[:,0]                    = 60 
    stick_fixed_conditions.frames.inertial.velocity_vector[:,0]        = 60 
    stick_fixed_conditions.freestream.mach_number                      = stick_fixed_conditions.freestream.velocity/stick_fixed_conditions.freestream.speed_of_sound
    stick_fixed_conditions.freestream.dynamic_pressure                 = 0.5 * stick_fixed_conditions.freestream.density *  (stick_fixed_conditions.freestream.velocity ** 2)
    stick_fixed_conditions.freestream.reynolds_number                  = stick_fixed_conditions.freestream.density * stick_fixed_conditions.freestream.velocity / stick_fixed_conditions.freestream.dynamic_viscosity  
     
    # ------------------------------------------------------------------------------------------------------------------------  
    # initialize analyses                                      
    aerodynamics                                      = RCAIDE.Framework.Analyses.Stability.Vortex_Lattice_Method()   
    aerodynamics.settings.number_of_spanwise_vortices = 40
    aerodynamics.vehicle                              = vehicle 
    aerodynamics.settings.use_surrogate               = False 
    aerodynamics.initialize()
     
    # ------------------------------------------------------------------------------------------------------------------------  
    # Run VLM 
    equilibrium_state                               = RCAIDE.Framework.Mission.Common.State()
    equilibrium_state.conditions                    = stick_fixed_conditions  
    stick_fixed_segment                             = RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Altitude()
    stick_fixed_segment.conditions                  = stick_fixed_conditions
    stick_fixed_segment.state.conditions            = stick_fixed_conditions
    stick_fixed_segment.analyses                    = Data()
    stick_fixed_segment.analyses.aerodynamics       = aerodynamics
    orientation(stick_fixed_segment)
    orientations(stick_fixed_segment) 
    
    evaluate_no_surrogate(stick_fixed_segment,aerodynamics.settings,vehicle) 
    compute_dynamic_flight_modes(stick_fixed_segment,aerodynamics.settings,vehicle)

    # ------------------------------------------------------------------------------------------------------------------------  
    # Post Process Results 
    # ------------------------------------------------------------------------------------------------------------------------     
    CD                      = stick_fixed_conditions.static_stability.coefficients.drag[0,0]  
    CM                      = abs(stick_fixed_conditions.static_stability.coefficients.M[0,0])
    spiral_criteria         = stick_fixed_conditions.static_stability.spiral_criteria[0,0]
    NP                      = stick_fixed_conditions.static_stability.neutral_point[0,0]
    cg                      = vehicle.mass_properties.center_of_gravity[0][0]
    MAC                     = vehicle.wings.main_wing.chords.mean_aerodynamic
    static_margin           = (NP - cg)/MAC
    CM_alpha                = stick_fixed_conditions.static_stability.derivatives.CM_alpha[0,0] 
   
    print("Drag Coefficient           : " + str(CD))
    print("Moment Coefficient         : " + str(CM))
    print("Static Margin              : " + str(static_margin))
    print("CM alpla                   : " + str(CM_alpha))    
    print("Spiral Criteria            : " + str(spiral_criteria))
    
    CD_true       =  0.016760164266095924
    CM_true       =  0.014948948535811293
    NP_true       =  2.5672633278782984
    CM_alpha_true =  -1.6388205972121546
    
    error =  Data()
    error.CD        =  np.abs((CD - CD_true)/CD_true)  
    error.CM        =  np.abs((CM - CM_true)/CM_true)  
    error.NP        =  np.abs((NP - NP_true)/NP_true)  
    error.CM_alpha  =  np.abs((CM_alpha - CM_alpha_true)/CM_alpha_true)    

    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6) 
        
    return    

if __name__ == '__main__': 
    main()    