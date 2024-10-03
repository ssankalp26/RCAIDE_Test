# Regression/scripts/Tests/performance_payload_range.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Methods.Performance.payload_range_diagram        import payload_range_diagram
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric  import compute_weight  

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  

# local imports 
sys.path.append('../../Vehicles')
from Embraer_190    import vehicle_setup as E190_vehicle_setup
from Embraer_190    import configs_setup as E190_configs_setup 
from NASA_X57       import vehicle_setup as X57_vehicle_setup 
from NASA_X57       import configs_setup as X57_configs_setup     

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main(): 
    fuel_payload_range_res = fuel_aircraft_payload_range()
    fuel_r =  fuel_payload_range_res.range
    fuel_r_true =  5739571.581626772
    print('Fuel Range: ' + str(fuel_r[-1]))
    fuel_error =  abs(fuel_r[-1]- fuel_r_true) /fuel_r_true
    assert(abs(fuel_error)<1e-6)
    
    electric_r_true = 137359.4709563402
    electric_payload_range_res = electric_aircraft_payload_range()       
    electric_r =  electric_payload_range_res.range
    print('Electric Range: ' + str(electric_r[-1]))
    electric_error =  abs(electric_r[-1]- electric_r_true) /electric_r_true
    assert(abs(electric_error)<1e-6)
    
    return 
    
    
def fuel_aircraft_payload_range():
    
    # vehicle data
    E190_vehicle  = E190_vehicle_setup() 
    
    # Set up vehicle configs
    E190_configs  = E190_configs_setup(E190_vehicle)

    # create analyses
    E190_analyses = E190_analyses_setup(E190_configs)

    # mission analyses 
    E190_mission = E190_mission_setup(E190_analyses)
    
    # create mission instances (for multiple types of missions)
    E190_missions = missions_setup(E190_mission) 
      
    fuel_payload_range_res  = payload_range_diagram(E190_vehicle,E190_missions.base_mission,'cruise',reserves=0., plot_diagram = True)
        
    return fuel_payload_range_res 

def electric_aircraft_payload_range():
    
    # vehicle data
    X57_vehicle  = X57_vehicle_setup() 
    breakdown    = compute_weight(X57_vehicle, contingency_factor=1.0)    
    X57_vehicle.mass_properties.operating_empty =  breakdown.empty
    X57_vehicle.mass_properties.operating_empty =  breakdown.empty
    
    # Set up vehicle configs
    X57_configs  = X57_configs_setup(X57_vehicle)

    # create analyses
    X57_analyses = X57_analyses_setup(X57_configs)

    # mission analyses 
    X57_mission = X57_mission_setup(X57_analyses)
    
    # create mission instances (for multiple types of missions)
    X57_missions = missions_setup(X57_mission) 
      
    electric_payload_range_res =  payload_range_diagram(X57_vehicle,X57_missions.base_mission,'cruise',reserves=0., plot_diagram = True)
        
    return electric_payload_range_res
  
def E190_analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = E190_base_analysis(config)
        analyses[tag] = analysis

    return analyses

def E190_base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
    
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.vehicle = vehicle
    aerodynamics.settings.number_of_spanwise_vortices   = 25
    aerodynamics.settings.number_of_chordwise_vortices  = 5     
    analyses.append(aerodynamics)   

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses    

# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
 
def E190_mission_setup(analyses):

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
  
    Segments = RCAIDE.Framework.Mission.Segments 
    base_segment = Segments.Segment()
    base_segment.state.numerics.number_of_control_points  = 3  

    # ------------------------------------------------------------------    
    #   Climb Segment 
    # ------------------------------------------------------------------    
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb" 
    segment.analyses.extend( analyses.cruise )  
    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end = 10.5   * Units.km
    segment.air_speed    = 226.0  * Units['m/s']
    segment.climb_rate   = 3.0    * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]  
    segment.assigned_control_variables.body_angle.active             = True                
      
    mission.append_segment(segment)


    # ------------------------------------------------------------------    
    #   Cruise Segment 
    # ------------------------------------------------------------------    

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude  = 10.668 * Units.km  
    segment.air_speed = 230.412 * Units['m/s']
    segment.distance  = 1000 * Units.nmi    
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #  Descent Segment 
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_start = 10.5 * Units.km 
    segment.altitude_end   = 0.0   * Units.km
    segment.air_speed      = 220.0 * Units['m/s']
    segment.descent_rate   = 4.5   * Units['m/s']   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]  
    segment.assigned_control_variables.body_angle.active             = True                
     
    mission.append_segment(segment)
 

    return mission 

def X57_analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = X57_base_analysis(config)
        analyses[tag] = analysis

    return analyses

def X57_base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle()
 
    # ------------------------------------------------------------------
    #  Weights
    weights = RCAIDE.Framework.Analyses.Weights.Weights_eVTOL()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    
    # Calculate extra drag from landing gear: 
    main_wheel_width  = 4. * Units.inches
    main_wheel_height = 12. * Units.inches
    nose_gear_height  = 10. * Units.inches
    nose_gear_width   = 4. * Units.inches 
    total_wheel       = 2*main_wheel_width*main_wheel_height + nose_gear_width*nose_gear_height 
    main_gear_strut_height = 2. * Units.inches
    main_gear_strut_length = 24. * Units.inches
    nose_gear_strut_height = 12. * Units.inches
    nose_gear_strut_width  = 2. * Units.inches 
    total_strut = 2*main_gear_strut_height*main_gear_strut_length + nose_gear_strut_height*nose_gear_strut_width 
    drag_area = 1.4*( total_wheel + total_strut)
    
    
    aerodynamics = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.vehicle                             = vehicle
    aerodynamics.settings.drag_coefficient_increment = drag_area/vehicle.reference_area
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)
    
    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses

def X57_mission_setup(analyses):
    

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'mission' 

    # unpack Segments module
    Segments = RCAIDE.Framework.Mission.Segments  
    base_segment = Segments.Segment()
    base_segment.state.numerics.number_of_control_points  = 3  
    
    # ------------------------------------------------------------------
    # Climb Segment 
    # ------------------------------------------------------------------  
    segment = Segments.Climb.Linear_Speed_Constant_Rate(base_segment) 
    segment.tag = "climb"   
    segment.analyses.extend( analyses.base ) 
    segment.initial_battery_state_of_charge              = 1.0  
    segment.altitude_start                               = 0   * Units.feet  
    segment.altitude_end                                 = 15000.0  * Units.feet 
    segment.air_speed_start                              = 100.    * Units['mph'] 
    segment.air_speed_end                                = 130     * Units.kts
    segment.climb_rate                                   = 500.     * Units['ft/min']       
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
       
    mission.append_segment(segment)  

    # ------------------------------------------------------------------
    #  Cruise Segment 
    # ------------------------------------------------------------------ 
    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.base )  
    segment.altitude                                      = 15000   * Units.feet 
    segment.air_speed                                     = 130 * Units.kts
    segment.distance                                      = 20.   * Units.nautical_mile 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                  
          
    mission.append_segment(segment)
    
    

    # ------------------------------------------------------------------
    #  Descent Segment 
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent" 
    segment.analyses.extend( analyses.base )  
    segment.altitude_end   = 0.0   * Units.km
    segment.air_speed      = 100 * Units.kts
    segment.descent_rate   = 4.5   * Units['m/s']    
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                  
          
    mission.append_segment(segment)    
  
    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------ 
    
    
    return mission

def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions   

if __name__ == '__main__': 
    main()    
    plt.show() 