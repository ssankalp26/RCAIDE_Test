# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------     
import RCAIDE
from RCAIDE.Framework.Core import Units, Data

# Routines   
import numpy as np
import sys 
import os
from copy import  deepcopy

sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Navion    import vehicle_setup , configs_setup

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():  
    # vehicle data
    vehicle  = vehicle_setup() 
    
    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses 
    mission = mission_setup(analyses)
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 
     
    # mission analysis 
    results = missions.base_mission.evaluate() 

    segment_results =  results.segments.cruise.conditions
    # ------------------------------------------------------------------------------------------------------------------------  
    # Post Process Results 
    # ------------------------------------------------------------------------------------------------------------------------     
    CD                      = segment_results.static_stability.coefficients.drag[0,0]  
    CM                      = abs(segment_results.static_stability.coefficients.M[0,0])
    spiral_criteria         = segment_results.static_stability.spiral_criteria[0,0]
    NP                      = segment_results.static_stability.neutral_point[0,0]
    cg                      = vehicle.mass_properties.center_of_gravity[0][0]
    MAC                     = vehicle.wings.main_wing.chords.mean_aerodynamic
    static_margin           = (NP - cg)/MAC
    CM_alpha                = segment_results.static_stability.derivatives.CM_alpha[0,0] 
   
    print("Drag Coefficient           : " + str(CD))
    print("Moment Coefficient         : " + str(CM))
    print("Static Margin              : " + str(static_margin))
    print("CM alpla                   : " + str(CM_alpha))    
    print("Spiral Criteria            : " + str(spiral_criteria))
    
    CD_true       =  0.016000109659799963
    CM_true       =  0.03418551375391235
    NP_true       =  2.5671448424629455
    CM_alpha_true =  -1.6388574504280666
    
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

# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in list(configs.items()):
        analysis = base_analysis(config)
        analyses[tag] = analysis
 
    return analyses


def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 

    # ------------------------------------------------------------------
    #  Weights
    weights                                          = RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weights.vehicle                                  = vehicle
    analyses.append(weights)
 
    #  Aerodynamics Analysis
    aerodynamics                                        = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics.vehicle                                = vehicle
    aerodynamics.settings.number_of_spanwise_vortices   = 40
    aerodynamics.settings.use_surrogate                 = False  
    analyses.append(aerodynamics)
     
    # Stability Analysis
    stability                                        = RCAIDE.Framework.Analyses.Stability.Vortex_Lattice_Method()
    stability.vehicle                                = vehicle
    stability.settings.number_of_spanwise_vortices   = 40  
    stability.settings.use_surrogate                 = False  
    analyses.append(stability)    
  
    #  Energy
    energy                                           = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle                                   = vehicle 
    analyses.append(energy)
 
    #  Planet Analysis
    planet                                           = RCAIDE.Framework.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere                                       = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet                       = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses 
   
# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------

def mission_setup(analyses): 

    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'mission'
  
    # unpack Segments module
    Segments = RCAIDE.Framework.Mission.Segments

    #   Cruise Segment: constant Speed, constant altitude 
    segment                           = Segments.Untrimmed.Untrimmed()
    segment.analyses.extend( analyses.base )   
    segment.tag                       = "cruise"
    segment.angle_of_attack           = 0
    segment.bank_angle                = 0
    segment.altitude                  = 5000 * Units.feet
    segment.air_speed                 = 60

    segment.flight_dynamics.force_x   = True    
    segment.flight_dynamics.force_z   = True    
    segment.flight_dynamics.force_y   = True     
    segment.flight_dynamics.moment_y  = True 
    segment.flight_dynamics.moment_x  = True
    segment.flight_dynamics.moment_z  = True
    
    mission.append_segment(segment)  
    
    return mission



def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  

if __name__ == '__main__': 
    main()    