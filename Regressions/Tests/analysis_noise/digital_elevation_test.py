# digital_elevation_and_noise_hemispheres_test.py
#
# Created: Dec 2023 M. Clarke  
 
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
# RCAIDE Imports 
import RCAIDE
from RCAIDE.Framework.Core import Units , Data 
from RCAIDE.Library.Plots import *       
# Python imports
import matplotlib.pyplot as plt  
import sys 
import numpy as np     

# local imports 
sys.path.append('../../Vehicles')
from NASA_X57    import vehicle_setup, configs_setup     

# ----------------------------------------------------------------------
#   Main
# ---------------------------------------------------------------------- 
def main():       
    plot_elevation_contours(topography_file   ='LA_Metropolitan_Area.txt',use_lat_long_coordinates = True, save_filename = "Elevation_Contours_Lat_Long")

    plot_elevation_contours(topography_file   ='LA_Metropolitan_Area.txt',use_lat_long_coordinates = False, save_filename = "Elevation_Contours_XY")  
      
    vehicle  = vehicle_setup()      
    vehicle.networks.electric.busses.bus.identical_propulsors     = False # only for regression     
    configs  = configs_setup(vehicle) 
    analyses = analyses_setup(configs)  
    mission  = mission_setup(analyses)
    missions = missions_setup(mission)  
    results  = missions.base_mission.evaluate()   
    
    regression_plotting_flag = False 
    flight_times = np.array(['06:00:00','06:15:00','06:30:00','06:45:00',
                             '07:00:00','07:15:00','07:30:00','07:45:00',
                             '08:00:00','08:15:00','08:30:00','08:45:00',
                             '09:00:00','09:15:00','09:30:00','09:45:00',
                             '10:00:00','10:15:00','10:30:00','10:45:00',
                             '11:00:00','11:15:00','11:30:00','11:45:00',
                             '12:00:00','12:15:00','12:30:00','12:45:00',
                             '13:00:00','13:15:00','13:30:00','13:45:00',
                             '14:00:00','14:15:00','14:30:00','14:45:00',
                             '15:00:00'])

    noise_data   = post_process_noise_data(results,
                                           flight_times = flight_times, 
                                           DNL_time_period= 24*Units.hours,
                                           LAeqt_time_period  = 15*Units.hours,
                                           SENEL_time_period = 24*Units.hours)  

    
    plot_results(results,noise_data,regression_plotting_flag)   

    X57_SPL        = np.max(results.segments.climb.conditions.noise.total_SPL_dBA) 
    X57_SPL_true   = 45.232719642900996
    X57_diff_SPL   = np.abs(X57_SPL - X57_SPL_true)
    print('Error: ',X57_diff_SPL)
    assert np.abs((X57_SPL - X57_SPL_true)/X57_SPL_true) < 1e-3    
     
    return      

# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ---------------------------------------------------------------------- 
def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis      = base_analysis(config) 
        analyses[tag] = analysis

    return analyses  


def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
 
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Framework.Analyses.Weights.Weights_EVTOL()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.vehicle  = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)   
 
    #  Noise Analysis   
    noise = RCAIDE.Framework.Analyses.Noise.Frequency_Domain_Buildup()   
    noise.vehicle = vehicle
    noise.settings.mean_sea_level_altitude          = False         
    noise.settings.aircraft_departure_coordinates   = [33.94067953101678, -118.40513722978149]
    noise.settings.aircraft_destination_coordinates = [33.81713622114423, -117.92111163722772]  
    #noise.settings.topography_file                  = 'LA_Metropolitan_Area.txt' 
    analyses.append(noise)

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
#  Set Up Mission 
# ---------------------------------------------------------------------- 
def mission_setup(analyses):      
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    mission       = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag   = 'mission' 
    Segments      = RCAIDE.Framework.Mission.Segments  
    base_segment  = Segments.Segment()   
    base_segment.state.numerics.number_of_control_points  = 10
    base_segment.state.numerics.discretization_method     = RCAIDE.Library.Methods.Utilities.Chebyshev.linear_data
    
    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment) 
    segment.tag = "cruise"   
    segment.analyses.extend( analyses.base ) 
    segment.initial_battery_state_of_charge              = 1.0       
    segment.altitude                                     = 30
    segment.air_speed                                    = 100
    segment.distance                                     = 1000  
    segment.true_course                                  = 0
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
       
    mission.append_segment(segment)      
     
    return mission

# ----------------------------------------------------------------------
#  Set Up Missions 
# ---------------------------------------------------------------------- 
def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  


# ----------------------------------------------------------------------
#  Plot Resuls 
# ---------------------------------------------------------------------- 
def plot_results(results,noise_data,regression_plotting_flag): 
    # Plot noise hemisphere
    plot_noise_hemisphere(noise_data,
                          noise_level      = noise_data.SPL_dBA[1], 
                          min_noise_level  = 20,  
                          max_noise_level  = 90, 
                          noise_scale_label= 'SPL [dBA]',
                          show_figure      = regression_plotting_flag)     
    

    # Plot noise hemisphere with vehicle 
    plot_noise_hemisphere(noise_data,
                          noise_level      = noise_data.SPL_dBA[1], 
                          min_noise_level  = 20,  
                          max_noise_level  = 90, 
                          noise_scale_label= 'SPL [dBA]',
                          save_filename    = "Noise_Hemisphere_With_Aircraft", 
                          vehicle          = results.segments.cruise.analyses.aerodynamics.vehicle,
                          show_figure      = regression_plotting_flag)       
    
    plot_noise_level(noise_data,
                    noise_level  = noise_data.SPL_dBA[0], 
                    save_filename="Sideline_Noise_Levels")  
    
    # Maximum Sound Pressure Level   
    plot_3D_noise_contour(noise_data,
                          noise_level      = np.max(noise_data.SPL_dBA,axis=0), 
                          min_noise_level  = 20,  
                          max_noise_level  = 90, 
                          noise_scale_label= 'SPL [dBA]',
                          save_filename    = "SPL_max_Noise_3D_Contour",
                          show_figure      = regression_plotting_flag)   
                        

    # Day Night Average Noise Level 
    plot_3D_noise_contour(noise_data,
                        noise_level      = noise_data.DNL,
                        min_noise_level  = 20,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'DNL',
                        show_microphones = True, 
                        save_filename    = "DNL_Noise_3D_Contour",
                        show_figure      = regression_plotting_flag) 
    

    # Equivalent Noise Level
    plot_3D_noise_contour(noise_data,
                        noise_level      = noise_data.L_AeqT,
                        min_noise_level  = 20,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'LAeqT',
                        show_trajectory  = True,
                        save_filename    = "LAeqT_Noise_3D_Contour",
                        show_figure      = regression_plotting_flag)    
    

    # 24-hr Equivalent Noise Level
    plot_3D_noise_contour(noise_data,
                       noise_level      = noise_data.L_AeqT,
                       min_noise_level  = 20,  
                       max_noise_level  = 90, 
                       noise_scale_label= '24hr-LAeqT',
                       save_filename    = "24hr_LAeqT_Noise_3D_Contour", 
                       use_lat_long_coordinates = False,                         
                       show_figure      = regression_plotting_flag)      
    

    # Single Event Noise Exposure Level
    plot_3D_noise_contour(noise_data,
                       noise_level      = noise_data.SENEL,
                       min_noise_level  = 20,  
                       max_noise_level  = 90, 
                       noise_scale_label= 'SENEL',
                       save_filename    = "SENEL_Noise_3D_Contour",
                       show_figure      = regression_plotting_flag)
    
    # Maximum Sound Pressure Level   
    plot_2D_noise_contour(noise_data,
                        noise_level      = np.max(noise_data.SPL_dBA,axis=0), 
                        min_noise_level  = 20,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'SPL [dBA]',
                        save_filename    = "SPL_max_Noise_2D_Contour",
                        show_elevation   = True,
                        use_lat_long_coordinates= False,
                        show_figure      = regression_plotting_flag)   
                        

    # Day Night Average Noise Level 
    plot_2D_noise_contour(noise_data,
                        noise_level      = noise_data.DNL,
                        min_noise_level  = 20,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'DNL',
                        save_filename    = "DNL_Noise_2D_Contour",
                        show_figure      = regression_plotting_flag) 
    

    # Equivalent Noise Level
    plot_2D_noise_contour(noise_data,
                        noise_level      = noise_data.L_AeqT,
                        min_noise_level  = 20,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'LAeqT',
                        save_filename    = "LAeqT_Noise_2D_Contour",
                        show_figure      = regression_plotting_flag)    
    

    # 24-hr Equivalent Noise Level
    plot_2D_noise_contour(noise_data,
                       noise_level      = noise_data.L_AeqT,
                       min_noise_level  = 20,  
                       max_noise_level  = 90, 
                       noise_scale_label= '24hr-LAeqT',
                       save_filename    = "24hr_LAeqT_Noise_2D_Contour",
                       show_figure      = regression_plotting_flag)      
    

    # Single Event Noise Exposure Level
    plot_2D_noise_contour(noise_data,
                       noise_level      = noise_data.SENEL,
                       min_noise_level  = 20,  
                       max_noise_level  = 90, 
                       noise_scale_label= 'SENEL',
                       save_filename    = "SENEL_Noise_2D_Contour",
                       show_figure      = regression_plotting_flag)      
    return  

if __name__ == '__main__': 
    main()    
    plt.show()
